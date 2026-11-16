import importlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Literal

FLAT_MODULES = ("main", "business_logic", "database_manager", "database_model",
                "utils", "strava", "middleware", "scheduler", "db_migration")


@dataclass
class AppModules:
    layout: str
    business_logic: Any
    bl_module: Any
    database_manager: Any
    utils: Any
    db_path: Path


def detect_layout(checkout: Path) -> Literal["flat", "package"]:
    """Tell the pre-restructure flat layout from the package layout"""
    if (checkout / "backend" / "business_logic.py").exists():
        return "flat"
    if (checkout / "src" / "velo_supervisor" / "business_logic.py").exists():
        return "package"
    raise ValueError(f"No known application layout in {checkout}")


def _forget_app_modules():
    for name in list(sys.modules):
        if name in FLAT_MODULES or name == "velo_supervisor" or name.startswith("velo_supervisor."):
            del sys.modules[name]


def load_app(checkout: Path, db_path: Path, workdir: Path) -> AppModules:
    """Import the application from a checkout bound to db_path.

    The application reads config.json from the working directory at import time,
    so this changes cwd, VELO_SUPERVISOR_CONFIG and sys.path and does not restore
    them. Callers isolate that, for example with pytest's monkeypatch.
    """
    layout = detect_layout(checkout)
    workdir.mkdir(parents=True, exist_ok=True)
    config = {"db_path": str(db_path),
              "strava_tokens": str(workdir / "strava_tokens.json"),
              "verbose_logging": False}
    (workdir / "config.json").write_text(json.dumps(config), encoding="utf-8")
    os.chdir(workdir)
    os.environ["VELO_SUPERVISOR_CONFIG"] = str(workdir / "config.json")
    _forget_app_modules()
    source_root = checkout / ("backend" if layout == "flat" else "src")
    sys.path.insert(0, str(source_root))
    prefix = "" if layout == "flat" else "velo_supervisor."
    utils = importlib.import_module(f"{prefix}utils")
    bl_module = importlib.import_module(f"{prefix}business_logic")
    app_state = SimpleNamespace(strava_last_pull=None,
                                strava_days_since_last_pull=None,
                                db_path=str(db_path))
    return AppModules(layout=layout,
                      business_logic=bl_module.BusinessLogic(app_state),
                      bl_module=bl_module,
                      database_manager=bl_module.database_manager,
                      utils=utils,
                      db_path=db_path)
