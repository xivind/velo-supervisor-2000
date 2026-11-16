import json
import re
import sqlite3
from pathlib import Path


def _normalise_value(value):
    if isinstance(value, float):
        return round(value, 6)
    return value


def stored_state(db_path: Path) -> dict[str, dict[str, dict]]:
    """Read every table and column straight from SQLite, keyed table, primary key, column"""
    connection = sqlite3.connect(db_path)
    try:
        tables = [row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        state = {}
        for table in tables:
            info = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
            columns = [row[1] for row in info]
            key_column = next((row[1] for row in info if row[5] == 1), None)
            rows = connection.execute(f'SELECT * FROM "{table}" ORDER BY rowid').fetchall()
            state[table] = {}
            for row in rows:
                record = {column: _normalise_value(value) for column, value in zip(columns, row)}
                key = record[key_column] if key_column else json.dumps(list(row), default=str)
                state[table][str(key)] = record
        return state
    finally:
        connection.close()


def normalise_new_ids(state: dict, baseline_ids: set[str]) -> dict:
    """Replace primary keys absent from baseline_ids with new:<table>:<n>, everywhere in the state"""
    mapping = {}
    for table, rows in state.items():
        counter = 0
        for key in rows:
            if key not in baseline_ids:
                counter += 1
                mapping[key] = f"new:{table}:{counter}"
    if not mapping:
        return state
    pattern = re.compile("|".join(re.escape(key) for key in sorted(mapping, key=len, reverse=True)))

    def replace(value):
        if isinstance(value, str):
            return pattern.sub(lambda match: mapping[match.group(0)], value)
        if isinstance(value, dict):
            return {replace(key): replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return value

    return replace(state)


def dumps(state: dict) -> str:
    """Serialise a state deterministically, keeping non-ASCII characters readable"""
    return json.dumps(state, sort_keys=True, ensure_ascii=False, indent=1)
