import requests
from classes.location import Location
import json
import os
from dotenv import load_dotenv
from functions.logHandler import writeLog

requests.packages.urllib3.util.connection.HAS_IPV6 = False  # Disable IPv6 for requests

def getPovertyData(location: Location) -> list:
    '''Fetches poverty data for a given location using the US Census API.

    API Reference:
    https://api.census.gov/data/timeseries/poverty/saipe
    Variable Reference:
    https://api.census.gov/data/timeseries/poverty/saipe/variables.html
    '''
    load_dotenv("keys.env")  # Load API keys from the keys.env file

    if location.getCountry() == "United States":  # Ensure the location is in the US
        writeLog("Loading Poverty Data")  # Log the start of the data loading process
        
        # Load the dictionary of state FIPS codes
        with open("functions/functionData/stateFips.json", "r") as file:
            fipsDict = json.load(file)

            try:
                stateID = fipsDict[location.getState()]  # Get the FIPS code for the state
            except KeyError:
                writeLog("Failed Getting Poverty Data: Location Object Missing A State")  # Log missing state error
                return ["Error"]  # Return error if state is missing



            try:
                # Send a GET request to the US Census API
                request = requests.get(
                    f"https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT&for=state:{stateID}&YEAR=2023&key={os.getenv('USCensus')}",
                    timeout=15
                )
                if request.status_code == 200:  # Check if the request was successful
                    writeLog("Done Loading Poverty Data")  # Log success
                    return request.json()  # Return the JSON response
                else:
                    writeLog("Error Loading Poverty Data | Cannot Connect To API")  # Log API connection error
                    return []  # Return an empty list on failure
            except requests.exceptions.Timeout:
                writeLog("Poverty Data Timed Out")  # Log timeout error
                return []  # Return an empty list on timeout