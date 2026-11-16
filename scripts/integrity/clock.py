import os
import time
from contextlib import contextmanager
from datetime import datetime, timezone

import time_machine

FIXED_NOW = datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc)


@contextmanager
def frozen_clock():
    """Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible"""
    previous_tz = os.environ.get("TZ")
    os.environ["TZ"] = "UTC"
    time.tzset()
    try:
        with time_machine.travel(FIXED_NOW, tick=False):
            yield
    finally:
        if previous_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = previous_tz
        time.tzset()
