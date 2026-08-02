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
        #.       missing                          empty
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

    months = df["created_at"].dt.to_period("M") # converting the timestamp to month
    counts = months.value_counts() # counting how many tickets there are in each month
    return counts.sort_index()


def avg_resolution_time_by_priority(df) -> dict:
    """
    Return the average resolution time (in hours) per priority level.
    Resolution time = resolved_at - created_at
    """
    import pandas as pd
    df = df.copy() # to not make changes to the original df
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])
    resolved = df[df["status"] == "resolved"] # throwing away the open tickets

    res_time_td = resolved["resolved_at"] - resolved["created_at"] # this is timedelta, needs to be converted to hours

    hours = res_time_td.dt.total_seconds() / 3600
    resolved["resolution_hours"] = hours
    avg_time_by_priority = resolved.groupby("priority")["resolution_hours"].mean() # grouping the priorities and taking the mean of the res hours
    return avg_time_by_priority


def highest_unresolved_category(df) -> str:
    """Return the category with the highest percentage of unresolved tickets."""

    import pandas as pd
    total = df["category"].value_counts() # counting the total tickets per category
    unresolved = df[df["status"] == "open"]["category"].value_counts() # counting the tickets which are still open by the category
    percantage = unresolved.div(total, fill_value = 0) # divide unresolved by total, the result is between 1 and 0, not percantage
    return percantage.idxmax()



# ============================================================
# ADVANCED LEVEL — Optimization, edge cases, and design
# ============================================================

def load_data_chunked(filepath: str, chunk_size: int = 1000):
    """
    Load data in chunks for memory efficiency.
    Simulate handling a file that doesn't fit in memory.
    Return the fully processed DataFrame.
    """
    import pandas as pd

    chunks = pd.read_csv(filepath, chunksize=chunk_size)
    df = pd.concat(chunks, ignore_index=True) # putting all chunks together
    return df


def detect_anomalies(df) -> list[dict]:
    """
    Find tickets with suspicious data:
    - resolved_at earlier than created_at
    - resolution time over 30 days
    - duplicate ticket titles from the same customer

    Return a list of dicts describing each anomaly found:
    [{"ticket_id": ..., "issue": "resolved before created"}, ...]
    """
    import pandas as pd

    anomalies = []

    # resolved_at earlier than created_at
    df1 = df.copy()
    df1["resolved_at"] = pd.to_datetime(df1["resolved_at"])
    df1["created_at"] = pd.to_datetime(df1["created_at"])
    df_check1 = df1[df1["resolved_at"] < df1["created_at"]]

    # resolution time over 30 days
    df2 = df.copy()
    df2["resolved_at"] = pd.to_datetime(df2["resolved_at"])
    res_time_td = df2["resolved_at"] - df2["created_at"]
    days = res_time_td.dt.days
    df_check2 = df2[days > 30]

    # duplicate ticket titles from the same customer
    df_check3 = df[df.duplicated(subset = ["customer_id", "title"], keep = False)]

    # converting df to set for faster scanning
    check1_ids = set(df_check1["ticket_id"])
    check2_ids = set(df_check2["ticket_id"])
    check3_ids = set(df_check3["ticket_id"])

    for ticket_id in df["ticket_id"]:
        issue = [] # storing all anomalies each ticket has
        if ticket_id in check1_ids:
            issue.append("resolved_at earlier than created_at")
        if ticket_id in check2_ids:
            issue.append("resolution time over 30 days")
        if ticket_id in check3_ids:
            issue.append("duplicate ticket titles from the same customer")

        if issue:
            anomalies.append({"ticket_id": ticket_id, "issue": issue})

    return anomalies


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
    # Total tickets, open vs resolved
    total_tickets = count_by_status(df.to_dict(orient="records")) # turns df to dict
    report = f"Total tickets: {sum(total_tickets.values())}, open: {total_tickets["open"]}, resolved: {total_tickets["resolved"]}\n"

    # Busiest month
    month_tickets = tickets_per_month(df)
    busiest_month = month_tickets.idxmax()
    report += f"Busiest month: {busiest_month}\n"

    # Slowest category to resolve (similar to avg_resolution_time_by_priority)
    slowest_category = slowest_category_func(df) 
    report += f"Slowest category to resolve {slowest_category}\n"

    # Top 3 customers by ticket count
    customers = top_3_customers(df)
    report += f"Top 3 customers by ticket count: {', '.join(customers)}\n"
    
    # Data quality score (% of rows with no issues)
    anomalies_count = len(detect_anomalies(df))
    total = len(df)
    report += f"Data quality score: {(1-anomalies_count/total)*100:.2f}%"

    return report

# helper function
def slowest_category_func(df) -> str:
    """Slowest category to resolve (similar to avg_resolution_time_by_priority)"""
    import pandas as pd
    df = df.copy() # to not make changes to the original df
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])
    resolved = df[df["status"] == "resolved"] # keeping only the resolved tickets
    res_time_td = resolved["resolved_at"] - resolved["created_at"] # this is timedelta

    time = res_time_td.dt.total_seconds()
    resolved["time"] = time
    avg_time_by_category = resolved.groupby("category")["time"].mean()
    slowest_category = avg_time_by_category.idxmax()
    return slowest_category

# helper
def top_3_customers(df) -> list:
    import pandas as pd
    from collections import Counter
    customers = df["customer_id"].tolist()
    top_3 = [item for item, count in Counter(customers).most_common(3)]
    return top_3


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
