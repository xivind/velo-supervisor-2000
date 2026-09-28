"""Health check: errors logged the last 24 hours or a failing database make the app unhealthy, warnings do not"""

import logging
from datetime import datetime, timedelta


def recording_logger(modules):
    logger = logging.getLogger("test_health")
    logger.handlers = [modules.utils.ERROR_RECORDER]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    return logger


def test_recorder_keeps_errors_and_ignores_lower_levels(modules):
    logger = recording_logger(modules)
    logger.info("Ride sync started")
    logger.warning("Validation of history record failed: Invalid date format")
    logger.error("Bulk update of database failed")

    recent_errors = modules.utils.ERROR_RECORDER.read_recent_errors(24)
    assert [message for _, message in recent_errors] == ["Bulk update of database failed"]


def test_recorder_keeps_errors_even_when_handler_level_is_reset(modules):
    """lifespan in main.py sets every root handler to INFO or DEBUG at startup"""
    modules.utils.ERROR_RECORDER.setLevel(logging.DEBUG)
    logger = recording_logger(modules)
    logger.debug("Component distance update successful")
    logger.warning("Collection validation failed")

    assert modules.utils.ERROR_RECORDER.read_recent_errors(24) == []


def test_recorder_includes_exception_in_message(modules):
    logger = recording_logger(modules)
    try:
        raise AttributeError("'NoneType' object has no attribute 'bike_name'")
    except AttributeError:
        logger.exception("An error occurred")

    _, message = modules.utils.ERROR_RECORDER.read_recent_errors(24)[0]
    assert message == "An error occurred: AttributeError: 'NoneType' object has no attribute 'bike_name'"


def test_healthy_without_errors_and_with_working_database(modules):
    success, message = modules.business_logic.check_database_connection()
    assert success and message == "ok"

    healthy, health_status = modules.utils.get_health_status(success, message)
    assert healthy
    assert health_status == {"status": "healthy", "database": "ok", "latest_errors": []}


def test_error_makes_app_unhealthy_for_24_hours(modules):
    recorder = modules.utils.ERROR_RECORDER
    recorder.errors.append((datetime.now() - timedelta(hours=25), "An error occurred refreshing tokens: expired"))
    assert modules.utils.get_health_status(True, "ok")[0]

    recorder.errors.append((datetime.now() - timedelta(hours=23), "An error occurred refreshing tokens: expired"))
    healthy, health_status = modules.utils.get_health_status(True, "ok")
    assert not healthy
    assert health_status["status"] == "unhealthy"
    assert [error["message"] for error in health_status["latest_errors"]] == ["An error occurred refreshing tokens: expired"]


def test_failing_database_makes_app_unhealthy(modules, tmp_path):
    not_a_database = tmp_path / "not_a_database.sqlite"
    not_a_database.write_text("this is not a database", encoding="utf-8")
    modules.database_model.database.init(str(not_a_database))

    success, message = modules.business_logic.check_database_connection()
    assert not success and message == "Database check failed: file is not a database"

    healthy, health_status = modules.utils.get_health_status(success, message)
    assert not healthy
    assert health_status["database"] == message


def test_missing_database_file_makes_app_unhealthy(modules, tmp_path):
    """SQLite creates an empty file for a wrong path, e.g. a missing Docker mount"""
    modules.database_model.database.init(str(tmp_path / "missing.sqlite"))

    success, message = modules.business_logic.check_database_connection()
    assert not success and message == "Database check failed: no such table: bikes"
