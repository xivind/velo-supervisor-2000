"""Synthetic dataset that characterisation, rule, page and Strava tests start from.

Every date lies before FIXED_NOW (2026-11-16 12:00 UTC). Installation records and
services are at 08:00 on the 1st of a month; rides are at 12:00 mid-month, so no ride
shares a timestamp with an event and the boundaries never decide a result.

Rides, one a month:
- bike-road: 50 km on the 10th, 2025-01 to 2026-10 (22 rides, 1100 km)
- bike-gravel: 20 km on the 20th, 2025-01 to 2026-10 (22 rides, 440 km)
- bike-retired: 10 km on the 15th, 2025-01 to 2026-03 (15 rides, 150 km); the bike is retired
- ride-no-gear: 15 km on 2026-05-05, bike_id "None" as Strava stores rides without gear

Components:
- comp-chain-moved (Chain, 3000 km, service 500 km): moved across both active bikes.
  Road 2025-01-01 to 2025-07-01, off a month, gravel 2025-08-01 to 2026-03-01, off a
  month, road again from 2026-04-01. Completed services 2025-04-01 (road period) and
  2025-10-01 (gravel period), so service records span several installation records.
  Rides since the last service count only while installed: 5 gravel rides plus 7 road
  rides, so it is due for service. Has the planned service of wp-drivetrain.
- comp-cassette-serviced (Cassette, service 1000 km): road since 2025-01-01, 1100 km, which
  would exceed the interval, but completed services 2025-06-01 and 2026-02-01 reset it.
- comp-wheel-offset (Rear wheel): road since 2025-03-01 with a 1000 km distance offset
  (bought used); the offset counts for lifetime, not for the service interval. Has a
  planned service with its own planned date and no workplan.
- comp-tire-time (Tire): only time-based intervals (365 days lifetime, 90 days service,
  30 days threshold). Gravel since 2025-12-01, last service 2026-08-01, so it is due
  for replacement and past its service interval. It is the worst component of
  bike-gravel, which therefore needs attention.
- comp-pads-norwegian, named "Bremseklosser bak æøå": gravel since 2025-01-01, healthy.
- comp-pads-retired: bike-retired from 2025-01-01, serviced 2025-04-01, retired
  2025-10-01; its 365-day lifetime counts days up to retirement. bike-retired is left
  with no active components.
- comp-no-history (Spare saddle): not installed, no installation history, 300 km
  offset, stored as the alternate method sets it on creation. Recalculation reports
  it as the one failure, by design.

Collections: coll-mixed holds an installed and a not installed component (needs
attention); coll-gravel-set holds the two gravel components (healthy).

Workplans and incidents: wp-drivetrain (planned, generated title) and inc-drivetrain
(open) share a completed cassette service and the planned chain service; wp-brake-check
(done, named) and inc-squeal (resolved) share the completed service of comp-pads-retired.

Component types are this module's own (COMPONENT_TYPES), replacing the template's.
Chain and Rear wheel are mandatory, so bike-gravel and bike-retired lack both; Bottle
cage is unused.

Computed columns (distances, remaining, next, statuses, markers, in_use) start blank or
zero, except on comp-no-history, so every value after setup comes from the
recalculation. Row order matters: on bike-road the healthy cassette comes before the
chain, because update_bike_status raises when a bike's only rated installed components
are due (no OK, none exceeded), which a chain recalculated first would hit (#371;
Task 9 carries a dedicated characterisation test for it).

IDS holds every ID except rides; values start with bike-, comp-, coll-, wp-, inc-, svc-
or hist-. Ride IDs read ride-<road|gravel|commute>-<yyyy>-<mm>, plus ride-no-gear.
"""

import json
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from velo_supervisor import db_migration

TEMPLATE_DB = Path(__file__).resolve().parents[2] / "config" / "template_db.sqlite"


