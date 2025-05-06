'''
Spot Finder!
Beta

4/15/2025

Project Spot 2025

Keagan, Ayman Faruqi, Lisa Lin, Sameeh


ENSURE API keys are never exposed to the front. Keep keys in seperate files and make sure the file is ignored in git. 
We do not want keys leaked on Github
'''
  
import requests
from dotenv import load_dotenv
import os
from classes.location import Location
from classes.ui.stylesheet import returnStyleSheet
import sys

'''UI Component imports'''
from PyQt6.QtWidgets import *
from classes.ui.mainwindow import MainWindow

'''DB Components'''
from classes.database import init_db

'''Debug Imports'''
from functions.logHandler import writeLog

'''UUID'''
import uuid


load_dotenv("keys.env") #Loads keys from keys.env | Keys can be accessed with os.genenv("KEYNAME")



def getLocation(location: str) -> Location: 
    '''This function uses Google Maps API to get coordinates of location. Can be used for other APIs
    This stuff below basically formats the user input in a way to be inserted into the request
    The address should be formatted like: address=+1600+Jordna+Lane,+Chicago,+Illinois
    Documents: https://developers.google.com/maps/documentation/geocoding/requests-geocoding#json'''


    writeLog(f"Finding Location {location}...")

    #Creates location object
    address = location
    address = address.lower()
    address = address.split(',')

    if len(address) > 1: #If the user only provides a city or a state so it doesnt throw an error
        city = f"+{address[0].replace(" ","+")}"
        state = f"+{address[1].replace(" ","+")}"
        placeToSearch = f"{city},{state}"
    else:
        placeToSearch = f"+{address[0].replace(" ", "+")}"
    
    
    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={placeToSearch}&key={os.getenv("GoogleMapsKey")}")
    
    #Picks data from the json and creates a Location object
    if response.status_code == 200:
        if len(response.json()["results"]) > 0:
            results = response.json()["results"][0]
            
            country = "N/A"
            state = "N/A"

            for addressComponent in results["address_components"]:
                if addressComponent["types"][0] == "country":
                    country = addressComponent["long_name"]
                elif addressComponent["types"][0] == "administrative_area_level_1":
                    state = addressComponent["long_name"]
            
            writeLog(f"Found Location {location}")
            return(Location(address=results["formatted_address"],coordinates=results["geometry"]["location"],country=country, state=state))
        else:
            writeLog(f"Failed To Find Location {location}")
            return(Location(address="N/A"))
    else:
        writeLog(f"Google Maps API Not Responding")
        return Location(address="N/A")

def getWeather(location: Location): 
    '''Takes in a location object and uses the coordinates to query the API getting current temp 
    and precipitation from the last week. Populates the location object with this info.

    Uses open-meto for weather: https://open-meteo.com/en/docs'''

    writeLog(f"Getting Weather For {location.getAddress()}")

    coordinates = location.getCoordinates()
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=precipitation&current=temperature_2m&timezone=auto&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch")
    
    location.setTemperature(response.json()["current"]["temperature_2m"])

    sevenDayRain = 0.0
    for day in response.json()["hourly"]["precipitation"]: sevenDayRain+=day
    location.setPrecipitation(sevenDayRain)

    location.setCurrentTime(response.json()["current"]["time"][-5:])

    # Save to database
    if hasattr(location, 'save_weather_data'):
        location.save_weather_data()

    writeLog(f"Got Weather For {location.getAddress()}")


if __name__ == "__main__":
    '''Main Loop Handles The UI Setup'''

    writeLog("Program Started")

    #Generates user id if it doesn't already exists simply links to hearts

    with open("user.id", "a+") as file:
        file.seek(0)
        contents = file.read()
        if len(contents) == 0:
            file.write(str(uuid.uuid4()))
        file.close()

    init_db()  # Initialize database when app starts
    app = QApplication(sys.argv)
    app.setStyleSheet(returnStyleSheet())

    window = MainWindow()
    window.show()

    app.exec()


'''Deletes all generated images'''
for item in os.listdir("functions/generatedImages"):
    if item.endswith(".png") or item.endswith(".jpg"):
        os.remove(f"functions/generatedImages/{item}")

writeLog(f"Program Terminated Successfully.")

