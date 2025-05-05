from .comparison_database import (
    load_comparison_data,
    add_city_to_comparison,
    delete_city_from_comparison,
    export_comparison_to_csv
)
import datetime

# Get current comparison data
def get_comparison_data():
    return load_comparison_data()

# Add city to comparison (extend with comparison result and timestamp)
def add_city(city, population, gdp, temp, result=None):
    """ Adds a city with additional comparison result and timestamp """
    timestamp = str(datetime.datetime.now())  # Get current timestamp
    return add_city_to_comparison(city, population, gdp, temp, result, timestamp)

# Remove city from comparison
def remove_city(city):
    return delete_city_from_comparison(city)

# Export comparison results to CSV file
def export_comparison(filepath="comparison_export.csv"):
    return export_comparison_to_csv(filepath)

# Compare and save cities, returning the comparison result
def compare_and_save_cities(city1, city2, population1, population2, gdp1, gdp2, temp1, temp2):
    """
    Compares two cities and saves the result.
    """
    # Example of comparison logic (you can extend this as per your requirements)
    result = f"Comparison between {city1} and {city2}: Population Difference: {abs(population1 - population2)}, GDP Difference: {abs(gdp1 - gdp2)}, Temperature Difference: {abs(temp1 - temp2)}"
    
    # Save comparison record to the database
    add_city(city1, population1, gdp1, temp1, result)
    add_city(city2, population2, gdp2, temp2, result)
    
    return result  # Return comparison result
