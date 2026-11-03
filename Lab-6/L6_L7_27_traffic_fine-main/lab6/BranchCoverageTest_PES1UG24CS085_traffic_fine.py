import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Test cases written so that every decision (if / elif / else / for)
# in traffic_fine.py is taken both ways, including boundary values.


# ---------- speeding_fine ----------

def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_speed_equal_to_limit():
    # boundary: speed == limit is not speeding
    assert speeding_fine(60, 60, "city") == 0

def test_school_zone_base_fine():
    assert speeding_fine(40, 30, "school") == 2000

def test_school_zone_excess_over_20():
    assert speeding_fine(55, 30, "school") == 4000

def test_school_zone_excess_over_40():
    assert speeding_fine(100, 50, "school") == 6000

def test_highway_zone_base_fine():
    assert speeding_fine(105, 100, "highway") == 1000

def test_highway_zone_excess_over_20():
    assert speeding_fine(130, 100, "highway") == 2000

def test_highway_zone_excess_over_40():
    assert speeding_fine(150, 100, "highway") == 3000

def test_city_zone_small_excess():
    assert speeding_fine(70, 60, "city") == 500

def test_other_zone_excess_over_40():
    assert speeding_fine(110, 60, "residential") == 1500

def test_excess_exactly_20_is_base_fine():
    # boundary: excess of 20 is not "> 20"
    assert speeding_fine(80, 60, "city") == 500

def test_excess_exactly_40_is_double():
    # boundary: excess of 40 is not "> 40"
    assert speeding_fine(100, 60, "city") == 1000


# ---------- license_action ----------

def test_clean_record():
    assert license_action(2, False, False) == "none"

def test_commercial_driver_revoked():
    assert license_action(12, True, False) == "revoke"

def test_private_driver_suspended():
    assert license_action(12, False, False) == "suspend"

def test_repeat_offender_suspended():
    assert license_action(8, False, True) == "suspend"

def test_first_offender_warning():
    assert license_action(11, False, False) == "warning"

def test_commercial_flag_ignored_below_12():
    assert license_action(9, True, False) == "warning"

def test_notice_lower_boundary():
    assert license_action(4, False, False) == "notice"

def test_notice_upper_boundary():
    assert license_action(7, False, True) == "notice"

def test_zero_points():
    assert license_action(0, True, True) == "none"


# ---------- total_penalty ----------

def test_empty_list_total_zero():
    # loop body never runs
    assert total_penalty([]) == 0

def test_total_below_cap():
    assert total_penalty([500, 1000, 2000]) == 3500

def test_total_exactly_at_cap():
    # boundary: 10000 is not "> 10000", so no capping
    assert total_penalty([6000, 4000]) == 10000

def test_total_capped_at_10000():
    assert total_penalty([6000, 6000]) == 10000

def test_zero_fine_allowed():
    assert total_penalty([0, 500]) == 500

def test_negative_fine_raises():
    with pytest.raises(ValueError):
        total_penalty([500, -100])

def test_negative_fine_first_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-1])
