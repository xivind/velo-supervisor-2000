"""The Strava sync against synthetic Strava responses.

FakeOAuth2Session (fake_oauth.py) replaces requests_oauthlib.OAuth2Session in strava.py and
answers from tests/fixtures/strava. Page 1 of the activities holds November 2026 activities
newest first: rides on bike-road (60 km), bike-gravel (25 km, a GravelRide), the new
bike-touring (40 km) and without gear (12 km), plus a Run and a VirtualRide. Page 2 holds a
missed road ride of 70 km on 2026-06-25, a corrected copy of ride-gravel-2026-10 (22 km
instead of 20) and a Walk; page 3 is empty. Activities carry type and sport_type, as Strava
sends them. Strava IDs are integers; the corrected ride carries the dataset's
string ID so that it replaces the stored ride. Ride IDs that are not in the dataset show as new:rides:<n> in the
deltas, numbered in row order, and new bikes as new:bikes:<n>.
"""

import asyncio
import importlib
import json
import logging
import sys
from pathlib import Path

import pytest
from fixtures.dataset import IDS
from fixtures.expected import assert_matches_expected
from integrity.clock import FIXED_NOW
from integrity.snapshot import stored_state

from strava.fake_oauth import load_fixture, new_session_class

ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities?page={}&per_page=200"
REFRESH_URL = "https://www.strava.com/oauth/token"
GEAR_PREFIX = "https://www.strava.com/api/v3/gear/"
TOKEN = {
    "access_token": "synthetic-access-token",
    "refresh_token": "synthetic-refresh-token",
    "token_type": "Bearer",
    "client_id": "00000",
    "client_secret": "synthetic-client-secret",
}
PAGE1_RIDES = ["9100000004", "9100000003", "9100000001", "9100000002"]
PAGE2_RIDES = ["ride-gravel-2026-10", "9000000001"]
SPORT_TYPES = [
    ("Ride", True),
    ("MountainBikeRide", True),
    ("GravelRide", True),
    ("EBikeRide", False),
    ("EMountainBikeRide", False),
    ("VirtualRide", False),
    ("Velomobile", False),
    ("Handcycle", False),
]


def _write_token(path, expires_in):
    """Write a token file at path, expiring expires_in seconds after FIXED_NOW"""
    token = {**TOKEN, "expires_at": int(FIXED_NOW.timestamp()) + expires_in}
    Path(path).write_text(json.dumps(token), encoding="utf-8")


def _install(app, monkeypatch, refresh_error=None):
    session = new_session_class(refresh_error)
    monkeypatch.setattr(sys.modules[type(app.bl_module.strava).__module__], "OAuth2Session", session)
    return session


def _bare_strava(tmp_path, monkeypatch, activities):
    """A Strava instance without the app or dataset, behind a valid token, that receives activities as page 1"""
    module = importlib.import_module("velo_supervisor.strava")
    token_file = tmp_path / "strava_tokens.json"
    _write_token(token_file, 3600)
    monkeypatch.setattr(module, "OAuth2Session", new_session_class(activities=activities))
    return module.Strava(str(token_file))


def _sport_type_activity(sport_type):
    return next(activity for activity in load_fixture("sport_types") if activity["sport_type"] == sport_type)


def _urls(session):
    return [url for url, _ in session.calls]


def _gear_requested(session):
    return {url.removeprefix(GEAR_PREFIX).split("?")[0] for url in _urls(session) if url.startswith(GEAR_PREFIX)}


def _errors(caplog):
    return [record.getMessage() for record in caplog.records if record.levelno >= logging.ERROR]


@pytest.fixture
def session(app, monkeypatch):
    """A fake session behind a token that is valid for another hour"""
    _write_token(app.bl_module.strava.oauth_file, 3600)
    return _install(app, monkeypatch)


def test_all_mode_reads_every_page_until_empty(app, session, caplog):
    """Pages 1, 2 and 3 are requested; page 3 is empty and ends the loop. Only Ride activities
    are kept, in page order, and all mode collects no recent bikes.
    """
    strava = app.bl_module.strava
    asyncio.run(strava.get_rides("all"))
    assert _urls(session) == [ACTIVITIES_URL.format(page) for page in (1, 2, 3)]
    assert [ride["ride_id"] for ride in strava.payload_rides] == PAGE1_RIDES + PAGE2_RIDES
    assert strava.bike_ids_recent_rides == set()
    assert _errors(caplog) == []