@dataclass(frozen=True)
class DatasetIds:
    bike_road: str = "bike-road"
    bike_gravel: str = "bike-gravel"
    bike_retired: str = "bike-retired"
    comp_chain_moved: str = "comp-chain-moved"
    comp_cassette_serviced: str = "comp-cassette-serviced"
    comp_wheel_offset: str = "comp-wheel-offset"
    comp_tire_time: str = "comp-tire-time"
    comp_pads_norwegian: str = "comp-pads-norwegian"
    comp_pads_retired: str = "comp-pads-retired"
    comp_no_history: str = "comp-no-history"
    hist_chain_road_1: str = "hist-chain-road-1"
    hist_chain_off_road: str = "hist-chain-off-road"
    hist_chain_gravel: str = "hist-chain-gravel"
    hist_chain_off_gravel: str = "hist-chain-off-gravel"
    hist_chain_road_2: str = "hist-chain-road-2"
    hist_cassette: str = "hist-cassette"
    hist_wheel: str = "hist-wheel"
    hist_tire: str = "hist-tire"
    hist_pads_norwegian: str = "hist-pads-norwegian"
    hist_pads_installed: str = "hist-pads-installed"
    hist_pads_retired: str = "hist-pads-retired"
    svc_chain_1: str = "svc-chain-1"
    svc_chain_2: str = "svc-chain-2"
    svc_chain_planned: str = "svc-chain-planned"
    svc_cassette_1: str = "svc-cassette-1"
    svc_cassette_2: str = "svc-cassette-2"
    svc_wheel_planned: str = "svc-wheel-planned"
    svc_tire: str = "svc-tire"
    svc_pads_retired: str = "svc-pads-retired"
    coll_mixed: str = "coll-mixed"
    coll_gravel_set: str = "coll-gravel-set"
    wp_drivetrain: str = "wp-drivetrain"
    wp_brake_check: str = "wp-brake-check"
    inc_drivetrain: str = "inc-drivetrain"
    inc_squeal: str = "inc-squeal"


IDS = DatasetIds()

COMPONENT_TYPES = [
    {
        "component_type": "Chain",
        "expected_lifetime": 3000,
        "service_interval": 500,
        "in_use": 0,
        "mandatory": "Yes",
        "max_quantity": 1,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": 100,
        "threshold_days": None,
    },
    {
        "component_type": "Cassette",
        "expected_lifetime": 6000,
        "service_interval": 1000,
        "in_use": 0,
        "mandatory": "No",
        "max_quantity": 1,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": 100,
        "threshold_days": None,
    },
    {
        "component_type": "Rear wheel",
        "expected_lifetime": 10000,
        "service_interval": 2000,
        "in_use": 0,
        "mandatory": "Yes",
        "max_quantity": 1,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": 200,
        "threshold_days": None,
    },
    {
        "component_type": "Tire",
        "expected_lifetime": None,
        "service_interval": None,
        "in_use": 0,
        "mandatory": "No",
        "max_quantity": 2,
        "service_interval_days": 90,
        "lifetime_expected_days": 365,
        "threshold_km": None,
        "threshold_days": 30,
    },
    {
        "component_type": "Rear brake pads",
        "expected_lifetime": 1500,
        "service_interval": None,
        "in_use": 0,
        "mandatory": "No",
        "max_quantity": 1,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": 100,
        "threshold_days": None,
    },
    {
        "component_type": "Saddle",
        "expected_lifetime": 20000,
        "service_interval": None,
        "in_use": 0,
        "mandatory": "No",
        "max_quantity": 1,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": 200,
        "threshold_days": None,
    },
    {
        "component_type": "Bottle cage",
        "expected_lifetime": None,
        "service_interval": None,
        "in_use": 0,
        "mandatory": "No",
        "max_quantity": 0,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": None,
        "threshold_days": None,
    },
]

BIKES = [
    {
        "bike_id": IDS.bike_road,
        "bike_name": "Road bike",
        "bike_retired": "False",
        "service_status": None,
        "total_distance": 1100.0,
        "notes": "Summer bike",
    },
    {
        "bike_id": IDS.bike_gravel,
        "bike_name": "Gravel bike",
        "bike_retired": "False",
        "service_status": None,
        "total_distance": 440.0,
        "notes": None,
    },
    {
        "bike_id": IDS.bike_retired,
        "bike_name": "Old commuter",
        "bike_retired": "True",
        "service_status": None,
        "total_distance": 150.0,
        "notes": "Sold 2026-04",
    },
]


