"""
Exercise 2: SQL Test Runner
============================

This script sets up an in-memory SQLite database with the schema and sample data,
then runs your SQL queries from exercise_2_sql.sql and prints the results.

Usage:
    python exercises/run_sql.py
"""

import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SCHEMA_FILE = DATA_DIR / "schema.sql"
SQL_EXERCISE_FILE = Path(__file__).parent / "exercise_2_sql.sql"


def create_database() -> sqlite3.Connection:
    """Create an in-memory SQLite database and load schema + sample data."""
    conn = sqlite3.connect(":memory:")
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    return conn


def extract_queries(filepath: Path) -> list[tuple[str, str]]:
    """
    Parse the SQL exercise file and extract named queries.
    Returns a list of (query_name, query_sql) tuples.

    Args:
        filepath: Path to the SQL file containing queries.
    
    Returns:
        List of tuples where each tuple is (query_name, query_sql).
    """
    content = filepath.read_text(encoding="utf-8")
    queries = []
    current_name = None
    current_lines = []

    for line in content.splitlines():
        if line.strip().startswith("-- Query"):
            # Save previous query if exists
            if current_name and current_lines:
                sql = "\n".join(current_lines).strip()
                if sql:
                    queries.append((current_name, sql))
            current_name = line.strip().lstrip("- ").split(":")[0].strip()
            current_lines = []
        elif line.strip().startswith("-- Expected"):
            continue
        elif line.strip().startswith("-- ") and current_name and not current_lines:
            # Continuation of the query description comment, skip
            continue
        elif current_name is not None:
            # Only collect non-comment lines as SQL
            if not line.strip().startswith("--"):
                current_lines.append(line)

    # Don't forget the last query
    if current_name and current_lines:
        sql = "\n".join(current_lines).strip()
        if sql:
            queries.append((current_name, sql))

    return queries


def run_query(conn: sqlite3.Connection, name: str, sql: str) -> None:
    """Execute a query and print results in a formatted table.
    
    Args:
        conn: SQLite connection object.
        name: Name of the query for display.
        sql: The SQL query string to execute.
        
    Returns: 
        None. Prints results to console.
    """
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    print(f"SQL:\n{sql}\n")

    try:
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Print header
        col_widths = [max(len(str(col)), max((len(str(r[i])) for r in rows), default=0)) for i, col in enumerate(columns)]
        header = " | ".join(col.ljust(w) for col, w in zip(columns, col_widths))
        separator = "-+-".join("-" * w for w in col_widths)

        print(header)
        print(separator)

        # Print rows
        for row in rows:
            print(" | ".join(str(val).ljust(w) for val, w in zip(row, col_widths)))

        print(f"\n({len(rows)} rows)")

    except Exception as e:
        print(f"ERROR: {e}")


def main():
    print("Setting up SQLite database with sample data...")
    conn = create_database()

    # Verify data loaded
    cursor = conn.execute("SELECT COUNT(*) FROM employees")
    emp_count = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM departments")
    dept_count = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM projects")
    proj_count = cursor.fetchone()[0]
    print(f"Loaded: {emp_count} employees, {dept_count} departments, {proj_count} projects")

    # Extract and run queries
    queries = extract_queries(SQL_EXERCISE_FILE)

    if not queries:
        print("\nNo queries found in exercise_2_sql.sql.")
        print("Write your SQL queries below the comment markers and run this script again.")
        return

    print(f"\nFound {len(queries)} queries to execute:")

    for name, sql in queries:
        run_query(conn, name, sql)

    conn.close()
    print(f"\n{'='*60}")
    print("Done.")


if __name__ == "__main__":
    main()
