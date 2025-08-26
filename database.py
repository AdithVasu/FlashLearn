import sqlite3
import pandas as pd
import os

DB_FILE = "notes.db"

def init_db():
    """Initializes the database schema if it does not exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            youtube_url TEXT NOT NULL,
            summary_level TEXT,
            notes_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_notes_to_db(title: str, youtube_url: str, summary_level: str, notes_content: str):
    """Saves the generated notes to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO notes (title, youtube_url, summary_level, notes_content)
        VALUES (?, ?, ?, ?)
    ''', (title, youtube_url, summary_level, notes_content))
    conn.commit()
    conn.close()

def get_all_notes_from_db():
    """Retrieves all notes from the database and returns them as a pandas DataFrame."""
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
        
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM notes ORDER BY created_at DESC", conn)
    conn.close()
    return df

def delete_notes_from_db(note_ids: list):
    """Deletes notes with the given IDs from the database."""
    if not note_ids:
        return
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    placeholders = ','.join('?' for _ in note_ids)
    c.execute(f"DELETE FROM notes WHERE id IN ({placeholders})", note_ids)
    conn.commit()
    conn.close()