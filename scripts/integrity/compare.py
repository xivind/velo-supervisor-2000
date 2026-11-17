import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACT_SCRIPT = Path(__file__).resolve().with_name("extract.py")


def diff(left, right, path: str = "") -> list[str]:
    """One line per difference as 'path: left=... right=...', paths joined with '/'"""
    if isinstance(left, dict) and isinstance(right, dict):
        lines = []
        for key in sorted(set(left) | set(right), key=str):
            child = f"{path}/{key}" if path else str(key)
            if key not in right:
                lines.append(f"{child}: only in left")
            elif key not in left:
                lines.append(f"{child}: only in right")
            else:
                lines.extend(diff(left[key], right[key], child))
        return lines
    if left != right:
        return [f"{path}: left={left!r} right={right!r}"]
    return []


def _error_paths(node, path=""):
    if isinstance(node, dict):
        if isinstance(node.get("error"), str):
            yield path, node["error"]
        for key, value in node.items():
            if key != "error":
                yield from _error_paths(value, f"{path}/{key}" if path else str(key))


def present_on_both_sides(left: dict, right: dict) -> list[str]:
    """Recalculation failures and derived error entries that appear identically on both sides"""
    lines = [
        f"recalculation_failures: {line}"
        for line in left.get("recalculation_failures", [])
        if line in right.get("recalculation_failures", [])
    ]
    right_errors = set(_error_paths(right.get("derived", {})))
    lines += [
        f"derived/{path}: {message}"
        for path, message in _error_paths(left.get("derived", {}))
        if (path, message) in right_errors
    ]
    return lines


def rows_per_table(state: dict) -> dict[str, int]:
    return {table: len(rows) for table, rows in state.get("stored", {}).items()}


def _run_extract(checkout: Path, db: Path, out: Path):
    subprocess.run(
        [sys.executable, str(EXTRACT_SCRIPT), "--checkout", str(checkout), "--db", str(db), "--out", str(out)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a git ref against the working tree")
    parser.add_argument("--ref", required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        out_dir = args.out_dir or Path(temp) / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        export = Path(temp) / "export"
        export.mkdir()
        archive = subprocess.run(["git", "archive", args.ref], cwd=REPO_ROOT, check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(export)], input=archive, check=True)
        left_out, right_out = out_dir / "left.json", out_dir / "right.json"
        _run_extract(export, args.db, left_out)
        _run_extract(REPO_ROOT, args.db, right_out)
        left = json.loads(left_out.read_text(encoding="utf-8"))
        right = json.loads(right_out.read_text(encoding="utf-8"))
    differences = diff(left, right)
    for line in differences:
        print(line)
    print(f"\nCompared {args.ref} (left) with working tree (right); outputs in {out_dir}")
    left_counts, right_counts = rows_per_table(left), rows_per_table(right)
    for table in sorted(set(left_counts) | set(right_counts)):
        print(f"  {table}: left={left_counts.get(table, 0)} right={right_counts.get(table, 0)}")
    print(f"{len(differences)} differences" if differences else "identical")
    both = present_on_both_sides(left, right)
    print("\nPresent on both sides:")
    print("\n".join(f"  {line}" for line in both) if both else "  none")
    return 1 if differences else 0


if __name__ == "__main__":
    sys.exit(main())
