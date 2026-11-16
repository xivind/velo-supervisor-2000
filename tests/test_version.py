from importlib.metadata import PackageNotFoundError

from velo_supervisor import utils


def test_version_comes_from_package_metadata(monkeypatch):
    monkeypatch.setattr(utils, "version", lambda name: "1.2.3")
    assert utils.get_current_version() == "1.2.3"


def test_version_unknown_when_not_installed(monkeypatch):
    def missing(name):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(utils, "version", missing)
    assert utils.get_current_version() == "Version unknown"
