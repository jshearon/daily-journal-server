import sqlite3
import json
from models import Entry

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./db/dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM entries a
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['moodId'])

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      e.id,
      e.concept,
      e.entry,
      e.date,
      e.moodId
    FROM entries e
    WHERE e.id = ?
    """, (id, ))

    data = db_cursor.fetchone()

    entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['moodId'])
    return json.dumps(entry.__dict__)
