"""Characterisation of the full recalculation on the synthetic dataset.

Every value below is worked out by hand from tests/fixtures/dataset.py and the code as
it is today. Tests that need rows the dataset lacks insert them into the test's own
database and recalculate again, so the shared expected file stays recorded from the
untouched dataset.
"""

import json
import sqlite3

from fixtures.dataset import IDS, component, history, service
from fixtures.expected import assert_matches_expected
from integrity.derived import derived_values
from integrity.recalculate import recalculate
from integrity.snapshot import stored_state

NO_HISTORY_FAILURE = (
    f"process_history_records:{IDS.comp_no_history}: No history records found for component: Spare saddle"
)
UNBOUND_STATUS = "cannot access local variable 'service_status' where it is not associated with a value"


def _insert(app, table, rows):
    connection = sqlite3.connect(app.db_path)
    try:
        columns = list(rows[0])
        connection.executemany(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
            [[row[column] for column in columns] for row in rows],
        )
        connection.commit()
    finally:
        connection.close()


def _bike(bike_id, name):
    return {
        "bike_id": bike_id,
        "bike_name": name,
        "bike_retired": "False",
        "service_status": None,
        "total_distance": 0.0,
        "notes": None,
    }


def _ride(ride_id, bike_id, record_time, distance):
    return {
        "ride_id": ride_id,
        "bike_id": bike_id,
        "record_time": record_time,
        "ride_name": ride_id,
        "ride_distance": distance,
        "moving_time": "1:00:00",
        "commute": "False",
    }


def _stored(app):
    return stored_state(app.db_path)


def test_recalculation_matches_expected(snapshot_now):
    assert_matches_expected("recalculation", snapshot_now())


def test_second_recalculation_changes_nothing(app, snapshot_now):
    """A recalculation on already recalculated data leaves every stored and derived value as it was"""
    before = snapshot_now()
    assert recalculate(app) == [NO_HISTORY_FAILURE]
    assert snapshot_now() == before


def test_moved_component_distance_sums_rides_on_both_bikes(app):
    """Chain distance counts road rides while on road and gravel rides while on gravel.

    History markers (sum of rides on the record's bike from the previous Installed record):
    road_1 2025-01-01: 0
    off_road 2025-07-01: 0 + road Jan..Jun 2025, 6 x 50 = 300
    gravel 2025-08-01: 300 (previous record is Not installed, nothing added)
    off_gravel 2026-03-01: 300 + gravel Aug 2025..Feb 2026, 7 x 20 = 440
    road_2 2026-04-01: 440
    Distance: 440 + road Apr..Oct 2026, 7 x 50 = 790; lifetime remaining 3000 - 790 = 2210, OK
    (threshold 100). The road ride on 2025-07-10 and the gravel ride on 2026-03-20 fall in
    the months off and do not count.
    """
    stored = _stored(app)
    markers = {
        history_id: stored["component_history"][history_id]["distance_marker"]
        for history_id in (
            IDS.hist_chain_road_1,
            IDS.hist_chain_off_road,
            IDS.hist_chain_gravel,
            IDS.hist_chain_off_gravel,
            IDS.hist_chain_road_2,
        )
    }
    assert markers == {
        IDS.hist_chain_road_1: 0,
        IDS.hist_chain_off_road: 300,
        IDS.hist_chain_gravel: 300,
        IDS.hist_chain_off_gravel: 440,
        IDS.hist_chain_road_2: 440,
    }
    chain = stored["components"][IDS.comp_chain_moved]
    assert (chain["component_distance"], chain["lifetime_remaining"], chain["lifetime_status"]) == (790, 2210, "OK")
    assert (chain["bike_id"], chain["installation_status"], chain["updated_date"]) == (
        IDS.bike_road,
        "Installed",
        "2026-04-01 08:00",
    )


def test_offset_added_to_distance(app):
    """The distance offset counts for lifetime, not for the service interval.

    Rear wheel on road since 2025-03-01: Mar 2025..Oct 2026, 20 x 50 = 1000 km ridden.
    Distance 1000 + offset 1000 = 2000; lifetime remaining 10000 - 2000 = 8000, OK (threshold 200).
    No completed service, so distance since service is the ridden 1000 without the offset:
    service next 2000 - 1000 = 1000, OK. The planned service (svc-wheel-planned) does not reset
    the interval and keeps no distance marker or bike.
    """
    stored = _stored(app)
    wheel = stored["components"][IDS.comp_wheel_offset]
    assert (wheel["component_distance"], wheel["lifetime_remaining"], wheel["lifetime_status"]) == (2000, 8000, "OK")
    assert (wheel["service_next"], wheel["service_status"]) == (1000, "OK")
    planned = stored["services"][IDS.svc_wheel_planned]
    assert (planned["distance_marker"], planned["bike_id"], planned["status"]) == (None, None, "Planned")


