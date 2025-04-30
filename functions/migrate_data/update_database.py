from classes.database import get_db_connection

def get_search_history(limit=10):
    """Get formatted search history for UI"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                l.id,
                l.formatted_address,
                l.search_date,
                w.temperature,
                c.violent_crime_rate
            FROM locations l
            LEFT JOIN weather_data w ON l.id = w.location_id
            LEFT JOIN crime_data c ON l.id = c.location_id
            ORDER BY l.search_date DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]