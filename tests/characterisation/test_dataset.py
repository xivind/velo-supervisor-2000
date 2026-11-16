from dataclasses import astuple

from fixtures.dataset import IDS
from integrity.recalculate import recalculate
from integrity.snapshot import dumps


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
