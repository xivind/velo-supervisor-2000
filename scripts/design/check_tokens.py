"""Check the colour tokens of the design profile for contrast (WCAG 2.1).

Usage: uv run python scripts/design/check_tokens.py <tokens.json>
Prints one line per failing pair and exits 1 if any fail.
"""

import json
import sys
from pathlib import Path

STATUSES = ["ok", "due", "exceeded", "undefined", "retired"]
TOLD_APART = ["status-ok", "status-due", "status-exceeded"]

PAIRS: list[tuple[str, str, float]] = [
    ("ink", "surface", 4.5),
    ("ink", "surface-raised", 4.5),
    ("ink", "accent-tint", 4.5),
    ("ink-muted", "surface", 4.5),
    ("ink-muted", "surface-raised", 4.5),
    ("on-accent", "accent", 4.5),
    ("accent", "surface", 3.0),
    *[(f"status-{s}-text", f"status-{s}-tint", 4.5) for s in STATUSES],
    *[(a, b, 1.3) for i, a in enumerate(TOLD_APART) for b in TOLD_APART[i + 1 :]],
]


def _luminance(colour: str) -> float:
    hex_value = colour.lstrip("#")
    if len(hex_value) == 3:
        hex_value = "".join(c * 2 for c in hex_value)
    channels = [int(hex_value[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(a: str, b: str) -> float:
    """WCAG 2.1 contrast ratio of two hex colours, from 1 to 21."""
    light, dark = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def _colours(tokens: dict) -> dict[str, str]:
    """Light-theme value per colour token, with aliases ("{other-token}") resolved."""
    raw = {}
    for token in tokens.get("color", {}).get("tokens", []):
        value = token["value"]
        raw[token["name"]] = value.get("light") if isinstance(value, dict) else value
    resolved = {}
    for name, value in raw.items():
        seen = {name}
        while isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            target = value[1:-1]
            if target in seen or target not in raw:
                value = None
                break
            seen.add(target)
            value = raw[target]
        if value:
            resolved[name] = value
    return resolved


def check(tokens: dict) -> list[str]:
    """One message per failing pair ("<fg>/<bg>: <ratio> < <minimum>") or missing token."""
    colours = _colours(tokens)
    messages = []
    for name in dict.fromkeys(n for fg, bg, _ in PAIRS for n in (fg, bg)):
        if name not in colours:
            messages.append(f"missing {name}")
    for fg, bg, minimum in PAIRS:
        if fg in colours and bg in colours:
            ratio = contrast_ratio(colours[fg], colours[bg])
            if ratio < minimum:
                messages.append(f"{fg}/{bg}: {ratio:.2f} < {minimum}")
    return messages


def main() -> None:
    messages = check(json.loads(Path(sys.argv[1]).read_text()))
    for message in messages:
        print(message)
    sys.exit(1 if messages else 0)


if __name__ == "__main__":
    main()
