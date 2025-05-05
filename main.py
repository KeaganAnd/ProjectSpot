'''
Spot Finder!
Beta

4/15/2025

Project Spot 2025

Keagan, Ayman Faruqi, Lisa Lin, Sameeh


ENSURE API keys are never exposed to the front. Keep keys in seperate files and make sure the file is ignored in git. 
We do not want keys leaked on Github
'''
  
import sys
import os
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication

# UI + Logic imports
from classes.location import Location
from classes.ui.stylesheet import returnStyleSheet
from classes.ui.mainwindow import MainWindow  
from classes.database import init_db
from functions.logHandler import writeLog

# Load environment variables from .env file
load_dotenv("keys.env")


# Moved into MainWindow (GUI-based login/register)

def getLocation(location: str) -> Location:
    writeLog(f"Finding Location {location}...")

    address = location.lower().split(',')
    if len(address) > 1:
        city = f"+{address[0].replace(' ', '+')}"
        state = f"+{address[1].replace(' ', '+')}"
        placeToSearch = f"{city},{state}"
    else:
        placeToSearch = f"+{address[0].replace(' ', '+')}"

    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={placeToSearch}&key={os.getenv('GoogleMapsKey')}")

    if response.status_code == 200 and response.json()["results"]:
        results = response.json()["results"][0]
        country = next((c["long_name"] for c in results["address_components"] if "country" in c["types"]), "N/A")
        state = next((s["long_name"] for s in results["address_components"] if "administrative_area_level_1" in s["types"]), "N/A")

        writeLog(f"Found Location {location}")
        return Location(address=results["formatted_address"], coordinates=results["geometry"]["location"], country=country, state=state)
    
    writeLog(f"Failed to find location {location}")
    return Location(address="N/A")

def getWeather(location: Location):
    writeLog(f"Getting Weather For {location.getAddress()}")

    coordinates = location.getCoordinates()
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}"
        f"&hourly=precipitation&current=temperature_2m&timezone=auto&wind_speed_unit=mph"
        f"&temperature_unit=fahrenheit&precipitation_unit=inch"
    )

    data = response.json()
    location.setTemperature(data["current"]["temperature_2m"])
    location.setPrecipitation(sum(data["hourly"]["precipitation"]))
    location.setCurrentTime(data["current"]["time"][-5:])

    if hasattr(location, 'save_weather_data'):
        location.save_weather_data()

    writeLog(f"Got Weather For {location.getAddress()}")

# Main entry point
if __name__ == "__main__":
    writeLog("Program Started")
    
    init_db()  # Initialize database

    app = QApplication(sys.argv)
    app.setStyleSheet(returnStyleSheet())  # Set global styles

    window = MainWindow()  # Launch Main Window
    window.show()

    exit_code = app.exec()  # Start the Qt event loop

    # Clean up generated images
    gen_img_folder = "functions/generatedImages"
    for item in os.listdir(gen_img_folder):
        if item.endswith((".png", ".jpg")):
            os.remove(os.path.join(gen_img_folder, item))

    writeLog("Program Terminated Successfully.")
    sys.exit(exit_code)
