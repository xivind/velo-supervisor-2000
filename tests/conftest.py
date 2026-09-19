"""Shared fixtures: every test gets its own copy of the template database"""

import os
import sys
import json
import shutil
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
TEMPLATE_DB = os.path.join(BACKEND_DIR, "template_db.sqlite")


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Copy template db to tmp dir, write config.json there, chdir into it"""
    db_path = tmp_path / "test_db.sqlite"
    shutil.copy(TEMPLATE_DB, db_path)
    config = {"db_path": str(db_path),
              "strava_tokens": str(tmp_path / "strava_tokens.json"),
              "verbose_logging": False}
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    return {"db_path": str(db_path), "tmp_path": tmp_path}


@pytest.fixture
def migrated_env(app_env):
    """Run db_migration against the copied template db so the schema is current"""
    import db_migration
    conn = db_migration.sqlite3.connect(app_env["db_path"])
    cursor = conn.cursor()
    db_migration.run_all_migrations(cursor, conn)
    conn.close()
    return app_env


@pytest.fixture
def modules(migrated_env):
    """Fresh imports of the app modules bound to the test database"""
    for name in ["database_model", "database_manager", "utils", "business_logic"]:
        sys.modules.pop(name, None)
    import utils
    import database_model
    import business_logic
    from types import SimpleNamespace
    return SimpleNamespace(utils=utils,
                           database_model=database_model,
                           database_manager=business_logic.database_manager,
                           business_logic=business_logic.BusinessLogic(SimpleNamespace()))
