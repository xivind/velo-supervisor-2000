"""The starting database for new installs carries the approved component type defaults and no usage."""

import json
import sqlite3
from pathlib import Path

from fixtures.dataset import TEMPLATE_DB

DEFAULTS = Path(__file__).parent / "fixtures" / "component_type_defaults.json"


def template_types():
    connection = sqlite3.connect(f"file:{TEMPLATE_DB}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute("SELECT * FROM component_types ORDER BY component_type")]
    finally:
        connection.close()


def test_template_types_have_no_usage():
    assert [row["component_type"] for row in template_types() if row["in_use"] != 0] == []


def test_template_types_match_defaults():
    rows = [{key: value for key, value in row.items() if key != "in_use"} for row in template_types()]
    assert rows == json.loads(DEFAULTS.read_text())