def test_no_history_uses_alternate_method(app, recalculation_failures):
    """A component without installation history keeps the values the alternate method gives it.

    Spare saddle is not installed, so the distance iterator skips it, process_history_records
    fails on it (the one expected failure) and it tracks no days, so update_time_based_fields
    skips it too. Its stored values are those of update_component_lifetime_service_alternate:
    distance 300 (offset), lifetime remaining 20000 - 300 = 19700, OK (threshold 200), no service
    interval so service next None and "Not defined". Running the alternate method again changes
    nothing.
    """
    assert recalculation_failures == [NO_HISTORY_FAILURE]
    fields = (
        "component_distance",
        "lifetime_remaining",
        "lifetime_status",
        "service_next",
        "service_status",
        "lifetime_remaining_days",
        "service_next_days",
    )
    expected = (300, 19700, "OK", None, "Not defined", None, None)
    saddle = _stored(app)["components"][IDS.comp_no_history]
    assert tuple(saddle[field] for field in fields) == expected
    assert (
        app.business_logic.update_component_lifetime_service_alternate(
            "update", IDS.comp_no_history, 20000, None, None
        )[0]
        is True
    )
    saddle = _stored(app)["components"][IDS.comp_no_history]
    assert tuple(saddle[field] for field in fields) == expected


def test_retired_component_counts_days_to_retirement(app):
    """Day-based lifetime of a retired component stops at retirement, not at now.

    Commuter pads installed 2025-01-01 08:00, retired 2025-10-01 08:00: 31+28+31+30+31+30+31+31+30
    = 273 days; remaining 365 - 273 = 92, OK (threshold 30). Distance: commute rides Jan..Sep 2025,
    9 x 10 = 90; lifetime remaining 1500 - 90 = 1410, OK. Service 2025-04-01 before retirement:
    rides Apr..Sep 2025 counted, 6 x 10 = 60; service next 500 - 60 = 440, OK. The service
    marker is Jan..Mar 2025, 3 x 10 = 30. update_time_based_fields skips retired components,
    so the frozen clock does not move these values.
    """
    stored = _stored(app)
    pads = stored["components"][IDS.comp_pads_retired]
    assert (
        pads["component_distance"],
        pads["lifetime_remaining"],
        pads["lifetime_remaining_days"],
        pads["lifetime_status"],
    ) == (90, 1410, 92, "OK")
    assert (pads["service_next"], pads["service_next_days"], pads["service_status"]) == (440, None, "OK")
    assert stored["component_history"][IDS.hist_pads_retired]["distance_marker"] == 90
    pads_service = stored["services"][IDS.svc_pads_retired]
    assert (pads_service["distance_marker"], pads_service["bike_id"]) == (30, IDS.bike_retired)


def test_service_resets_interval(app):
    """Each completed service restarts the service interval; lifetime keeps counting.

    Cassette on road since 2025-01-01: 22 x 50 = 1100 km; lifetime remaining 6000 - 1100 = 4900, OK.
    Service markers: svc-cassette-1 2025-06-01 is Jan..May 2025, 5 x 50 = 250; svc-cassette-2
    2026-02-01 is Jun 2025..Jan 2026, 8 x 50 = 400. Since the last service: Feb..Oct 2026,
    9 x 50 = 450; service next 1000 - 450 = 550, OK (threshold 100). Without the services the
    1100 km would exceed the 1000 km interval.
    """
    stored = _stored(app)
    cassette = stored["components"][IDS.comp_cassette_serviced]
    assert (cassette["component_distance"], cassette["lifetime_remaining"], cassette["lifetime_status"]) == (
        1100,
        4900,
        "OK",
    )
    assert (cassette["service_next"], cassette["service_status"]) == (550, "OK")
    services = stored["services"]
    markers = {
        service_id: (services[service_id]["distance_marker"], services[service_id]["bike_id"])
        for service_id in (IDS.svc_cassette_1, IDS.svc_cassette_2)
    }
    assert markers == {IDS.svc_cassette_1: (250, IDS.bike_road), IDS.svc_cassette_2: (400, IDS.bike_road)}


