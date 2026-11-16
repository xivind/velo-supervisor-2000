from integrity.compare import diff, present_on_both_sides


def snapshot(**overrides):
    state = {"components": {"c1": {"service_status": "OK", "component_name": "Chain"},
                            "c2": {"service_status": "OK", "component_name": "Tyre"}},
             "bikes": {"b1": {"bike_name": "Bike"}}}
    state.update(overrides)
    return state


def test_identical_snapshots_have_no_diff():
    assert diff(snapshot(), snapshot()) == []


def test_changed_value_is_reported_with_path():
    right = snapshot()
    right["components"]["c2"]["service_status"] = "Due"
    lines = diff(snapshot(), right)
    assert len(lines) == 1
    assert "components" in lines[0] and "c2" in lines[0] and "service_status" in lines[0]
    assert "left='OK'" in lines[0] and "right='Due'" in lines[0]


def test_missing_table_and_row_are_reported():
    left = snapshot(workplans={"w1": {"title": "Plan"}})
    right = snapshot()
    right["bikes"]["b2"] = {"bike_name": "Other"}
    lines = diff(left, right)
    assert any("workplans" in line and "only in left" in line for line in lines)
    assert any("bikes/b2" in line and "only in right" in line for line in lines)


def test_present_on_both_sides_covers_failures_and_both_error_shapes():
    derived = {"overview": {"bike_overview": {"error": "ValueError: x"}},
               "bike": {"b1": {"overview_row": {"a": 1}, "error": "KeyError: y"}}}
    side = {"recalculation_failures": ["step:1: failed"], "derived": derived}
    other = {"recalculation_failures": ["step:1: failed", "step:2: only"],
             "derived": {**derived, "bike": {"b1": {"error": "KeyError: y", "overview_row": {}}}}}
    lines = present_on_both_sides(side, other)
    assert "recalculation_failures: step:1: failed" in lines
    assert "derived/overview/bike_overview: ValueError: x" in lines
    assert "derived/bike/b1: KeyError: y" in lines
    assert len(lines) == 3
