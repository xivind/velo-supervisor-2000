import shutil
import sqlite3
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DB = REPO_ROOT / "config" / "template_db.sqlite"


@pytest.fixture
def db_copy(tmp_path):
    path = tmp_path / "db.sqlite"
    shutil.copy(TEMPLATE_DB, path)
    return path


def insert(db_path, table, **values):
    connection = sqlite3.connect(db_path)
    columns = ", ".join(values)
    marks = ", ".join("?" for _ in values)
    connection.execute(f"INSERT INTO {table} ({columns}) VALUES ({marks})", list(values.values()))
    connection.commit()
    connection.close()