def test_services_across_installation_periods(app):
    """Service distances follow the chain across bikes and skip the months it was off.

    svc-chain-1 2025-04-01 (on road): road Jan..Mar 2025, 3 x 50 = 150, bike road.
    svc-chain-2 2025-10-01 (on gravel): road Apr..Jun 2025, 3 x 50 = 150, plus gravel Aug..Sep
    2025, 2 x 20 = 40, total 190, bike gravel.
    Since svc-chain-2: gravel Oct 2025..Feb 2026, 5 x 20 = 100, plus road Apr..Oct 2026,
    7 x 50 = 350, total 450; service next 500 - 450 = 50, below threshold 100: "Due for service".
    The planned service svc-chain-planned keeps no marker or bike.
    """
    stored = _stored(app)
    services = stored["services"]
    markers = {
        service_id: (services[service_id]["distance_marker"], services[service_id]["bike_id"])
        for service_id in (IDS.svc_chain_1, IDS.svc_chain_2, IDS.svc_chain_planned)
    }
    assert markers == {
        IDS.svc_chain_1: (150, IDS.bike_road),
        IDS.svc_chain_2: (190, IDS.bike_gravel),
        IDS.svc_chain_planned: (None, None),
    }
    chain = stored["components"][IDS.comp_chain_moved]
    assert (chain["service_next"], chain["service_status"]) == (50, "Due for service")


def test_time_based_intervals_count_days_to_now(app):
    """Day-based values of an active component count to the frozen now, 2026-11-16 12:00.

    Gravel tire installed 2025-12-01 08:00: Dec 2025..Oct 2026 is 31+31+28+31+30+31+30+31+31+30+31
    = 335 days to 2026-11-01, plus 15 = 350 (whole days); lifetime remaining 365 - 350 = 15, below
    threshold 30: "Due for replacement". Last service 2026-08-01 08:00: 31+30+31 = 92 days to
    2026-11-01, plus 15 = 107; service next 90 - 107 = -17: "Service interval exceeded".
    No km intervals: lifetime remaining and service next None, distance still counted, gravel
    Dec 2025..Oct 2026, 11 x 20 = 220. Service marker of svc-tire: gravel Dec 2025..Jul 2026,
    8 x 20 = 160.
    """
    stored = _stored(app)
    tire = stored["components"][IDS.comp_tire_time]
    assert (
        tire["component_distance"],
        tire["lifetime_remaining"],
        tire["lifetime_remaining_days"],
        tire["lifetime_status"],
    ) == (220, None, 15, "Due for replacement")
    assert (tire["service_next"], tire["service_next_days"], tire["service_status"]) == (
        None,
        -17,
        "Service interval exceeded",
    )
    assert stored["services"][IDS.svc_tire]["distance_marker"] == 160


def test_component_without_service_interval_has_no_service_status(app):
    """Bremseklosser bak æøå on gravel since 2025-01-01: 22 x 20 = 440 km; lifetime remaining
    1500 - 440 = 1060, OK (threshold 100). No km or day service interval: service next None,
    "Not defined".
    """
    pads = _stored(app)["components"][IDS.comp_pads_norwegian]
    assert (pads["component_distance"], pads["lifetime_remaining"], pads["lifetime_status"]) == (440, 1060, "OK")
    assert (pads["service_next"], pads["service_next_days"], pads["service_status"]) == (None, None, "Not defined")


def test_bike_status_is_worst_component(app):
    """A bike with an exceeded component needs attention, whatever its other components are.

    bike-gravel: tire service exceeded (-17 days) outranks the OK pads: "Components need attention".
    bike-retired: no installed component, one retired: "No active components".
    """
    bikes = _stored(app)["bikes"]
    assert bikes[IDS.bike_gravel]["service_status"] == "Components need attention"
    assert bikes[IDS.bike_retired]["service_status"] == "No active components"


def test_due_component_does_not_change_bike_status_when_another_is_ok(app):
    """update_bike_status ranks exceeded first, then OK, so any OK component outranks a due one.

    Each installed component counts once: exceeded if lifetime or service is exceeded, else due if
    either is due, else OK if either is OK. With one exceeded the bike needs attention; otherwise
    with one OK it is healthy, so the due chain on bike-road (service next 50) leaves it
    "All components healthy" beside the OK cassette and wheel.
    """
    stored = _stored(app)
    assert stored["components"][IDS.comp_chain_moved]["service_status"] == "Due for service"
    assert stored["bikes"][IDS.bike_road]["service_status"] == "All components healthy"


