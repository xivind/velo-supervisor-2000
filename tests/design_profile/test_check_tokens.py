from design.check_tokens import PAIRS, check, contrast_ratio

VALID = {
    "surface": "#ffffff",
    "surface-raised": "#f4f5f7",
    "ink": "#1b1f24",
    "ink-muted": "#57606a",
    "line": "#d0d7de",
    "accent": "#c2410c",
    "on-accent": "#ffffff",
    "accent-tint": "#fff1e6",
    "status-ok": "#1a7f37",
    "status-ok-tint": "#e6f6ea",
    "status-due": "#8a4b00",
    "status-due-tint": "#fff4d6",
    "status-exceeded": "#7a0e1c",
    "status-exceeded-tint": "#ffebe9",
    "status-undefined": "#57606a",
    "status-undefined-tint": "#eef0f2",
    "status-retired": "#4b5159",
    "status-retired-tint": "#e8eaed",
}


def tokens_with(**overrides):
    """A minimal tokens.json in the design system's list shape, valid unless overridden."""
    values = {**VALID, **overrides}
    return {
        "name": "Test",
        "version": 1,
        "color": {
            "themes": [{"id": "light", "name": "Light"}],
            "tokens": [{"name": name, "value": {"light": value}, "usage": ""} for name, value in values.items()],
        },
    }


def test_contrast_ratio_black_on_white():
    assert round(contrast_ratio("#000000", "#ffffff"), 1) == 21.0


def test_check_reports_failing_pair():
    tokens = tokens_with(ink="#777777", surface="#ffffff")
    assert any("ink/surface" in m for m in check(tokens))


def test_check_passes_valid_profile():
    assert check(tokens_with()) == []


def test_status_colours_must_differ_in_lightness():
    tokens = tokens_with(**{"status-ok": "#1a7f37", "status-due": "#1b7f38"})
    assert any("status-ok/status-due" in m for m in check(tokens))


def test_check_resolves_alias():
    tokens = tokens_with(**{"on-accent": "{surface}"})
    assert not any("on-accent" in m for m in check(tokens))


def test_check_reports_missing_token():
    tokens = tokens_with()
    tokens["color"]["tokens"] = [t for t in tokens["color"]["tokens"] if t["name"] != "accent"]
    assert "missing accent" in check(tokens)


def test_check_reads_plain_string_value():
    tokens = tokens_with()
    for token in tokens["color"]["tokens"]:
        token["value"] = token["value"]["light"]
    assert check(tokens) == []


def test_pairs_cover_every_status():
    names = {fg for fg, _, _ in PAIRS}
    assert {"status-ok", "status-due", "status-exceeded", "status-undefined", "status-retired"} <= names
