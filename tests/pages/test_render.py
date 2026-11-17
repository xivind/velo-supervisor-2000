"""Every page renders for every resource in the dataset, and unknown IDs fail the way they do today.

Not requested:
- /refresh_all_bikes and /refresh_rides/{mode}: Strava actions, covered by the Strava tests
- /get_filtered_log: reads the fixed path /data/logs/app.log
- /health: covered by test_health.py
- /incident_reports/{id}: there is no incident detail route; incidents render on /incident_reports
- POST routes: covered by the characterisation tests

The client is used without a with block, so the lifespan and the scheduler do not start.
"""
import pytest

from fixtures.dataset import IDS, BIKES, COMPONENTS, COLLECTIONS, INCIDENTS, WORKPLANS

OVERVIEW_PAGES = [
    ("/", "Road bike"),
    ("/component_overview", "Cassette"),
    ("/incident_reports", "Chain skips under load"),
    ("/workplans", "Brake check"),
    ("/component_types_overview", "Bottle cage"),
    ("/config_overview", "Config"),
    ("/help", "Help"),
]

DETAIL_PAGES = (
    [("/bike_details/{}", bike["bike_id"], bike["bike_name"]) for bike in BIKES]
    + [("/component_details/{}", row["component_id"], row["component_name"]) for row in COMPONENTS]
    + [("/collection_details/{}", row["collection_id"], row["collection_name"]) for row in COLLECTIONS]
    + [("/workplan_details/{}", row["workplan_id"], row["workplan_description"]) for row in WORKPLANS]
)

DETAIL_ROUTES = ["/bike_details/{}", "/component_details/{}", "/collection_details/{}", "/workplan_details/{}"]


@pytest.mark.parametrize("path, expected_text", OVERVIEW_PAGES, ids=[path for path, _ in OVERVIEW_PAGES])
def test_every_overview_page_renders(client, path, expected_text):
    response = client.get(path)
    assert response.status_code == 200
    assert expected_text in response.text


@pytest.mark.parametrize("route, resource_id, expected_text", DETAIL_PAGES,
                         ids=[route.format(resource_id) for route, resource_id, _ in DETAIL_PAGES])
def test_every_detail_page_renders(client, route, resource_id, expected_text):
    response = client.get(route.format(resource_id))
    assert response.status_code == 200
    assert expected_text in response.text


def test_every_incident_is_listed(client):
    text = client.get("/incident_reports").text
    for incident in INCIDENTS:
        assert incident["incident_description"] in text


@pytest.mark.parametrize("route", DETAIL_ROUTES)
def test_unknown_ids_today(client, route):
    """Stage 4 changes the unknown-ID status to 404 (#356)"""
    response = client.get(route.format("does-not-exist"))
    assert response.status_code == 500
