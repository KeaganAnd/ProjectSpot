import json
from classes.database import get_db_connection

def migrate_state_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create supporting tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            fips_code TEXT PRIMARY KEY,   -- FIPS code as the primary key
            name TEXT,                    -- Name of the state
            description TEXT              -- Description of the state
        )''')
        
        # Migrate stateFips.json
        with open('functions/functionData/stateFips.json') as f:
            state_fips = json.load(f)     # Load state FIPS data from JSON
            for state, fips in state_fips.items():
                cursor.execute('''
                    INSERT OR IGNORE INTO states (fips_code, name)
                    VALUES (?, ?)         -- Insert FIPS code and state name
                ''', (fips, state))
        
        # Migrate stateDescs.json
        with open('functions/functionData/stateDescs.json') as f:
            state_descs = json.load(f)    # Load state descriptions from JSON
            for state, desc in state_descs.items():
                cursor.execute('''
                    UPDATE states SET description = ?
                    WHERE name = ?       -- Update state description based on name
                ''', (desc, state))
        
        conn.commit()                     # Commit all changes to the database

if __name__ == "__main__":
    migrate_state_data()                  # Run the migration function
    print("Migration completed!")         # Print confirmation message