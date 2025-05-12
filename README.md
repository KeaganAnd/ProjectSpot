# Spot Finder
Team Spot 2025

Run *main.py*

# Installation Instructions

1. Install [Python](https://www.python.org/downloads/release/python-3133/) (3.13.3 is the version this was created on).
   If you **do not** already have python installed you will need to restart your computer afterwards.
2. Download source code from [here](https://github.com/KeaganAnd/ProjectSpot).
   1. On the top right click the green *Code* button.
   2. Click "Download Zip"
3. Extract the downloaded Zip file to a folder where you will use it.
4. Open your new folder.
5. Run `setupRequirements.bat`. 
   Windows may mark this file as unsafe since it is a .bat file. If this happens follow the steps below
   1. Click "More info"
   2. Click "Run Anyway"
   Read more below about what this file does or continue to step 6.
   *Advanced Instructions*
        This file simply runs a pip command to download the required python modules which can be viewed in `requirements.txt`. Then makes a file called "keys.env" which is used later in the setup.
6. Wait until the command window dissapears, this means setup is complete.
7. Open `keys.env` in notepad
8. Get API keys
   Since this apps makes use of APIs you will need to get keys for them. You will need four.
   1. [Google Maps](https://console.cloud.google.com/apis/credentials) 
   2. [US Census](https://api.census.gov/data/key_signup.html)
   3. [Gemini](https://aistudio.google.com/app/apikey)
   4. FBI key is a public key and you can use the one in this code
   In the `keys.env` file paste this code.
   ```env
    GoogleMapsKey=KEY
    USCensus=KEY
    FBI=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv
    GEMINI=KEY
   ``` 
9.  click `run.bat` which will start the program
    Or alternatively from the command line you can run `python -u main.py`


# Notes

inspectWindow.bat

Opens the ui in a chrome dev tools type environment