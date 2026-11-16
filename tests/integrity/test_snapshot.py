import json
import sqlite3

from conftest import insert
from integrity.snapshot import dumps, normalise_new_ids, stored_state


def test_snapshot_covers_every_table_and_column(db_copy):
    insert(db_copy, "bikes", bike_id="b1", bike_name="Bike")
    state = stored_state(db_copy)
    connection = sqlite3.connect(db_copy)
    tables = {row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")}
    assert set(state) == tables
    for table in tables:
        columns = {row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')}
        for row in state[table].values():
            assert set(row) == columns
    connection.close()
    assert state["bikes"]["b1"]["bike_name"] == "Bike"


def test_snapshot_keeps_null_and_zero_apart(db_copy):
    insert(db_copy, "components", component_id="c1", lifetime_remaining=None)
    insert(db_copy, "components", component_id="c2", lifetime_remaining=0.0)
    components = stored_state(db_copy)["components"]
    assert components["c1"]["lifetime_remaining"] is None
    assert components["c2"]["lifetime_remaining"] == 0.0


def test_snapshot_rounds_floats_to_six_decimals(db_copy):
    insert(db_copy, "components", component_id="c1", component_distance=1.23456789)
    assert stored_state(db_copy)["components"]["c1"]["component_distance"] == 1.234568


def test_snapshot_round_trips_non_ascii(db_copy):
    name = "Bremseklosser bak æøå"
    insert(db_copy, "components", component_id="c1", component_name=name)
    state = stored_state(db_copy)
    text = dumps(state)
    assert name in text
    assert json.loads(text) == state
    assert json.loads(text)["components"]["c1"]["component_name"] == name


def test_normalise_new_ids_is_stable(tmp_path, db_copy):
    insert(db_copy, "components", component_id="old1")
    baseline = set(stored_state(db_copy)["components"])
    states = []
    for suffix in ("aaaa1111", "bbbb2222"):
        path = tmp_path / f"{suffix}.sqlite"
        path.write_bytes(db_copy.read_bytes())
        insert(path, "components", component_id=f"comp-{suffix}")
        insert(path, "collections", collection_id=f"col-{suffix}",
               components=json.dumps([f"comp-{suffix}", "old1"]))
        states.append(normalise_new_ids(stored_state(path), baseline))
    assert states[0] == states[1]
    collection = states[0]["collections"]["new:collections:1"]
    assert collection["components"] == json.dumps(["new:components:1", "old1"])
    assert collection["collection_id"] == "new:collections:1"


def test_normalise_new_ids_leaves_substrings_alone(db_copy):
    baseline = (set(stored_state(db_copy)["component_types"]) - {"Chain"}) | {"c1"}
    insert(db_copy, "components", component_id="c1", component_name="Chain KMC X11", component_type="Chain")
    state = normalise_new_ids(stored_state(db_copy), baseline)
    assert "new:component_types:1" in state["component_types"]
    assert state["components"]["c1"]["component_name"] == "Chain KMC X11"
    assert state["components"]["c1"]["component_type"] == "new:component_types:1"
    assert "component_type" in state["components"]["c1"]


def test_normalise_new_ids_numbers_by_rowid_order(db_copy):
    baseline = set(stored_state(db_copy)["bikes"])
    insert(db_copy, "bikes", bike_id="zzz")
    insert(db_copy, "bikes", bike_id="aaa")
    bikes = normalise_new_ids(stored_state(db_copy), baseline)["bikes"]
    assert list(bikes)[-2:] == ["new:bikes:1", "new:bikes:2"]
    assert bikes["new:bikes:1"]["bike_id"] == "new:bikes:1"
