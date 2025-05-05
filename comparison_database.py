import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.join("data", "comparison.db")

# Initialize the database and create the comparison table with the new columns
def init_comparison_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comparison (
            city TEXT,
            population INTEGER,
            gdp_per_capita REAL,
            avg_temp REAL,
            comparison_result TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add city and comparison result to the database
def add_city_to_comparison(city, population, gdp, temp, result, timestamp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comparison (city, population, gdp_per_capita, avg_temp, comparison_result, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (city, population, gdp, temp, result, timestamp))
    conn.commit()
    conn.close()

# Load all comparison data from the database
def load_comparison_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT city, population, gdp_per_capita, avg_temp, comparison_result, timestamp FROM comparison")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Delete a city from the comparison data
def delete_city_from_comparison(city):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comparison WHERE city = ?", (city,))
    conn.commit()
    conn.close()

# Export comparison data to a CSV file
def export_comparison_to_csv(filepath="comparison_export.csv"):
    data = load_comparison_data()
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["City", "Population", "GDP per Capita", "Avg Temp", "Comparison Result", "Timestamp"])
        writer.writerows(data)
