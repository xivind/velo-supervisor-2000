"""The health rule: an error logged in the last 24 hours, a failing database or a missing database
file make the app unhealthy; warnings and lower levels do not (#103).

The app fixture binds the modules to the synthetic dataset. Recorder tests log through a logger
whose only handler is utils.ERROR_RECORDER; the /health tests import main, which adds the
recorder to the root logger, as at startup.
"""

import importlib
import logging
from datetime import timedelta

import pytest
import time_machine
from integrity.clock import FIXED_NOW


@pytest.fixture
def recorder(app):
    return app.utils.ERROR_RECORDER


@pytest.fixture
def logger(recorder):
    test_logger = logging.getLogger("test_health")
    test_logger.handlers = [recorder]
    test_logger.propagate = False
    test_logger.setLevel(logging.DEBUG)
    yield test_logger
    test_logger.handlers = []


@pytest.fixture
def database(app):
    return importlib.import_module("velo_supervisor.database_model").database


def test_recorder_keeps_errors_and_ignores_lower_levels(logger, recorder):
    logger.info("Ride sync started")
    logger.warning("Validation of history record failed: Invalid date format")
    logger.error("Bulk update of database failed")
    assert [message for _, message in recorder.read_recent_errors(24)] == ["Bulk update of database failed"]


def test_recorder_keeps_ignoring_lower_levels_when_handler_level_is_reset(logger, recorder):
    """lifespan in main.py sets every root handler to INFO or DEBUG at startup"""
    recorder.setLevel(logging.DEBUG)
    logger.debug("Component distance update successful")
    logger.warning("Collection validation failed")
    assert recorder.read_recent_errors(24) == []


def test_recorder_includes_exception_in_message(logger, recorder):
    try:
        raise AttributeError("'NoneType' object has no attribute 'bike_name'")
    except AttributeError:
        logger.exception("An error occurred")
    assert [message for _, message in recorder.read_recent_errors(24)] == [
        "An error occurred: AttributeError: 'NoneType' object has no attribute 'bike_name'"
    ]


def test_healthy_without_errors_and_with_working_database(app):
    """The recalculation of the dataset logs no error, so the fixture starts healthy"""
    database_check = app.business_logic.check_database_connection()
    assert database_check == (True, "ok")
    assert app.utils.get_health_status(*database_check) == (
        True,
        {"status": "healthy", "database": "ok", "latest_errors": []},
    )


def test_error_makes_app_unhealthy_for_24_hours(app, logger):
    """An error logged at the frozen now counts until 24 hours have passed"""
    logger.error("An error occurred refreshing tokens: expired")
    healthy, health_status = app.utils.get_health_status(True, "ok")
    assert healthy is False
    assert health_status == {
        "status": "unhealthy",
        "database": "ok",
        "latest_errors": [{"time": "2026-11-16 12:00:00", "message": "An error occurred refreshing tokens: expired"}],
    }

    with time_machine.travel(FIXED_NOW + timedelta(hours=23, minutes=59), tick=False):
        assert app.utils.get_health_status(True, "ok")[0] is False
    with time_machine.travel(FIXED_NOW + timedelta(hours=24, minutes=1), tick=False):
        assert app.utils.get_health_status(True, "ok") == (
            True,
            {"status": "healthy", "database": "ok", "latest_errors": []},
        )


def test_health_status_lists_the_last_three_errors_cut_at_300_characters(app, logger):
    """The status shows only the newest three errors, oldest first, each cut at 300 characters"""
    messages = [f"Error {number}: " + "x" * 400 for number in range(1, 5)]
    for message in messages:
        logger.error(message)
    healthy, health_status = app.utils.get_health_status(True, "ok")
    assert healthy is False
    assert health_status["latest_errors"] == [
        {"time": "2026-11-16 12:00:00", "message": message[:300]} for message in messages[1:]
    ]


def test_failing_database_makes_app_unhealthy(app, database, tmp_path):
    not_a_database = tmp_path / "not_a_database.sqlite"
    not_a_database.write_text("this is not a database", encoding="utf-8")
    database.init(str(not_a_database))

    database_check = app.business_logic.check_database_connection()
    assert database_check == (False, "Database check failed: file is not a database")
    healthy, health_status = app.utils.get_health_status(*database_check)
    assert healthy is False
    assert (health_status["status"], health_status["database"]) == (
        "unhealthy",
        "Database check failed: file is not a database",
    )


def test_missing_database_file_makes_app_unhealthy(app, database, tmp_path):
    """SQLite creates an empty file for a wrong path, e.g. a missing Docker mount"""
    database.init(str(tmp_path / "missing.sqlite"))
    database_check = app.business_logic.check_database_connection()
    assert database_check == (False, "Database check failed: no such table: bikes")
    assert app.utils.get_health_status(*database_check)[0] is False


def test_health_route_answers_200_when_healthy_and_503_after_an_error(client):
    """An error logged anywhere reaches the recorder through the root logger"""
    response = client.get("/health")
    assert (response.status_code, response.json()["status"]) == (200, "healthy")

    logging.getLogger("velo_supervisor").error("Strava API request failed")
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json()["latest_errors"] == [{"time": "2026-11-16 12:00:00", "message": "Strava API request failed"}]
