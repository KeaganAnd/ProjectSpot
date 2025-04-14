import requests
import shutil
from dotenv import load_dotenv
from classes.location import Location
import os

load_dotenv("keys.env")


def getLocationMap(location: Location) -> str:
    '''https://maps.googleapis.com/maps/api/staticmap?size=500x500&center=40.714728,-73.998672&zoom=10&key=AIzaSyA_GXuUVDpkZJRJ5yMsbRE3t--TFh01r1w'''
    request = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?size=350x300&center={location.getCoordinates()[0]},{location.getCoordinates()[1]}&zoom=10&key={os.getenv("GoogleMapsKey")}", stream=True)



    if request.status_code == 200:
        with open(f"functions/generatedImages/{location.getCoordinates()[0],location.getCoordinates()[1]}.png", 'wb') as f:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, f)   
        return(f"functions/generatedImages/{location.getCoordinates()[0],location.getCoordinates()[1]}.png")
    else:
        return("N/A")

