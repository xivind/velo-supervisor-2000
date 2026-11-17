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


def new_id_map(state: dict, baseline_ids: set[str]) -> dict[str, str]:
    """Map each primary key absent from baseline_ids to new:<table>:<n>, numbered in row order"""
    new_ids = {}
    for table, rows in state.items():
        counter = 0
        for key in rows:
            if key not in baseline_ids:
                counter += 1
                new_ids[key] = f"new:{table}:{counter}"
    return new_ids


def _replace_text(text, new_ids):
    if text in new_ids:
        return new_ids[text]
    if text.startswith("["):
        try:
            items = json.loads(text)
        except ValueError:
            return text
        if isinstance(items, list) and any(isinstance(item, str) and item in new_ids for item in items):
            return json.dumps([new_ids.get(item, item) if isinstance(item, str) else item for item in items])
    return text


def replace_ids(value, new_ids: dict[str, str]):
    """Replace new IDs in dict keys and values, lists and tuples, at any depth.

    Only whole strings equal to a new ID, and whole elements of JSON-array strings, are
    replaced, never substrings.
    """
    if isinstance(value, str):
        return _replace_text(value, new_ids)
    if isinstance(value, dict):
        return {replace_ids(key, new_ids): replace_ids(item, new_ids) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_ids(item, new_ids) for item in value]
    if isinstance(value, tuple):
        return tuple(replace_ids(item, new_ids) for item in value)
    return value


def normalise_new_ids(state: dict, baseline_ids: set[str]) -> dict:
    """Replace primary keys absent from baseline_ids with new:<table>:<n>.

    Only whole values equal to a new ID, and whole elements of JSON-array strings
    such as collections.components, are replaced, never substrings. Dict keys change
    only for the rows of the table that owns the new ID.
    """
    new_ids = new_id_map(state, baseline_ids)
    return {table: {new_ids.get(key, key): {column: replace_ids(value, new_ids) for column, value in row.items()}
                    for key, row in rows.items()}
            for table, rows in state.items()}


def dumps(state: dict) -> str:
    """Serialise a state deterministically, keeping non-ASCII characters readable"""
    return json.dumps(state, sort_keys=True, ensure_ascii=False, indent=1)
