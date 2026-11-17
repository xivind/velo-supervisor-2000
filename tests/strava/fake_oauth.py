"""A stand-in for requests_oauthlib.OAuth2Session that answers from tests/fixtures/strava.

Routing by URL:
- /api/v3/athlete/activities?page=N: activities_page<N>.json, or activities_empty.json when
  that page has no file
- /api/v3/athlete: athlete.json
- /api/v3/gear/<id>: gear_<id>.json
- refresh_token(): token_refresh.json, or raises refresh_error when it is set

Any other URL, or gear without a file, raises LookupError, which strava.py catches and logs as
an error. Subclass per test (see new_session_class) so calls and refreshes start empty.
"""

import json
from pathlib import Path
from typing import ClassVar
from urllib.parse import parse_qs, urlparse

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "strava"
API_PREFIX = "/api/v3/"


def load_fixture(name):
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


class FakeResponse:
    def __init__(self, payload, status_code=200, reason="OK"):
        self.payload = payload
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return self.payload


class FakeOAuth2Session:
    calls: ClassVar[list] = []
    refreshes: ClassVar[list] = []
    refresh_error = None

    def __init__(self, client_id, token=None):
        self.client_id = client_id
        self.token = dict(token or {})

    def get(self, url):
        self.calls.append((url, self.token.get("access_token")))
        return FakeResponse(load_fixture(self._route(url)))

    def refresh_token(self, token_url, refresh_token=None, **kwargs):
        self.refreshes.append((token_url, refresh_token, kwargs))
        if self.refresh_error:
            raise self.refresh_error
        return load_fixture("token_refresh")

    @staticmethod
    def _route(url):
        parsed = urlparse(url)
        path = parsed.path.removeprefix(API_PREFIX)
        if path == "athlete/activities":
            page = parse_qs(parsed.query)["page"][0]
            name = f"activities_page{page}"
            return name if (FIXTURES / f"{name}.json").exists() else "activities_empty"
        if path == "athlete":
            return "athlete"
        if path.startswith("gear/") and (FIXTURES / f"gear_{path.removeprefix('gear/')}.json").exists():
            return f"gear_{path.removeprefix('gear/')}"
        raise LookupError(f"No synthetic Strava response for {url}")


def new_session_class(refresh_error=None):
    """A FakeOAuth2Session subclass with its own empty call records"""
    return type(
        "FakeOAuth2Session", (FakeOAuth2Session,), {"calls": [], "refreshes": [], "refresh_error": refresh_error}
    )