def test_component_type_counts_include_every_installation_status(app):
    """in_use counts every component of the type, installed, not installed or retired"""
    types = _stored(app)["component_types"]
    assert {name: row["in_use"] for name, row in types.items()} == {
        "Chain": 1,
        "Cassette": 1,
        "Rear wheel": 1,
        "Tire": 1,
        "Rear brake pads": 2,
        "Saddle": 1,
        "Bottle cage": 0,
    }


def test_ride_at_install_and_service_timestamps_counts_on_both_sides(app):
    """Ride time filters are inclusive at both ends, so a ride at an event's exact minute counts.

    Chain on bike-boundary installed 2026-01-01 08:00, serviced 2026-03-01 08:00. Rides: 1 km at
    the install minute, 2 km on 2026-02-10, 4 km at the service minute, 8 km on 2026-04-10.
    Distance (rides >= install): 1 + 2 + 4 + 8 = 15, the install-minute ride included.
    Service marker (install <= ride <= service): 1 + 2 + 4 = 7.
    Since service (rides >= service): 4 + 8 = 12; service next 500 - 12 = 488.
    The 4 km ride at the service minute counts both in the service marker and in the distance
    since that service (#373).
    """
    _insert(app, "bikes", [_bike("bike-boundary", "Boundary bike")])
    _insert(
        app,
        "rides",
        [
            _ride("ride-boundary-install", "bike-boundary", "2026-01-01 08:00", 1.0),
            _ride("ride-boundary-feb", "bike-boundary", "2026-02-10 12:00", 2.0),
            _ride("ride-boundary-service", "bike-boundary", "2026-03-01 08:00", 4.0),
            _ride("ride-boundary-apr", "bike-boundary", "2026-04-10 12:00", 8.0),
        ],
    )
    _insert(
        app,
        "components",
        [
            component(
                "comp-boundary",
                "bike-boundary",
                "Boundary chain",
                "Chain",
                "Installed",
                "2026-01-01 08:00",
                0,
                lifetime_expected=3000,
                service_interval=500,
                threshold_km=100,
            )
        ],
    )
    _insert(
        app,
        "component_history",
        [history("hist-boundary", "comp-boundary", "bike-boundary", "Boundary chain", "2026-01-01 08:00", "Installed")],
    )
    _insert(
        app,
        "services",
        [service("svc-boundary", "comp-boundary", "Boundary chain", "Lubed", "Completed", "2026-03-01 08:00")],
    )
    assert recalculate(app) == [NO_HISTORY_FAILURE]
    stored = _stored(app)
    chain = stored["components"]["comp-boundary"]
    assert (chain["component_distance"], chain["service_next"], chain["service_status"]) == (15, 488, "OK")
    assert stored["services"]["svc-boundary"]["distance_marker"] == 7


def test_bike_with_only_unrated_components_is_maintenance_not_defined(app):
    """An installed component with no lifetime or service interval rates "Not defined" on both, so
    its bike, with nothing else installed, reads "Maintenance not defined". Distance still counts:
    one 30 km ride since installation.
    """
    _insert(app, "bikes", [_bike("bike-cage", "Cage bike")])
    _insert(app, "rides", [_ride("ride-cage", "bike-cage", "2026-02-10 12:00", 30.0)])
    _insert(
        app,
        "components",
        [component("comp-cage", "bike-cage", "Cage", "Bottle cage", "Installed", "2026-01-01 08:00", 0)],
    )
    _insert(
        app,
        "component_history",
        [history("hist-cage", "comp-cage", "bike-cage", "Cage", "2026-01-01 08:00", "Installed")],
    )
    assert recalculate(app) == [NO_HISTORY_FAILURE]
    stored = _stored(app)
    cage = stored["components"]["comp-cage"]
    assert (cage["component_distance"], cage["lifetime_status"], cage["service_status"]) == (
        30,
        "Not defined",
        "Not defined",
    )
    assert stored["bikes"]["bike-cage"]["service_status"] == "Maintenance not defined"