def test_recent_mode_collects_bikes_from_rides_with_gear(app, session, caplog):
    """Only page 1 is requested. Bikes come from Ride activities with gear: the null gear ride,
    the Run's shoes and the VirtualRide on bike-road add nothing.
    """
    strava = app.bl_module.strava
    asyncio.run(strava.get_rides("recent"))
    assert _urls(session) == [ACTIVITIES_URL.format(1)]
    assert strava.bike_ids_recent_rides == {IDS.bike_road, IDS.bike_gravel, "bike-touring"}
    assert [ride["ride_id"] for ride in strava.payload_rides] == PAGE1_RIDES
    assert strava.payload_rides[2] == {
        "ride_id": "9100000001",
        "bike_id": IDS.bike_road,
        "ride_name": "Road ride",
        "record_time": "2026-11-10 12:00",
        "moving_time": "2:00:00",
        "ride_distance": 60.0,
        "commute": False,
    }
    assert _errors(caplog) == []


def test_ride_without_gear_is_stored(app, session):
    """A ride with gear_id null is stored with bike_id "None", as the dataset's ride-no-gear, and
    no gear is requested for it.
    """
    asyncio.run(app.business_logic.update_rides_bulk("recent"))
    assert stored_state(app.db_path)["rides"]["9100000004"] == {
        "ride_id": "9100000004",
        "bike_id": "None",
        "record_time": "2026-11-14 12:00",
        "ride_name": "Ride on a rental bike",
        "ride_distance": 12.0,
        "moving_time": "0:45:00",
        "commute": "True",
    }
    assert _gear_requested(session) == {IDS.bike_road, IDS.bike_gravel, "bike-touring"}


def test_activities_not_counted_are_skipped(app, session, caplog):
    """Activities whose sport_type is not counted are skipped with a warning naming it and never
    stored, VirtualRide included, even with a bike as gear. The Run's gear is not requested.
    """
    caplog.set_level(logging.WARNING)
    asyncio.run(app.business_logic.update_rides_bulk("all"))
    rides = stored_state(app.db_path)["rides"]
    assert not {"9100000005", "9100000006", "9000000002"} & set(rides)
    skipped = [record.getMessage() for record in caplog.records if record.getMessage().endswith("Skipping.")]
    assert skipped == [
        "Activity of sport type Run is not counted. Skipping.",
        "Activity of sport type VirtualRide is not counted. Skipping.",
        "Activity of sport type Walk is not counted. Skipping.",
    ]
    assert "g-shoes" not in _gear_requested(session)


@pytest.mark.parametrize("with_type", [True, False], ids=["with-type", "without-type"])
@pytest.mark.parametrize(("sport_type", "counted"), SPORT_TYPES)
def test_sport_type_decides_what_counts(tmp_path, monkeypatch, caplog, sport_type, counted, with_type):
    """Only Ride, MountainBikeRide and GravelRide count towards component distance (#12): they are
    kept as rides and their gear collected as a recent bike. EBikeRide, EMountainBikeRide,
    VirtualRide, Velomobile and Handcycle are left out, gear or not. The decision reads
    sport_type alone, so it holds when Strava stops sending the deprecated type.
    """
    activity = _sport_type_activity(sport_type)
    if not with_type:
        activity = {key: value for key, value in activity.items() if key != "type"}
    strava = _bare_strava(tmp_path, monkeypatch, [activity])
    asyncio.run(strava.get_rides("recent"))
    assert _errors(caplog) == []
    if counted:
        assert [ride["ride_id"] for ride in strava.payload_rides] == [activity["id_str"]]
        assert strava.bike_ids_recent_rides == {activity["gear_id"]}
    else:
        assert strava.payload_rides == []
        assert strava.bike_ids_recent_rides == set()


def test_64_bit_activity_id_is_kept_exactly(tmp_path, monkeypatch):
    """Strava activity IDs may exceed 2**53 from 2027-06-01 (#12). The trail ride's ID is 2**53 + 1,
    the first integer a double cannot hold. Python parses JSON integers exactly, so ride_id
    holds the same digits as Strava's id_str, and the rides table stores it as text.
    """
    activity = _sport_type_activity("MountainBikeRide")
    strava = _bare_strava(tmp_path, monkeypatch, [activity])
    asyncio.run(strava.get_rides("all"))
    assert activity["id"] == 2**53 + 1
    assert strava.payload_rides[0]["ride_id"] == activity["id_str"] == "9007199254740993"


def test_expired_token_is_refreshed_and_saved(app, monkeypatch, caplog):
    """A token that expired a minute ago is refreshed once with the stored refresh token and the
    client credentials. The token file then holds the whole refresh response (expires_in
    included) plus the client credentials, and the activities are fetched with the new token.
    """
    _write_token(app.bl_module.strava.oauth_file, -60)
    session = _install(app, monkeypatch)
    strava = app.bl_module.strava
    asyncio.run(strava.get_rides("recent"))
    assert session.refreshes == [
        (REFRESH_URL, "synthetic-refresh-token", {"client_id": "00000", "client_secret": "synthetic-client-secret"})
    ]
    saved = json.loads(Path(strava.oauth_file).read_text(encoding="utf-8"))
    assert saved == {**load_fixture("token_refresh"), "client_id": "00000", "client_secret": "synthetic-client-secret"}
    assert session.calls == [(ACTIVITIES_URL.format(1), "synthetic-access-token-refreshed")]
    assert len(strava.payload_rides) == 4
    assert _errors(caplog) == []


