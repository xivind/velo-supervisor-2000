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
    """Replace primary keys absent from baseline_ids with new:<table>:<n>.

    Only whole values equal to a new ID, and whole elements of JSON-array strings
    such as collections.components, are replaced, never substrings. Dict keys change
    only for the rows of the table that owns the new ID.
    """
    mapping = {}
    for table, rows in state.items():
        counter = 0
        for key in rows:
            if key not in baseline_ids:
                counter += 1
                mapping[(table, key)] = f"new:{table}:{counter}"
    new_ids = {key: value for (_, key), value in mapping.items()}

    def replace_text(text):
        if text in new_ids:
            return new_ids[text]
        if text.startswith("["):
            try:
                items = json.loads(text)
            except ValueError:
                return text
            if isinstance(items, list) and any(isinstance(item, str) and item in new_ids for item in items):
                return json.dumps([new_ids.get(item, item) if isinstance(item, str) else item
                                   for item in items])
        return text

    normalised = {}
    for table, rows in state.items():
        normalised[table] = {}
        for key, row in rows.items():
            new_key = mapping.get((table, key), key)
            normalised[table][new_key] = {column: replace_text(value) if isinstance(value, str) else value
                                          for column, value in row.items()}
    return normalised


def dumps(state: dict) -> str:
    """Serialise a state deterministically, keeping non-ASCII characters readable"""
    return json.dumps(state, sort_keys=True, ensure_ascii=False, indent=1)
