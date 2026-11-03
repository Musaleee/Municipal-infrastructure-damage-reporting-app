import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Test cases written to execute every line (statement) of traffic_fine.py


# ---------- speeding_fine ----------

def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_school_zone_excess_over_40():
    # school base 2000, excess 50 -> triple
    assert speeding_fine(100, 50, "school") == 6000

def test_highway_zone_excess_over_20():
    # highway base 1000, excess 30 -> double
    assert speeding_fine(130, 100, "highway") == 2000

def test_city_zone_small_excess():
    # any other zone base 500, excess 10 -> base fine
    assert speeding_fine(70, 60, "city") == 500


# ---------- license_action ----------

def test_clean_record():
    assert license_action(2, False, False) == "none"

def test_commercial_driver_revoked():
    assert license_action(12, True, False) == "revoke"

def test_private_driver_suspended():
    assert license_action(13, False, False) == "suspend"

def test_repeat_offender_suspended():
    assert license_action(9, False, True) == "suspend"

def test_first_offender_warning():
    assert license_action(8, False, False) == "warning"

def test_notice():
    assert license_action(5, False, False) == "notice"


# ---------- total_penalty ----------

def test_total_capped_at_10000():
    assert total_penalty([6000, 6000]) == 10000

def test_negative_fine_raises():
    with pytest.raises(ValueError):
        total_penalty([500, -100])
