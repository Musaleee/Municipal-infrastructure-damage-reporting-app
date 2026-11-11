"""Lab 7 - Fuzz testing traffic_fine.py with Hypothesis.

Aryan Musale (PES1UG24CS085)

Each function gets:
  * a "no crash" fuzz test fed with arbitrary text / None, and
  * property tests fed with well-formed or almost-well-formed inputs,
    checking the result is actually correct.
"""
from hypothesis import given, settings, strategies as st

from traffic_fine import parse_ticket_id, total_fines, speed_excess

FUZZ = settings(max_examples=500, deadline=None)

# Inputs that look like the real thing but hit the edge cases
# (zeros, negatives, blanks, extra separators, unicode digits, spaces).
ticket_like = st.from_regex(r"\A[A-Za-z0-9 ]{0,3}-[0-9-]{0,5}-[0-9 ]{0,4}\Z")
csv_like = st.lists(st.integers(-20000, 20000).map(str) | st.just(""),
                    min_size=1, max_size=6).map(",".join)
reading_like = st.from_regex(r"\A-?[0-9]{1,3}/-?[0-9]{1,3}\Z")


# ---------------------------------------------------------------- parse_ticket_id
@FUZZ
@given(st.text() | st.none())
def test_parse_ticket_id_no_crash(s):
    try:
        parse_ticket_id(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_ticket_id crashed with: {e!r}"


@FUZZ
@given(ticket_like)
def test_parse_ticket_id_near_valid_no_crash(s):
    try:
        parse_ticket_id(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_ticket_id crashed with: {e!r}"


@FUZZ
@given(st.from_regex(r"\A[A-Za-z]{1,4}\Z"),
       st.integers(1900, 2100),
       st.integers(0, 99999))
def test_parse_ticket_id_valid(prefix, year, serial):
    ticket = f"{prefix}-{year}-{serial:04d}"
    assert parse_ticket_id(ticket) == (prefix.upper(), year, serial)


# ---------------------------------------------------------------- total_fines
@FUZZ
@given(st.text() | st.none())
def test_total_fines_no_crash(s):
    try:
        total_fines(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"total_fines crashed with: {e!r}"


@FUZZ
@given(csv_like)
def test_total_fines_never_negative(s):
    result = total_fines(s)
    assert result is None or 0 <= result <= 10000


@FUZZ
@given(st.lists(st.integers(0, 5000), min_size=1, max_size=10))
def test_total_fines_valid(amounts):
    csv = ",".join(str(a) for a in amounts)
    assert total_fines(csv) == min(sum(amounts), 10000)


# ---------------------------------------------------------------- speed_excess
@FUZZ
@given(st.text() | st.none())
def test_speed_excess_no_crash(s):
    try:
        speed_excess(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"speed_excess crashed with: {e!r}"


@FUZZ
@given(reading_like)
def test_speed_excess_near_valid(s):
    result = speed_excess(s)
    assert result is None or result >= 0


@FUZZ
@given(st.integers(0, 300), st.integers(1, 200))
def test_speed_excess_valid(speed, limit):
    expected = max(speed - limit, 0) * 100 // limit
    assert speed_excess(f"{speed}/{limit}") == expected
