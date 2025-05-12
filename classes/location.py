import json
import os
from classes.database import get_db_connection

class Location:
    def __init__(self, address: str, country: str = "N/A", state: str = "N/A", coordinates: dict = {"lat": 0, "lng": 0}, temperature: float = 0.0, precipitation: float = 0.0, currentTime: str = "", population: int = 0):
        self._address = address
        self._coordinates = [coordinates["lat"], coordinates["lng"]]  # Latitude and longitude
        self._temperature = temperature
        self._precipitation = precipitation
        self._currentTime = currentTime
        self._population = population
        self._country = country
        self._state = state
        self.db_id = None  # Database ID for the location

    # Getters
    def getAddress(self) -> str:
        return self._address

    def getCoordinates(self) -> list:
        return self._coordinates

    def getTemperature(self) -> float:
        return self._temperature

    def getPrecipitation(self) -> float:
        return self._precipitation

    def getCurrentTime(self) -> str:
        return self._currentTime

    def getPopulation(self) -> int:
        return self._population

    def getCountry(self) -> str:
        return self._country

    def getState(self) -> str:
        return self._state

    # Setters
    def setAddress(self, address: str):
        self._address = address

    def setCoordinates(self, lat: float, lng: float):
        self._coordinates = [lat, lng]

    def setTemperature(self, temperature: float):
        self._temperature = temperature

    def setPrecipitation(self, precipitation: float):
        self._precipitation = precipitation

    def setCurrentTime(self, current_time: str):
        self._currentTime = current_time

    def setCountry(self, country: str):
        self._country = country

    def setState(self, state: str):
        self._state = state

    def __str__(self):
        return (f"Report For: {self._address}:\n------------------------\n"
                f"Coordinates: {self._coordinates}\n"
                f"Temperature: {self._temperature}\n"
                f"Precipitation: {self._precipitation}\n"
                f"Current Time: {self._currentTime}")




        

    def save_to_db(self, currentUser):
        """Saves the location to the database."""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 1. Check if the row already exists
            cursor.execute("""
                SELECT id FROM locations
                WHERE formatted_address = ?
                AND latitude = ?
                AND longitude = ?
                AND country = ?
                AND state = ?
            """, (
                self._address,
                self._coordinates[0],
                self._coordinates[1],
                self._country,
                self._state
            ))

            row = cursor.fetchone()

            if row:
                self.db_id = row[0]
            else:
                # 2. Insert and get the new ID
                cursor.execute("""
                    INSERT INTO locations (formatted_address, latitude, longitude, country, state)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    self._address,
                    self._coordinates[0],
                    self._coordinates[1],
                    self._country,
                    self._state
                ))
                self.db_id = cursor.lastrowid


            cursor.execute("""
            INSERT OR IGNORE INTO searches (username, location_id)
            VALUES (?, ?);
            """, (currentUser, self.db_id))

            conn.commit()
            return self.db_id

    def save_weather_data(self):
        """Saves weather data for the location to the database."""
        if not self.db_id:
            return False

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO weather_data
                (location_id, temperature, precipitation, observation_time)
                VALUES (?, ?, ?, ?)
            ''', (
                self.db_id,
                self._temperature,
                self._precipitation,
                self._currentTime
            ))
            conn.commit()
            return True

def loadObjectFromJson(location: dict) -> Location:
    """Converts a dictionary into a Location object."""
    return Location(
        address=location["address"],
        coordinates={"lat": location["Coordinates"][0], "lng": location["Coordinates"][1]},
        temperature=location["Temperature"],
        precipitation=location["Precipitation"],
        currentTime=location["Current Time"],
        country=location["Country"],
        state=location["State"]
    )