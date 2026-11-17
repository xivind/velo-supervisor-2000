# Tests

Automated tests for Velo Supervisor 2000. They pin what the app calculates and does today, so later changes can show they changed nothing by accident. CI runs them on every push and pull request (`.github/workflows/tests.yml`).

## Running

From the project root:

```bash
uv sync
uv run pytest -q
uv run pytest --cov=velo_supervisor --cov-report=term-missing
uv run ruff check && uv run ruff format --check
```

The full suite takes a few minutes. Lint covers `tests/` and `scripts/` only (`[tool.ruff]` in `pyproject.toml`); app modules join as Stage 4 rewrites them.

## Layout

```
tests/
    conftest.py          shared fixtures: fixed clock, synthetic dataset, app bound to it, snapshots, test client
    fixtures/
        dataset.py       synthetic dataset builder; its docstring lists every bike, component and case
        expected.py      assert_matches_expected: compare a result with an expected file
        expected/        expected-result files (recalculation.json and op_<name>.json deltas)
        strava/          synthetic Strava responses, written by hand from the API docs
    characterisation/    recalculation and every write operation against expected results
    rules/               business rules: every validate_* refusal, workplan, incident and service rules
    pages/               every GET page renders for every resource in the dataset
    strava/              Strava sync against fake_oauth.py and fixtures/strava
    integrity/           the extractor and comparison tools in scripts/integrity
    test_*.py            health, migration, config location, version, template database
```

`pythonpath = ["scripts"]` in `pyproject.toml` lets tests import `integrity.*` from `scripts/integrity`.

## Fixed clock

Every test runs with the clock frozen at `FIXED_NOW`, 2026-11-16 12:00 UTC (`scripts/integrity/clock.py`, applied by the autouse `clock` fixture through time-machine). Day-based values such as `lifetime_remaining_days` are therefore the same on every run. A test that needs another time uses `time_machine.travel` inside the test.

## Synthetic dataset

`fixtures/dataset.py` builds the dataset at test time from `config/template_db.sqlite` with all migrations applied, writing rows straight into the tables. All dates lie before `FIXED_NOW`. It holds no production data: the repository is public. `IDS` gives the fixed IDs of its records. The `recalculated` fixture loads the app against a fresh copy and runs the full recalculation; `app`, `snapshot_now`, `operation_delta` and `client` build on it.

## Expected results

- `fixtures/expected/recalculation.json` is the full stored and derived state after recalculating the dataset. It is the baseline: every operation test first asserts its "before" state equals it.
- `fixtures/expected/op_<name>.json` holds the delta an operation leaves: each changed, added or removed path with its `before` and `after` value (`scripts/integrity/delta.py`; `<absent>` marks a missing side). Floats are rounded to 6 decimals.
- Values were recorded once from the code, then checked by hand against the rules. Where the code is wrong, the file records what the code does and the test's docstring names the issue.

Rules for changing them:

- Tooling never overwrites an existing expected file. `assert_matches_expected` writes a file only when it is missing and `RECORD_EXPECTED=1` is set; otherwise a missing file fails the test.
- An expected file changes only through a documented behaviour change: delete it by hand, record it again with `RECORD_EXPECTED=1 uv run pytest <test>`, and state the reason (issue, feature) in the commit and pull request. Review the diff of the new file line by line.
- Never edit an expected file to make a test pass.

## Comparison against master

The extractor (`scripts/integrity/extract.py`) runs one checkout, flat `master` layout or package layout, against a copy of a database with the clock fixed, recalculates, and writes the stored and derived state as JSON. `compare.py` exports a git ref with `git archive`, extracts it and the working tree on the same database, and prints the differences:

```bash
uv run python scripts/integrity/compare.py --ref master --db <copy of production database> --out-dir <folder outside the repo>
```

Exit code 0 and "identical" means no difference. It also prints row counts per table and a "Present on both sides" list (recalculation failures and derived errors that are the same on both sides). Run it locally whenever a change touches the calculations. It uses real data, so neither the database nor its outputs are ever committed.
