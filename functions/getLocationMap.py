import requests
import shutil
from dotenv import load_dotenv
from classes.location import Location
import os
from functions.logHandler import writeLog

load_dotenv("keys.env")  # Load API keys from the keys.env file


def getLocationMap(location: Location) -> str:
    '''Takes in a location object and uses the coordinates with the Google Maps API
    to generate a map. The map is placed in functions/generatedImages.
    The file name is then returned.'''
    
    writeLog("Getting Map Image")  # Log the start of the map generation process
    
    if not os.path.exists("functions/generatedImages"):
        os.makedirs("functions/generatedImages")

    # Send a request to the Google Maps Static API to generate a map image
    request = requests.get(
        f"https://maps.googleapis.com/maps/api/staticmap?size=350x300&center={location.getCoordinates()[0]},{location.getCoordinates()[1]}&zoom=10&key={os.getenv('GoogleMapsKey')}",
        stream=True
    )

    if request.status_code == 200:  # Check if the request was successful
        # Save the map image to the generatedImages folder
        file_path = f"functions/generatedImages/{location.getCoordinates()[0]},{location.getCoordinates()[1]}.png"
        with open(file_path, 'wb') as f:
            request.raw.decode_content = True  # Ensure the content is decoded properly
            shutil.copyfileobj(request.raw, f)  # Write the image data to the file
        
        writeLog("Done Getting Map Image")  # Log the successful completion
        return file_path  # Return the file path of the generated map image
    else:
        writeLog("Failed To Get Map Image")  # Log the failure
        return "N/A"  # Return "N/A" if the request failed