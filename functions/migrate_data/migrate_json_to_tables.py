import json
from classes.database import get_db_connection

def migrate_state_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create supporting tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            fips_code TEXT PRIMARY KEY,
            name TEXT,
            description TEXT
        )''')
        
        # Migrate stateFips.json
        with open('functions/functionData/stateFips.json') as f:
            state_fips = json.load(f)
            for state, fips in state_fips.items():
                cursor.execute('''
                    INSERT OR IGNORE INTO states (fips_code, name)
                    VALUES (?, ?)
                ''', (fips, state))
        
        # Migrate stateDescs.json
        with open('functions/functionData/stateDescs.json') as f:
            state_descs = json.load(f)
            for state, desc in state_descs.items():
                cursor.execute('''
                    UPDATE states SET description = ?
                    WHERE name = ?
                ''', (desc, state))
        
        conn.commit()

if __name__ == "__main__":
    migrate_state_data()
    print("Migration completed!")