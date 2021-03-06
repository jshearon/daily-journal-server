import sqlite3
import json
from models import Entry
from models import Mood
from models import Tag

def get_all_entries():
    with sqlite3.connect("./db/dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId,
            m.label mood_label
        FROM entries a
        JOIN moods m ON a.moodId = m.id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['date'], row['moodId'])
            mood = Mood(row['moodId'], row['mood_label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

            db_cursor.execute("""
              SELECT 
              t.id,
              t.name, 
              e.entry_id
              FROM entry_tag e
              JOIN tags t ON t.id = e.tag_id
              WHERE e.entry_id = ?
              """, ( row['id'], ))

            tagset = db_cursor.fetchall()
            tags = []
            for tag in tagset:
              each_tag = Tag(tag['id'], tag['name'])
              tags.append(each_tag.__dict__)
            entry.tags = tags

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

def entries_q(searchterm):
    with sqlite3.connect("./db/dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        from Entries e
        WHERE e.entry LIKE ?
        """, ( '%'+searchterm+'%', ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])
            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_journal_entry(new_entry):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      INSERT INTO entries
        (concept, entry, date, moodId)
      VALUES 
        (?, ?, ?, ?)
    """, ( new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'], ))

    id = db_cursor.lastrowid
    new_entry['id'] = id

    if new_entry['tags']:
      for tag in new_entry['tags']:
        db_cursor.execute("""
              INSERT INTO entry_tag 
                (entry_id, tag_id) 
              VALUES (?, ?)
        """, ( id, tag, ))

    return json.dumps(new_entry)

def update_entry(id, new_entry):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      UPDATE entries
      SET concept = ?, entry = ?, date = ?, moodId = ?
      WHERE id = ?
    """, ( new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'], id, ))

    rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
  
    db_cursor.execute("""
      DELETE FROM entries
      WHERE id = ?
      """, ( id, ))
