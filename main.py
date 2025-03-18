'''
Spot Finder!
Pre-Release

3/14/2025

Project Spot 2025

Keagan, Ayman Faruqi, Lisa Lin, Sameeh


ENSURE API keys are never exposed to the front. Keep keys in seperate files and make sure the file is ignored in git. 
We do not want keys leaked on Github
'''
  
import requests
from dotenv import load_dotenv, dotenv_values
import os
from classes.location import Location, loadObjectFromJson
import json
import sys

'''UI Component imports'''
from PyQt6.QtWidgets import *
from classes.ui.mainwindow import MainWindow


load_dotenv("keys.env") #Loads keys from keys.env | Keys can be accessed with os.genenv("KEYNAME")

clearConsole = lambda: os.system('cls') #Lambda to clear console, call like clearConsole()



def getLocation() -> Location: 
    '''This function uses Google Maps API to get coordinates of location. Can be used for other APIs
    This stuff below basically formats the user input in a way to be inserted into the request
    The address should be formatted like: address=+1600+Jordna+Lane,+Chicago,+Illinois
    Documents: https://developers.google.com/maps/documentation/geocoding/requests-geocoding#json'''

    #Start of user input
    userSearchLocation = input("Please enter a city and or state ('q' to return): ")

    #Sentinel Keyword
    if userSearchLocation == ('q' or 'Q'):
        return

    print("Loading...")

    #Creates location object
    address = userSearchLocation
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
        results = response.json()["results"][0]
        return(Location(address=results["formatted_address"],coordinates=results["geometry"]["location"]))
    else:
        print("API is not responding")
        return

def getWeather(location: Location): #Gets weather of location from coordinates
    #Uses open-meto for weather: https://open-meteo.com/en/docs
    coordinates = location.getCoordinates()
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=temperature_2m&current=temperature_2m,is_day,precipitation&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch")
    location.setTemperature(response.json()["current"]["temperature_2m"])
    location.setPrecipitation(response.json()["current"]["precipitation"])
    location.setCurrentTime(response.json()["current"]["time"][-5:])

def viewPreviousLocations(): #Function to get recent locations
    filePath = "json/cachedLocations.json"
    try: #Opens json file, parses it, and generates the form for the user to select a location
        clearConsole()
        print("Recent Searches: \n---------------------\n\n")
        with open(filePath, "r") as file:
            loadedFile = json.load(file)
            
            emojiList = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

            for i, location in enumerate(loadedFile):
                print(f"{emojiList[i]}: {location["address"]}")
            try:
                userInput = int(input())
            except ValueError: #This occurs if the user does not enter an integer in the input
                clearConsole()
                print("Please enter a number")
                input()
                file.close()
                viewPreviousLocations()
            if userInput >= 0 and userInput < len(loadedFile): #Checks if user input is between 0 and the amount of locations
                clearConsole()
                print(loadObjectFromJson(loadedFile[userInput]))
                file.close()
            else:
                clearConsole()
                print("Please select a valid option")
                input()
                file.close()
                viewPreviousLocations()


    except FileNotFoundError: #This occurs if the user has not searched yet
        clearConsole()
        print("Nothing here yet!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
    # while True:
    #     clearConsole()

    #     print("\n🚀 Welcome to Spot Finder! 🚀\n")
    #     print("Please Choose What You Would Like To Do:\n")
    #     print("1️⃣  Search for a location")
    #     print("2️⃣  View past locations")
    #     print("3️⃣  Quit")

    #     match input(""): #Logic to process users input
    #         case "1":#Search locations
    #             clearConsole()
    #             currentLocation = getLocation()

    #             if currentLocation == None: #If the user quits the search function, go to next iteration
    #                 continue

    #             #Gets weather for the location
    #             getWeather(currentLocation)
    #             clearConsole()
    #             print(currentLocation)
    #             input("\nEnter to continue")
    #             clearConsole()
    #             currentLocation.jsonify()
    #         case "2": #Get most recent locations
    #             clearConsole()
    #             viewPreviousLocations()
    #             input("Press enter to continue")
    #         case "3": #Quit App
    #             clearConsole()
    #             print("Thank you for using Spot Finder!")
    #             break
    #         case _: #Any other input
    #             clearConsole()
    #             print("This is not a valid option.")
    #             input("Press enter to continue")

print("End of program")

