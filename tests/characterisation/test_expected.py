import pytest
from fixtures import expected


@pytest.fixture
def expected_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(expected, "EXPECTED_DIR", tmp_path)
    monkeypatch.delenv("RECORD_EXPECTED", raising=False)
    return tmp_path


def test_missing_file_fails_naming_record_expected(expected_dir):
    with pytest.raises(pytest.fail.Exception, match="RECORD_EXPECTED=1"):
        expected.assert_matches_expected("case", {"a": 1})
    assert not (expected_dir / "case.json").exists()


def test_missing_file_is_recorded_when_asked(expected_dir, monkeypatch):
    monkeypatch.setenv("RECORD_EXPECTED", "1")
    expected.assert_matches_expected("case", {"name": "æøå", "b": [1, 2]})
    assert (expected_dir / "case.json").read_text(encoding="utf-8") == (
        '{\n "b": [\n  1,\n  2\n ],\n "name": "æøå"\n}\n'
    )
    expected.assert_matches_expected("case", {"b": [1, 2], "name": "æøå"})


def test_difference_fails(expected_dir):
    (expected_dir / "case.json").write_text('{\n "a": 1\n}\n', encoding="utf-8")
    with pytest.raises(AssertionError):
        expected.assert_matches_expected("case", {"a": 2})


def test_existing_file_is_never_overwritten(expected_dir, monkeypatch):
    monkeypatch.setenv("RECORD_EXPECTED", "1")
    (expected_dir / "case.json").write_text('{\n "a": 1\n}\n', encoding="utf-8")
    with pytest.raises(AssertionError):
        expected.assert_matches_expected("case", {"a": 2})
    assert (expected_dir / "case.json").read_text(encoding="utf-8") == '{\n "a": 1\n}\n'
