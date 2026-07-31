"""
Exercise 1: Python & Data Handling
===================================

This exercise has three levels. Complete as far as you can.
Each level builds on the previous one.

- BASE: Pure Python (no libraries required)
- STANDARD: Use pandas for data analysis
- ADVANCED: Optimization and edge-case handling

Run: python exercises/exercise_1_data.py
"""

from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "support_tickets.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "output"


# ============================================================
# BASE LEVEL — Pure Python (no external libraries needed)
# ============================================================

def load_csv_manual(filepath: str) -> list[dict]:
    """
    Load a CSV file using only built-in Python (no pandas).
    Return a list of dictionaries where each dict is one row,
    with column names as keys.

    Example: [{"ticket_id": "1", "title": "Login issue", ...}, ...]
    """
    import csv 
    with open(filepath, "r") as f:
        data = list(csv.DictReader(f)) # Used DictReader because the first row is the header and we need dictionaries
        return data


def count_by_status(rows: list[dict]) -> dict:
    """
    Count how many tickets are in each status (open, resolved, etc.).
    Return a dict like: {"open": 12, "resolved": 23}
    """
    from collections import Counter
    statuses = [row["status"] for row in rows] # goes through each row and receives the status of each ticket in a list
    tickets_dict = Counter(statuses) # Counter counts each word and returns a dict with the word and the count
    return tickets_dict


def filter_by_priority(rows: list[dict], priority: str) -> list[dict]:
    """
    Return only rows matching the given priority (case-insensitive).
    Example: filter_by_priority(rows, "high") returns all high-priority tickets.
    """
    tickets = []
    for row in rows:
        # turning strings lowercase for case-insensitive comparison
        ticket_priority = row["priority"].lower()
        if ticket_priority == priority.lower():
            tickets.append(row)
    return tickets


def find_missing_descriptions(rows: list[dict]) -> list[str]:
    """
    Return ticket_ids where 'description' is empty or missing.
    """
    ticket_ids = []
    for row in rows:
        if row["description"] is None or row["description"].strip() == "":
            ticket_ids.append(row["ticket_id"])
    return ticket_ids



# ============================================================
# STANDARD LEVEL — Pandas-based analysis
# ============================================================

def load_data(filepath: str):
    """Load the CSV file and return a pandas DataFrame."""
    import pandas as pd

    df = pd.read_csv(filepath)
    return df


def clean_data(df):
    """
    Clean the dataset:
    1. Remove rows where 'description' is empty or null.
    2. Normalize 'priority' column to lowercase: low, medium, high, critical.
    3. Parse 'created_at' into datetime format.

    Return the cleaned DataFrame.
    """
    import pandas as pd

    new_df = df.copy()
    not_null = new_df["description"].notna()
    not_empty = new_df["description"].str.strip() != ""
    new_df = new_df[not_empty & not_null]

    new_df["priority"] = new_df["priority"].str.lower()

    new_df["created_at"] = pd.to_datetime(new_df["created_at"])

    return new_df


def tickets_per_month(df) -> dict:
    """Return the number of tickets created per month (as a dict or Series)."""
    # TODO: Implement this function
    pass


def avg_resolution_time_by_priority(df) -> dict:
    """
    Return the average resolution time (in hours) per priority level.
    Resolution time = resolved_at - created_at
    """
    # TODO: Implement this function
    pass


def highest_unresolved_category(df) -> str:
    """Return the category with the highest percentage of unresolved tickets."""
    # TODO: Implement this function
    pass


# ============================================================
# ADVANCED LEVEL — Optimization, edge cases, and design
# ============================================================

def load_data_chunked(filepath: str, chunk_size: int = 1000):
    """
    Load data in chunks for memory efficiency.
    Simulate handling a file that doesn't fit in memory.
    Return the fully processed DataFrame.
    """
    # TODO: Implement chunked reading
    pass


def detect_anomalies(df) -> list[dict]:
    """
    Find tickets with suspicious data:
    - resolved_at earlier than created_at
    - resolution time over 30 days
    - duplicate ticket titles from the same customer

    Return a list of dicts describing each anomaly found:
    [{"ticket_id": ..., "issue": "resolved before created"}, ...]
    """
    # TODO: Implement anomaly detection
    pass


def generate_summary_report(df) -> str:
    """
    Generate a formatted text report including:
    - Total tickets, open vs resolved
    - Busiest month
    - Slowest category to resolve
    - Top 3 customers by ticket count
    - Data quality score (% of rows with no issues)

    Return as a formatted string.
    """
    # TODO: Implement report generation
    pass


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Exercise 1: Python & Data Handling")
    print("=" * 60)

    # --- BASE ---
    print("\n--- BASE LEVEL ---")
    rows = load_csv_manual(DATA_PATH)
    if rows:
        print(f"Loaded {len(rows)} rows")
        print(f"Status counts: {count_by_status(rows)}")
        print(f"High priority tickets: {len(filter_by_priority(rows, 'high'))}")
        print(f"Missing descriptions: {find_missing_descriptions(rows)}")
    else:
        print("load_csv_manual() not implemented yet")

    # --- STANDARD ---
    print("\n--- STANDARD LEVEL ---")
    try:
        df = load_data(DATA_PATH)
    except ImportError:
        print("pandas not installed — skip with: pip install pandas")
        df = None
    if df is not None:
        df_clean = clean_data(df)
        print(f"Rows after cleaning: {len(df_clean)}")
        print(f"Tickets per month: {tickets_per_month(df_clean)}")
        print(f"Avg resolution time: {avg_resolution_time_by_priority(df_clean)}")
        print(f"Worst category: {highest_unresolved_category(df_clean)}")

        # Export
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(OUTPUT_PATH / "cleaned_tickets.csv", index=False)
        print(f"Exported to {OUTPUT_PATH}/cleaned_tickets.csv")
    else:
        print("load_data() not implemented yet")

    # --- ADVANCED ---
    print("\n--- ADVANCED LEVEL ---")
    if df is not None:
        anomalies = detect_anomalies(df_clean) if df_clean is not None else None
        if anomalies is not None:
            print(f"Anomalies found: {len(anomalies)}")
            for a in anomalies[:5]:
                print(f"  - Ticket {a.get('ticket_id')}: {a.get('issue')}")

        report = generate_summary_report(df_clean) if df_clean is not None else None
        if report:
            print(f"\n{report}")
        else:
            print("generate_summary_report() not implemented yet")
    else:
        print("Requires STANDARD level to be completed first")
