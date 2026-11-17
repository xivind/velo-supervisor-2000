ABSENT = "<absent>"


def _leaves(value, path, out):
    if isinstance(value, dict) and value:
        for key, item in value.items():
            key = str(key)
            if "/" in key:
                raise ValueError(f"Key {key!r} at {path!r} contains '/', which would make delta paths ambiguous")
            _leaves(item, f"{path}/{key}" if path else key, out)
    else:
        if value == ABSENT:
            raise ValueError(f"Value at {path!r} equals the absent marker {ABSENT!r}")
        out[path] = value
    return out


def snapshot_delta(before: dict, after: dict) -> dict:
    """Every leaf path that differs between two snapshots, as {path: {"before": x, "after": y}}.

    Paths join dict keys with '/'. Lists, tuples and empty dicts are single values, never
    compared element by element. A path missing on one side holds ABSENT there, so an added
    or removed None stays apart from a None that changed. Paths are sorted.
    """
    old, new = _leaves(before, "", {}), _leaves(after, "", {})
    return {
        path: {"before": old.get(path, ABSENT), "after": new.get(path, ABSENT)}
        for path in sorted(set(old) | set(new))
        if old.get(path, ABSENT) != new.get(path, ABSENT)
    }