def _months(first, last):
    year, month = first
    while (year, month) <= last:
        yield year, month
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)


def monthly_rides(bike_id, label, day, distance, moving_time, last):
    return [
        {
            "ride_id": f"ride-{label}-{year}-{month:02d}",
            "bike_id": bike_id,
            "record_time": f"{year}-{month:02d}-{day:02d} 12:00",
            "ride_name": f"{label.capitalize()} ride {year}-{month:02d}",
            "ride_distance": distance,
            "moving_time": moving_time,
            "commute": "False",
        }
        for year, month in _months((2025, 1), last)
    ]


RIDES = (
    monthly_rides(IDS.bike_road, "road", 10, 50.0, "2:00:00", (2026, 10))
    + monthly_rides(IDS.bike_gravel, "gravel", 20, 20.0, "1:00:00", (2026, 10))
    + monthly_rides(IDS.bike_retired, "commute", 15, 10.0, "0:40:00", (2026, 3))
    + [
        {
            "ride_id": "ride-no-gear",
            "bike_id": "None",
            "record_time": "2026-05-05 12:00",
            "ride_name": "Rental bike",
            "ride_distance": 15.0,
            "moving_time": "1:00:00",
            "commute": "True",
        }
    ]
)


def component(component_id, bike_id, name, component_type, status, updated_date, cost, **settings):
    row = {
        "component_id": component_id,
        "bike_id": bike_id,
        "component_name": name,
        "component_type": component_type,
        "component_distance": 0.0,
        "component_distance_offset": 0,
        "installation_status": status,
        "lifetime_expected": None,
        "lifetime_remaining": None,
        "lifetime_status": None,
        "service_interval": None,
        "service_status": None,
        "service_next": None,
        "updated_date": updated_date,
        "cost": cost,
        "notes": None,
        "service_interval_days": None,
        "lifetime_expected_days": None,
        "threshold_km": None,
        "threshold_days": None,
        "lifetime_remaining_days": None,
        "service_next_days": None,
    }
    row.update(settings)
    return row


COMPONENTS = [
    component(
        IDS.comp_cassette_serviced,
        IDS.bike_road,
        "Cassette",
        "Cassette",
        "Installed",
        "2025-01-01 08:00",
        800,
        lifetime_expected=6000,
        service_interval=1000,
        threshold_km=100,
    ),
    component(
        IDS.comp_wheel_offset,
        IDS.bike_road,
        "Rear wheel",
        "Rear wheel",
        "Installed",
        "2025-03-01 08:00",
        2500,
        component_distance_offset=1000,
        lifetime_expected=10000,
        service_interval=2000,
        threshold_km=200,
        notes="Bought used",
    ),
    component(
        IDS.comp_chain_moved,
        IDS.bike_road,
        "Chain",
        "Chain",
        "Installed",
        "2026-04-01 08:00",
        400,
        lifetime_expected=3000,
        service_interval=500,
        threshold_km=100,
    ),
    component(
        IDS.comp_tire_time,
        IDS.bike_gravel,
        "Gravel tire",
        "Tire",
        "Installed",
        "2025-12-01 08:00",
        600,
        lifetime_expected_days=365,
        service_interval_days=90,
        threshold_days=30,
    ),
    component(
        IDS.comp_pads_norwegian,
        IDS.bike_gravel,
        "Bremseklosser bak æøå",
        "Rear brake pads",
        "Installed",
        "2025-01-01 08:00",
        200,
        lifetime_expected=1500,
        threshold_km=100,
        notes="Byttet før påske",
    ),
    component(
        IDS.comp_pads_retired,
        IDS.bike_retired,
        "Commuter brake pads",
        "Rear brake pads",
        "Retired",
        "2025-10-01 08:00",
        150,
        lifetime_expected=1500,
        service_interval=500,
        threshold_km=100,
        lifetime_expected_days=365,
        threshold_days=30,
    ),
    component(
        IDS.comp_no_history,
        None,
        "Spare saddle",
        "Saddle",
        "Not installed",
        "2025-05-01 08:00",
        1200,
        component_distance=300.0,
        component_distance_offset=300,
        lifetime_expected=20000,
        lifetime_remaining=19700.0,
        lifetime_status="OK",
        service_status="Not defined",
        threshold_km=200,
    ),
]


