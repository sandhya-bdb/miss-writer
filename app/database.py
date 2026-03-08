import sqlite3
import os
import json
from datetime import datetime

# Database file location
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stories.db")

def init_db():
    """Initialize the database and create the stories table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            genre TEXT,
            tone TEXT,
            transcript TEXT,
            themes TEXT,
            emotions TEXT,
            core_ideas TEXT,
            story TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_story(genre: str, tone: str, transcript: str, themes: list[str], emotions: list[str], core_ideas: list[str], story: str):
    """Save a generated story to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    
    # Convert lists to JSON strings for storage
    themes_json = json.dumps(themes)
    emotions_json = json.dumps(emotions)
    core_ideas_json = json.dumps(core_ideas)
    
    cursor.execute('''
        INSERT INTO stories (timestamp, genre, tone, transcript, themes, emotions, core_ideas, story)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, genre, tone, transcript, themes_json, emotions_json, core_ideas_json, story))
    
    conn.commit()
    story_id = cursor.lastrowid
    conn.close()
    return story_id

def get_all_stories():
    """Retrieve all stories from the database, ordered by newest first."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionary-like objects
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stories ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    
    stories = []
    for row in rows:
        story_dict = dict(row)
        # Parse JSON strings back to lists, but cast to Any or Dict to avoid lint errors
        themes = json.loads(story_dict['themes']) if story_dict['themes'] else []
        emotions = json.loads(story_dict['emotions']) if story_dict['emotions'] else []
        core_ideas = json.loads(story_dict['core_ideas']) if story_dict['core_ideas'] else []
        
        # Override the string fields with lists
        story_dict['themes'] = themes # type: ignore
        story_dict['emotions'] = emotions # type: ignore
        story_dict['core_ideas'] = core_ideas # type: ignore
        
        stories.append(story_dict)
        
    return stories
