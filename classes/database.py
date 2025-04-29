import sqlite3
from contextlib import contextmanager

DATABASE = 'spot_finder.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            formatted_address TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            country TEXT,
            state TEXT,
            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            temperature REAL,
            precipitation REAL,
            observation_time TEXT,
            FOREIGN KEY (location_id) REFERENCES locations(id)
        )''')
        
        conn.commit()

def load_location_data(location_id):
    """Load complete saved location data from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get base location info
        cursor.execute('''
            SELECT l.*, w.temperature, w.precipitation, 
                   c.violent_crime_rate, p.poverty_rate
            FROM locations l
            LEFT JOIN weather_data w ON l.id = w.location_id
            LEFT JOIN crime_data c ON l.id = c.location_id
            LEFT JOIN poverty_data p ON l.id = p.location_id
            WHERE l.id = ?
        ''', (location_id,))
        
        result = cursor.fetchone()
        if not result:
            return None
            
        # Convert to dictionary for easier use
        return dict(result)
        