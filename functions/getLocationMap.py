import requests
import shutil
from dotenv import load_dotenv
from classes.location import Location
import os

load_dotenv("keys.env")


def getLocationMap(location: Location) -> str:
    '''Takes in a location object and uses the coordinates with the Google Maps API
    to generate a map. The map is placed in functions/generatedImages.
    The file name is then returned'''
    request = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=350x300&center={location.getCoordinates()[0]},{location.getCoordinates()[1]}&zoom=10&key={os.getenv("GoogleMapsKey")}", stream=True)



    if request.status_code == 200:
        with open(f"functions/generatedImages/{location.getCoordinates()[0],location.getCoordinates()[1]}.png", 'wb') as f:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, f)   
        return(f"functions/generatedImages/{location.getCoordinates()[0],location.getCoordinates()[1]}.png")
    else:
        return("N/A")

