from dataclasses import astuple

from fixtures.dataset import IDS
from integrity.recalculate import recalculate
from integrity.snapshot import dumps, stored_state


def test_dataset_builds_and_recalculates(app, snapshot_now):
    snapshot = snapshot_now()
    stored_keys = {key for rows in snapshot["stored"].values() for key in rows}
    assert set(astuple(IDS)) <= stored_keys
    assert not any(key.startswith("new:") for key in stored_keys)
    assert set(astuple(IDS)) & set(snapshot["derived"]["component"]) == {
        value for value in astuple(IDS) if value.startswith("comp-")}


def test_only_the_component_without_history_fails_recalculation(app, recalculation_failures):
    expected = [f"process_history_records:{IDS.comp_no_history}: No history records found for component: Spare saddle"]
    assert recalculation_failures == expected
    assert recalculate(app) == expected


def test_read_functions_raise_no_errors_on_the_dataset(app, snapshot_now):
    assert '"error"' not in dumps(snapshot_now()["derived"])


def test_component_name_keeps_norwegian_letters(app, snapshot_now):
    stored = snapshot_now()["stored"]
    assert stored["components"][IDS.comp_pads_norwegian]["component_name"] == "Bremseklosser bak æøå"


def test_new_ids_are_normalised_in_both_layers(app, snapshot_now):
    baseline = {key for rows in stored_state(app.db_path).values() for key in rows}
    success, _, component_id = app.business_logic.create_component(
        None, "Installed", "2026-11-01 08:00", "New chain", "Chain", IDS.bike_gravel,
        "3000", "500", "100", "", "", "", "300", 0, None)
    assert success
    new_ids = {key for rows in stored_state(app.db_path).values() for key in rows} - baseline
    assert component_id in new_ids and len(new_ids) == 2
    text = dumps(snapshot_now())
    assert not any(new_id in text for new_id in new_ids)
    assert "new:components:1" in text and "new:component_history:1" in text
