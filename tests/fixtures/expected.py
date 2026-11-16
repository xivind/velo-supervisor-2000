import os
from pathlib import Path

import pytest

from integrity.snapshot import dumps

EXPECTED_DIR = Path(__file__).resolve().parent / "expected"


def assert_matches_expected(name: str, result: dict) -> None:
    """Compare result with expected/<name>.json in snapshot.dumps format.

    A missing file is written only when RECORD_EXPECTED=1 and fails the test otherwise.
    An existing file is never written, so changing one means deleting it by hand.
    """
    path = EXPECTED_DIR / f"{name}.json"
    actual = dumps(result) + "\n"
    if not path.exists():
        if os.environ.get("RECORD_EXPECTED") == "1":
            path.write_text(actual, encoding="utf-8")
            return
        pytest.fail(f"Expected result {path} is missing; run with RECORD_EXPECTED=1 to record it")
    assert actual == path.read_text(encoding="utf-8"), f"Result differs from {path}"
