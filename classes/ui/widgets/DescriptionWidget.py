from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import json
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

from google import genai #Import Google Gemini API
from functions.logHandler import writeLog

class DescriptionWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(600, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Image label for weather icon
        self.descLabel = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", self)
        self.descLabel.setWordWrap(True)
        self.descLabel.setProperty("class","boldBody")


        
        
        self.descLabel.setScaledContents(True)
        main_layout.addWidget(self.descLabel)

        
        self.descLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
       
        self.descLabel.setMinimumSize(1,1)
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")

    def updateLabel(self, location):

        if location.getCountry() == "United States":
            with open("functions/functionData/stateDescs.json") as file:
                data = json.load(file)
                self.descLabel.setText(data[location.getState()])
            
            writeLog("Description Label Updated")
        elif location.getAddress() != "N/A":
            client = genai.Client(api_key=os.getenv("GEMINI"))

            response = client.models.generate_content(
                model="gemini-1.5-flash", contents=f"Write a description about {location.getAddress()} the description should be 75 words or less. It should include details about the weather, geography, culture, and safety of the state"
            )
            self.descLabel.setText(response.text)
        else:
            self.descLabel.setText("We could not find this location")