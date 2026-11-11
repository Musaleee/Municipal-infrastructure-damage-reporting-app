"""Traffic fine helpers - hardened after fuzz testing (Lab 7).

Every function now validates its input and returns None for anything
malformed instead of raising an exception.
"""
import re

MAX_TOTAL = 10000
MAX_DIGITS = 9  # keeps int() conversions small and fast

# ASCII-only patterns: str.isdigit() / \d would also accept things like '²'
# or Arabic-Indic digits, which int() then rejects or silently converts.
_TICKET_RE = re.compile(r"([A-Za-z]{1,10})-([0-9]{4})-([0-9]{1,%d})" % MAX_DIGITS)
_AMOUNT_RE = re.compile(r"[0-9]{1,%d}" % MAX_DIGITS)


def parse_ticket_id(ticket_id):
    """'TF-2024-0456' -> ('TF', 2024, 456); None if the ID is malformed."""
    if not isinstance(ticket_id, str):
        return None
    match = _TICKET_RE.fullmatch(ticket_id.strip())
    if match is None:
        return None
    prefix, year, serial = match.groups()
    return prefix.upper(), int(year), int(serial)


def total_fines(amounts_csv):
    """'500,1200,300' -> 2000, capped at MAX_TOTAL; None if any amount is bad."""
    if not isinstance(amounts_csv, str):
        return None
    parts = [part.strip() for part in amounts_csv.split(',')]
    if not all(_AMOUNT_RE.fullmatch(part) for part in parts):
        return None  # empty, negative, non-numeric or absurdly long amount
    return min(sum(int(part) for part in parts), MAX_TOTAL)


def speed_excess(reading):
    """'72/60' -> 20 (percent over the limit); 0 if not speeding.

    None if the reading is malformed or the limit is zero.
    """
    if not isinstance(reading, str):
        return None
    parts = [part.strip() for part in reading.split('/')]
    if len(parts) != 2 or not all(_AMOUNT_RE.fullmatch(part) for part in parts):
        return None
    speed, limit = int(parts[0]), int(parts[1])
    if limit == 0:
        return None
    return max(speed - limit, 0) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    if result is None:
        print("Invalid ticket ID. Expected format PREFIX-YYYY-SERIAL.")
    else:
        print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    if result is None:
        print("Invalid fine amounts. Use non-negative whole numbers separated by commas.")
    else:
        print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    if result is None:
        print("Invalid reading. Use speed/limit with a limit greater than 0.")
    else:
        print("Percent Over Limit:", result)


if __name__ == "__main__":
    main()