def test_bike_left_without_components_is_no_components_registered(app):
    """A component uninstalled from a bike is stored with no bike, and the bike status is updated
    for the bike of its latest history record; with nothing else on that bike it reads
    "No components registered". Distance: one 30 km ride while installed, Jan..Mar 2026.
    """
    _insert(app, "bikes", [_bike("bike-empty", "Empty bike")])
    _insert(app, "rides", [_ride("ride-empty", "bike-empty", "2026-02-10 12:00", 30.0)])
    _insert(
        app,
        "components",
        [
            component(
                "comp-loose",
                None,
                "Loose saddle",
                "Saddle",
                "Not installed",
                "2026-03-01 08:00",
                0,
                lifetime_expected=20000,
                threshold_km=200,
            )
        ],
    )
    _insert(
        app,
        "component_history",
        [
            history("hist-loose-on", "comp-loose", "bike-empty", "Loose saddle", "2026-01-01 08:00", "Installed"),
            history("hist-loose-off", "comp-loose", "bike-empty", "Loose saddle", "2026-03-01 08:00", "Not installed"),
        ],
    )
    assert recalculate(app) == [NO_HISTORY_FAILURE]
    stored = _stored(app)
    loose = stored["components"]["comp-loose"]
    assert (loose["bike_id"], loose["component_distance"], loose["lifetime_remaining"], loose["lifetime_status"]) == (
        None,
        30,
        19970,
        "OK",
    )
    assert stored["bikes"]["bike-empty"]["service_status"] == "No components registered"


def test_lifetime_reached_exactly_is_exceeded(app):
    """Remaining lifetime of zero already counts as exceeded, and an exceeded component makes the
    bike need attention. Worn pads with a 1100 km lifetime on bike-road since 2025-01-01:
    22 x 50 = 1100 km, remaining 1100 - 1100 = 0: "Lifetime exceeded"; bike-road becomes
    "Components need attention" although cassette and wheel are OK.
    """
    _insert(
        app,
        "components",
        [
            component(
                "comp-worn-pads",
                IDS.bike_road,
                "Worn pads",
                "Rear brake pads",
                "Installed",
                "2025-01-01 08:00",
                0,
                lifetime_expected=1100,
                threshold_km=100,
            )
        ],
    )
    _insert(
        app,
        "component_history",
        [history("hist-worn-pads", "comp-worn-pads", IDS.bike_road, "Worn pads", "2025-01-01 08:00", "Installed")],
    )
    assert recalculate(app) == [NO_HISTORY_FAILURE]
    stored = _stored(app)
    pads = stored["components"]["comp-worn-pads"]
    assert (pads["component_distance"], pads["lifetime_remaining"], pads["lifetime_status"]) == (
        1100,
        0,
        "Lifetime exceeded",
    )
    assert stored["bikes"][IDS.bike_road]["service_status"] == "Components need attention"


def test_collection_with_retired_member_needs_attention(app):
    """A retired member blocks operations: retired pads plus the installed gravel pads, collection
    on bike-gravel. One installed bike, matching the collection's, so no mismatch.
    """
    _insert(
        app,
        "collections",
        [
            {
                "collection_id": "coll-retired",
                "collection_name": "With retired",
                "components": json.dumps([IDS.comp_pads_retired, IDS.comp_pads_norwegian]),
                "bike_id": IDS.bike_gravel,
                "sub_collections": None,
                "updated_date": "2026-01-01 08:00",
                "comment": None,
            }
        ],
    )
    status = derived_values(app)["collection"]["coll-retired"]["status"]
    assert status == {
        "is_empty": False,
        "has_retired": True,
        "has_mixed_statuses": False,
        "has_different_bikes": False,
        "collection_bike_mismatch": False,
        "blocks_operations": True,
        "can_display_bike": False,
        "retired_count": 1,
        "installed_count": 1,
        "not_installed_count": 0,
        "bike_count": 1,
        "bike_names_list": ["Gravel bike"],
        "actual_component_bike_id": IDS.bike_gravel,
        "actual_component_bike_name": "Gravel bike",
        "status": "needs_attention",
    }


def test_collection_with_members_on_different_bikes_needs_attention(app):
    """Members installed on two bikes block operations and no single bike is shown: the chain on
    bike-road and the tire on bike-gravel, collection on bike-road (one of them, so no mismatch).
    """
    _insert(
        app,
        "collections",
        [
            {
                "collection_id": "coll-split",
                "collection_name": "Split",
                "components": json.dumps([IDS.comp_chain_moved, IDS.comp_tire_time]),
                "bike_id": IDS.bike_road,
                "sub_collections": None,
                "updated_date": "2026-01-01 08:00",
                "comment": None,
            }
        ],
    )
    status = derived_values(app)["collection"]["coll-split"]["status"]
    assert status == {
        "is_empty": False,
        "has_retired": False,
        "has_mixed_statuses": False,
        "has_different_bikes": True,
        "collection_bike_mismatch": False,
        "blocks_operations": True,
        "can_display_bike": False,
        "retired_count": 0,
        "installed_count": 2,
        "not_installed_count": 0,
        "bike_count": 2,
        "bike_names_list": ["Gravel bike", "Road bike"],
        "actual_component_bike_id": None,
        "actual_component_bike_name": None,
        "status": "needs_attention",
    }


