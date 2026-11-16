import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from integrity.clock import frozen_clock
from integrity.derived import derived_values
from integrity.loader import AppModules, load_app
from integrity.recalculate import recalculate
from integrity.snapshot import dumps, new_id_map, normalise_new_ids, replace_ids, stored_state


def extract(checkout: Path, db_path: Path,
            scenario: Callable[[AppModules], None] | None = None) -> dict:
    """Run one checkout against a copy of db_path and return its stored and derived state.

    The scenario runs after the baseline recalculation and is never followed by another
    full recalculation, so a wrong incremental update inside it stays visible.
    """
    with tempfile.TemporaryDirectory() as work:
        workdir = Path(work)
        db_copy = workdir / "db.sqlite"
        shutil.copy(db_path, db_copy)
        with frozen_clock():
            app = load_app(checkout, db_copy, workdir)
            failures = recalculate(app)
            baseline_ids = {key for rows in stored_state(db_copy).values() for key in rows}
            if scenario is not None:
                scenario(app)
            stored = stored_state(db_copy)
            return {"stored": normalise_new_ids(stored, baseline_ids),
                    "derived": replace_ids(derived_values(app), new_id_map(stored, baseline_ids)),
                    "recalculation_failures": failures}


def main():
    parser = argparse.ArgumentParser(description="Extract stored and derived state from a checkout")
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = extract(args.checkout.resolve(), args.db.resolve())
    args.out.write_text(dumps(result), encoding="utf-8")


if __name__ == "__main__":
    main()
