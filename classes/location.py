import json
import os
from classes.database import get_db_connection

class Location:
    def __init__(self, address: str, country: str = "N/A", state: str = "N/A", coordinates: dict = {"lat":0,"lng":0}, temperature: float = 0.0, precipitation: float = 0.0, currentTime: str = "", population: int = 0):
        self._address = address
        self._coordinates = [coordinates["lat"], coordinates["lng"]]  # In lat/long format
        self._temperature = temperature
        self._precipitation = precipitation
        self._currentTime = currentTime
        self._population = population
        self._country = country
        self._state = state

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
        return self._currentTime
    
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
    
    def jsonify(self): #Adds this location to the json file
        filePath = f"{os.path.join(os.path.dirname(os.path.dirname(__file__)), "cachedLocations.json")}"

        data =  {"address" : self._address, "Coordinates" : self._coordinates, "Temperature" : self._temperature, "Precipitation" : self._precipitation, "Current Time" : self._currentTime, "Country" : self._country, "State" : self._state}
        
        

        try:
            currentLocations = [data]
            with open(filePath, "r") as file:
                loadedFile = json.load(file)

                for location in loadedFile:
                    if location["Coordinates"] != self._coordinates:
                        currentLocations.append(location)
            
            if len(currentLocations) > 4:
                currentLocations.pop(4) #Only allows 10 locations to be saved

            with open(filePath, "w") as file:
                jsonObject = json.dumps(currentLocations, indent=4)
                file.write(jsonObject)

        except FileNotFoundError:
            with open(filePath, "w") as file:
                jsonObject = json.dumps([data], indent=4)
                file.write(jsonObject)
 
        file.close()

def loadObjectFromJson(location : dict): #This function just turns a dict into a Location object used in the get recent locations function in main.py
    return(Location(address=location["address"],coordinates={"lat" : location["Coordinates"][0],"lng" : location["Coordinates"][1]},temperature=location["Temperature"],precipitation=location["Precipitation"],currentTime=location["Current Time"],country=location["Country"], state=location["State"]))

def save_to_db(self):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO locations 
            (formatted_address, latitude, longitude, country, state)
            VALUES (?, ?, ?, ?, ?)
            RETURNING id
        ''', (
            self.address,
            self.coordinates['lat'],
            self.coordinates['lng'],
            self.country,
            self.state
        ))
        self.db_id = cursor.fetchone()[0]
        conn.commit()
        return self.db_id

def save_weather_data(self):
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
            self.temperature,
            self.precipitation,
            self.current_time
        ))
        conn.commit()
        return True