def test_bike_with_only_due_component_fails_status_update(app):
    """Records current behaviour; see #371.

    Due chain alone on bike-due: one 450 km ride since installation, lifetime 3000 - 450 = 2550 OK,
    service next 500 - 450 = 50, "Due for service". It counts as due, not OK, so no branch of
    update_bike_status sets a status and it raises UnboundLocalError: the distance iterator stops
    at bike-due (first in sort order) and process_history_records fails for the chain. The
    component values are written before the raise; the bike status stays unset.
    """
    _insert(app, "bikes", [_bike("bike-due", "Due bike")])
    _insert(app, "rides", [_ride("ride-due", "bike-due", "2026-06-10 12:00", 450.0)])
    _insert(
        app,
        "components",
        [
            component(
                "comp-due-chain",
                "bike-due",
                "Due chain",
                "Chain",
                "Installed",
                "2026-06-01 08:00",
                0,
                lifetime_expected=3000,
                service_interval=500,
                threshold_km=100,
            )
        ],
    )
    _insert(
        app,
        "component_history",
        [history("hist-due-chain", "comp-due-chain", "bike-due", "Due chain", "2026-06-01 08:00", "Installed")],
    )
    assert recalculate(app) == [
        f'distance_iterator:all_bikes: {{"{UNBOUND_STATUS}"}}',
        f"process_history_records:comp-due-chain: Error processing history records for Due chain: {UNBOUND_STATUS}",
        NO_HISTORY_FAILURE,
    ]
    stored = _stored(app)
    chain = stored["components"]["comp-due-chain"]
    assert (chain["component_distance"], chain["lifetime_status"], chain["service_next"], chain["service_status"]) == (
        450,
        "OK",
        50,
        "Due for service",
    )
    assert stored["bikes"]["bike-due"]["service_status"] is None


def test_bike_with_only_not_installed_component_fails_status_update(app):
    """Records current behaviour; see #371.

    Spare wheel stored as not installed but still registered to bike-spare (bike_id kept), with
    history installed 2026-01-01 and uninstalled 2026-03-01 on bike-spare, one 100 km ride between.
    update_bike_status(bike-spare) finds components but none installed or retired, sets no status
    and raises UnboundLocalError inside process_history_records. The distance iterator skips
    bike-spare (nothing installed), so only that one line is added. Distance 100 and lifetime
    10000 - 100 = 9900 OK are written before the raise; bike_id stays set, the bike status unset.
    """
    _insert(app, "bikes", [_bike("bike-spare", "Spare bike")])
    _insert(app, "rides", [_ride("ride-spare", "bike-spare", "2026-02-10 12:00", 100.0)])
    _insert(
        app,
        "components",
        [
            component(
                "comp-spare-wheel",
                "bike-spare",
                "Spare wheel",
                "Rear wheel",
                "Not installed",
                "2026-03-01 08:00",
                0,
                lifetime_expected=10000,
                threshold_km=200,
            )
        ],
    )
    _insert(
        app,
        "component_history",
        [
            history("hist-spare-on", "comp-spare-wheel", "bike-spare", "Spare wheel", "2026-01-01 08:00", "Installed"),
            history(
                "hist-spare-off", "comp-spare-wheel", "bike-spare", "Spare wheel", "2026-03-01 08:00", "Not installed"
            ),
        ],
    )
    assert recalculate(app) == [
        NO_HISTORY_FAILURE,
        f"process_history_records:comp-spare-wheel: Error processing history records for Spare wheel: {UNBOUND_STATUS}",
    ]
    stored = _stored(app)
    wheel = stored["components"]["comp-spare-wheel"]
    assert (wheel["bike_id"], wheel["component_distance"], wheel["lifetime_remaining"], wheel["lifetime_status"]) == (
        "bike-spare",
        100,
        9900,
        "OK",
    )
    assert stored["bikes"]["bike-spare"]["service_status"] is None
