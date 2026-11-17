import pytest

from integrity.delta import ABSENT, snapshot_delta


def test_unchanged_snapshots_give_empty_delta():
    state = {"stored": {"bikes": {"b1": {"name": "Bike", "notes": None}}}}
    assert snapshot_delta(state, state) == {}


def test_changed_value():
    before = {"stored": {"bikes": {"b1": {"name": "Bike", "distance": 10}}}}
    after = {"stored": {"bikes": {"b1": {"name": "Bike", "distance": 25}}}}
    assert snapshot_delta(before, after) == {"stored/bikes/b1/distance": {"before": 10, "after": 25}}


def test_added_and_removed_rows_list_every_leaf():
    before = {"bikes": {"b1": {"name": "Old", "notes": "x"}}}
    after = {"bikes": {"b2": {"name": "New", "notes": "y"}}}
    assert snapshot_delta(before, after) == {
        "bikes/b1/name": {"before": "Old", "after": ABSENT},
        "bikes/b1/notes": {"before": "x", "after": ABSENT},
        "bikes/b2/name": {"before": ABSENT, "after": "New"},
        "bikes/b2/notes": {"before": ABSENT, "after": "y"}}


def test_list_is_one_value():
    before = {"collection": {"names": ["A", "B"]}}
    after = {"collection": {"names": ["A", "B", "C"]}}
    assert snapshot_delta(before, after) == {"collection/names": {"before": ["A", "B"], "after": ["A", "B", "C"]}}


def test_none_and_absent_stay_apart():
    before = {"row": {"kept_none": None, "dropped_none": None}}
    after = {"row": {"kept_none": 1, "added_none": None}}
    assert snapshot_delta(before, after) == {
        "row/added_none": {"before": ABSENT, "after": None},
        "row/dropped_none": {"before": None, "after": ABSENT},
        "row/kept_none": {"before": None, "after": 1}}


def test_empty_dict_is_a_value():
    assert snapshot_delta({"row": {"a": 1}}, {"row": {}}) == {
        "row": {"before": ABSENT, "after": {}},
        "row/a": {"before": 1, "after": ABSENT}}


def test_paths_are_sorted():
    delta = snapshot_delta({"b": 1, "a": {"z": 1, "y": 1}}, {"b": 2, "a": {"z": 2, "y": 2}})
    assert list(delta) == ["a/y", "a/z", "b"]


def test_key_with_slash_is_refused():
    with pytest.raises(ValueError, match="contains '/'"):
        snapshot_delta({"a/b": 1}, {})


def test_value_equal_to_marker_is_refused():
    with pytest.raises(ValueError, match="absent marker"):
        snapshot_delta({"a": ABSENT}, {})