def history(history_id, component_id, bike_id, name, updated_date, reason, notes=None):
    return {
        "history_id": history_id,
        "component_id": component_id,
        "bike_id": bike_id,
        "component_name": name,
        "updated_date": updated_date,
        "update_reason": reason,
        "distance_marker": 0.0,
        "notes": notes,
    }


HISTORY = [
    history(IDS.hist_chain_road_1, IDS.comp_chain_moved, IDS.bike_road, "Chain", "2025-01-01 08:00", "Installed"),
    history(IDS.hist_chain_off_road, IDS.comp_chain_moved, IDS.bike_road, "Chain", "2025-07-01 08:00", "Not installed"),
    history(
        IDS.hist_chain_gravel,
        IDS.comp_chain_moved,
        IDS.bike_gravel,
        "Chain",
        "2025-08-01 08:00",
        "Installed",
        "Moved to the gravel bike for winter",
    ),
    history(
        IDS.hist_chain_off_gravel, IDS.comp_chain_moved, IDS.bike_gravel, "Chain", "2026-03-01 08:00", "Not installed"
    ),
    history(IDS.hist_chain_road_2, IDS.comp_chain_moved, IDS.bike_road, "Chain", "2026-04-01 08:00", "Installed"),
    history(IDS.hist_cassette, IDS.comp_cassette_serviced, IDS.bike_road, "Cassette", "2025-01-01 08:00", "Installed"),
    history(IDS.hist_wheel, IDS.comp_wheel_offset, IDS.bike_road, "Rear wheel", "2025-03-01 08:00", "Installed"),
    history(IDS.hist_tire, IDS.comp_tire_time, IDS.bike_gravel, "Gravel tire", "2025-12-01 08:00", "Installed"),
    history(
        IDS.hist_pads_norwegian,
        IDS.comp_pads_norwegian,
        IDS.bike_gravel,
        "Bremseklosser bak æøå",
        "2025-01-01 08:00",
        "Installed",
    ),
    history(
        IDS.hist_pads_installed,
        IDS.comp_pads_retired,
        IDS.bike_retired,
        "Commuter brake pads",
        "2025-01-01 08:00",
        "Installed",
    ),
    history(
        IDS.hist_pads_retired,
        IDS.comp_pads_retired,
        IDS.bike_retired,
        "Commuter brake pads",
        "2025-10-01 08:00",
        "Retired",
    ),
]


def service(
    service_id,
    component_id,
    name,
    description,
    status,
    service_date=None,
    workplan_id=None,
    incident_id=None,
    planned_date=None,
):
    return {
        "service_id": service_id,
        "component_id": component_id,
        "component_name": name,
        "bike_id": None,
        "service_date": service_date,
        "distance_marker": 0.0 if status == "Completed" else None,
        "description": description,
        "workplan_id": workplan_id,
        "status": status,
        "incident_id": incident_id,
        "planned_date": planned_date,
    }


SERVICES = [
    service(IDS.svc_chain_1, IDS.comp_chain_moved, "Chain", "Cleaned and lubed", "Completed", "2025-04-01 08:00"),
    service(IDS.svc_chain_2, IDS.comp_chain_moved, "Chain", "Waxed", "Completed", "2025-10-01 08:00"),
    service(
        IDS.svc_chain_planned,
        IDS.comp_chain_moved,
        "Chain",
        "Replace chain",
        "Planned",
        workplan_id=IDS.wp_drivetrain,
        incident_id=IDS.inc_drivetrain,
    ),
    service(
        IDS.svc_cassette_1, IDS.comp_cassette_serviced, "Cassette", "Cleaned cassette", "Completed", "2025-06-01 08:00"
    ),
    service(
        IDS.svc_cassette_2,
        IDS.comp_cassette_serviced,
        "Cassette",
        "Deep clean",
        "Completed",
        "2026-02-01 08:00",
        workplan_id=IDS.wp_drivetrain,
        incident_id=IDS.inc_drivetrain,
    ),
    service(
        IDS.svc_wheel_planned,
        IDS.comp_wheel_offset,
        "Rear wheel",
        "True rear wheel",
        "Planned",
        planned_date="2026-10-15 10:00",
    ),
    service(IDS.svc_tire, IDS.comp_tire_time, "Gravel tire", "Sealant top-up", "Completed", "2026-08-01 08:00"),
    service(
        IDS.svc_pads_retired,
        IDS.comp_pads_retired,
        "Commuter brake pads",
        "Cleaned pads",
        "Completed",
        "2025-04-01 08:00",
        workplan_id=IDS.wp_brake_check,
        incident_id=IDS.inc_squeal,
    ),
]

