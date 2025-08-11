import sqlite3
import json

def print_db_contents(db_path="test_data/test_optimization.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM optimization_results")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    if not rows:
        print("No results found in the database.")
    for row in rows:
        record = dict(zip(columns, row))
        # Pretty print metadata if it's a dict-like string
        if record.get("metadata"):
            try:
                record["metadata"] = json.loads(record["metadata"].replace("'", '"'))
            except Exception:
                pass
        print(json.dumps(record, indent=2, default=str))
        print("-" * 40)
    conn.close()

if __name__ == "__main__":
    print_db_contents("test_data/test_optimization.db")
