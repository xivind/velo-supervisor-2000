import json

import pytest

from velo_supervisor import utils


def test_read_config_uses_env_path(tmp_path, monkeypatch):
    path = tmp_path / "elsewhere.json"
    path.write_text(json.dumps({"marker": "env"}))
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", str(path))
    assert utils.read_config() == {"marker": "env"}


def test_read_config_defaults_to_working_directory(tmp_path, monkeypatch):
    (tmp_path / "config.json").write_text(json.dumps({"marker": "cwd"}))
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VELO_SUPERVISOR_CONFIG", raising=False)
    assert utils.read_config() == {"marker": "cwd"}


def test_empty_env_value_is_treated_as_unset(tmp_path, monkeypatch):
    (tmp_path / "config.json").write_text(json.dumps({"marker": "cwd"}))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", "")
    assert utils.read_config() == {"marker": "cwd"}


def test_write_config_writes_to_env_path(tmp_path, monkeypatch):
    path = tmp_path / "written.json"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", str(path))
    success, _ = utils.write_config("system_settings", verbose_logging=True)
    assert success
    assert json.loads(path.read_text())["verbose_logging"] is True
    assert not (tmp_path / "config.json").exists()


def test_missing_config_error_names_path(tmp_path, monkeypatch):
    path = tmp_path / "missing.json"
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", str(path))
    with pytest.raises(FileNotFoundError, match="missing.json"):
        utils.read_config()
