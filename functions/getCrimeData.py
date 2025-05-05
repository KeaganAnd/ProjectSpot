import requests
from classes.location import Location
import os
from dotenv import load_dotenv
from functions.logHandler import writeLog

load_dotenv("keys.env")

#This just converts the state saved in the location object into an abbreviation which is needed to search the API
state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

requests.packages.urllib3.util.connection.HAS_IPV6 = False

def getCrimeData(location: Location) -> int:
    '''If the location is in the US then it will return crime statistics for the state.
    Sums up all the violent crimes in 2023 and returns the int
    Uses Census.gov'''
    if location.getCountry() == "United States":
        writeLog("Loading Crime Data")
        
        request = requests.get(f"https://api.usa.gov/crime/fbi/cde/arrest/state/{state_abbreviations[location.getState()]}/all?type=totals&from=01-2023&to=01-2024&API_KEY={os.getenv('FBI')}",timeout=3)

        offenses = request.json()["Offense Name"]

        violentCrimeSum = offenses["Rape"]+offenses["Rape (Legacy)"]+offenses["Robbery"]+offenses["Aggravated Assault"]+offenses["Murder and Nonnegligent Homicide"]+offenses["Manslaughter by Negligence"]

        writeLog("Done Loading Crime Data")
        return(violentCrimeSum)