COLLECTIONS = [
    {
        "collection_id": IDS.coll_mixed,
        "collection_name": "Mixed parts",
        "components": json.dumps([IDS.comp_wheel_offset, IDS.comp_no_history]),
        "bike_id": IDS.bike_road,
        "sub_collections": None,
        "updated_date": "2026-03-01 08:00",
        "comment": "Installed and spare parts",
    },
    {
        "collection_id": IDS.coll_gravel_set,
        "collection_name": "Gravel set",
        "components": json.dumps([IDS.comp_tire_time, IDS.comp_pads_norwegian]),
        "bike_id": IDS.bike_gravel,
        "sub_collections": None,
        "updated_date": "2025-12-01 08:00",
        "comment": None,
    },
]

WORKPLANS = [
    {
        "workplan_id": IDS.wp_drivetrain,
        "workplan_name": None,
        "due_date": "2026-11-01 10:00",
        "workplan_status": "Planned",
        "workplan_size": "Medium",
        "workplan_description": "Drivetrain overhaul",
        "completion_date": None,
        "completion_notes": None,
    },
    {
        "workplan_id": IDS.wp_brake_check,
        "workplan_name": "Brake check",
        "due_date": "2025-04-01 10:00",
        "workplan_status": "Done",
        "workplan_size": "Small",
        "workplan_description": "Check the commuter brakes",
        "completion_date": "2025-04-01 10:00",
        "completion_notes": "Pads cleaned",
    },
]

INCIDENTS = [
    {
        "incident_id": IDS.inc_drivetrain,
        "incident_date": "2026-01-15 10:00",
        "incident_status": "Open",
        "incident_severity": "Priority",
        "incident_affected_component_ids": json.dumps([IDS.comp_chain_moved, IDS.comp_cassette_serviced]),
        "incident_affected_bike_id": IDS.bike_road,
        "incident_description": "Chain skips under load",
        "resolution_date": None,
        "resolution_notes": None,
    },
    {
        "incident_id": IDS.inc_squeal,
        "incident_date": "2025-03-20 10:00",
        "incident_status": "Resolved",
        "incident_severity": "Monitor",
        "incident_affected_component_ids": json.dumps([IDS.comp_pads_retired]),
        "incident_affected_bike_id": IDS.bike_retired,
        "incident_description": "Rear brake squeals",
        "resolution_date": "2025-04-01 10:00",
        "resolution_notes": "Cleaned the pads",
    },
]

TABLES = {
    "component_types": COMPONENT_TYPES,
    "bikes": BIKES,
    "rides": RIDES,
    "components": COMPONENTS,
    "component_history": HISTORY,
    "services": SERVICES,
    "collections": COLLECTIONS,
    "workplans": WORKPLANS,
    "incidents": INCIDENTS,
}


def build_dataset(db_path: Path) -> None:
    """Write the dataset into a migrated copy of the template database at db_path"""
    shutil.copy(TEMPLATE_DB, db_path)
    connection = sqlite3.connect(db_path)
    try:
        db_migration.run_all_migrations(connection.cursor(), connection)
        connection.execute("DELETE FROM component_types")
        for table, rows in TABLES.items():
            columns = list(rows[0])
            connection.executemany(
                f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
                [[row[column] for column in columns] for row in rows],
            )
        connection.commit()
    finally:
        connection.close()