def test_failed_refresh_is_logged_and_the_old_token_used(app, monkeypatch, caplog):
    """When the refresh raises, the error is logged, the token file is left as it was and the
    activities are still requested with the expired token.
    """
    _write_token(app.bl_module.strava.oauth_file, -60)
    before = Path(app.bl_module.strava.oauth_file).read_text(encoding="utf-8")
    session = _install(app, monkeypatch, refresh_error=ConnectionError("synthetic outage"))
    asyncio.run(app.bl_module.strava.get_rides("recent"))
    assert _errors(caplog) == ["An error occurred refreshing tokens: synthetic outage."]
    assert Path(app.bl_module.strava.oauth_file).read_text(encoding="utf-8") == before
    assert session.calls == [(ACTIVITIES_URL.format(1), "synthetic-access-token")]


def test_refresh_all_bikes_merges_athlete_and_known_bikes(app, session, caplog):
    """Gear is requested for the bikes in the rides table (road, gravel, retired) and the bikes on
    the athlete profile (road, gravel, touring), so bike-retired comes from the rides alone and
    bike-touring, with no rides yet, from the profile alone. bike-touring is inserted with
    service status "No components registered"; known bikes keep their status and get the
    Strava name, retired flag, distance and description. A null description is stored as the
    text "None".

    The profile holds one bike the rides table lacks, not two: get_bikes inserts new bikes in
    set order, which varies between runs, so two would swap new:bikes labels in op_strava_all.
    """
    result = asyncio.run(app.business_logic.refresh_all_bikes())
    assert result == (True, "Records for 4 bikes updated.")
    assert _gear_requested(session) == {IDS.bike_road, IDS.bike_gravel, IDS.bike_retired, "bike-touring"}
    bikes = stored_state(app.db_path)["bikes"]
    assert bikes["bike-touring"] == {
        "bike_id": "bike-touring",
        "bike_name": "Touring bike",
        "bike_retired": "False",
        "service_status": "No components registered",
        "total_distance": 40.0,
        "notes": "Bought 2026-11",
    }
    assert bikes[IDS.bike_gravel]["notes"] == "None"
    assert bikes[IDS.bike_road]["total_distance"] == 1230.0
    assert _errors(caplog) == []


def test_recent_mode(app, session, operation_delta, caplog):
    """update_rides_bulk("recent"): the four page 1 rides are stored and the three bikes ridden are
    refreshed and recalculated; bike-touring (new:bikes:1) has no components.

    bike-road gains 60 km on 2026-11-10. Cassette 1100 + 60 = 1160, lifetime remaining 4840,
    service next 1000 - (9 x 50 + 60) = 490. Rear wheel 1000 offset + 20 x 50 + 60 = 2060,
    remaining 7940, service next 2000 - 1060 = 940. Chain 790 + 60 = 850, remaining 2150,
    service next 500 - (100 + 350 + 60) = -10: Due for service becomes Service interval
    exceeded and bike-road needs attention. bike-gravel gains 25 km: pads 465 (remaining
    1035), tire 245. Bike distances and the null gravel description come from the gear.
    """
    result = asyncio.run(app.business_logic.update_rides_bulk("recent"))
    assert result == (True, "Update of rides, bikes and components successful: Processed components for 3 bikes.")
    assert _errors(caplog) == []
    assert_matches_expected("op_strava_recent", operation_delta())


def test_all_mode(app, session, operation_delta, caplog):
    """update_rides_bulk("all"): rides from pages 1 and 2 are stored, every known and athlete bike
    is refreshed, and the components of every bike in the rides table are recalculated.

    As op_strava_recent plus the 70 km road ride of 2026-06-25 and ride-gravel-2026-10 replaced
    (22 km, renamed). Cassette 1230 (remaining 4770, service next 1000 - 580 = 420), rear wheel
    2130 (remaining 7870, service next 870), chain 920 (remaining 2080, service next -80).
    Gravel pads 440 - 20 + 22 + 25 = 467 (remaining 1033), tire 247.
    """
    result = asyncio.run(app.business_logic.update_rides_bulk("all"))
    assert result == (True, "Update of rides, bikes and components successful: Processed components for 4 bikes.")
    assert _errors(caplog) == []
    assert_matches_expected("op_strava_all", operation_delta())
