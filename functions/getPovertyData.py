import requests
from classes.location import Location
import json
import os
from dotenv import load_dotenv

def getPovertyData(location: Location) -> list:
    '''https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT&for=state:01&YEAR=2023
    
    https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html

    Refrence for variable names:
    https://api.census.gov/data/timeseries/poverty/saipe/variables.html
    '''
    load_dotenv("keys.env")
    if location.getCountry() == "United States":
        print("Loading Poverty Data")
        print(location.getCountry())
        with open("functions/functionData/stateFips.json", "r") as file:
            fipsDict = json.load(file) #Loads the dictionary of state codes needed for API

            try:
                stateID = fipsDict[location.getState()]
            except KeyError:
                return(["Error"])
                

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Host": "api.census.gov",
                "Priority": "u=0, i",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
            }
            
            

            request = requests.get(f"https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT&for=state:{stateID}&YEAR=2023&key={os.getenv("USCensus")}", headers=headers, timeout=.5)
            print("Done Loading Poverty Data")
            return(request.json())
        

