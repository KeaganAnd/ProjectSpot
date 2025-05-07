import json
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class LocationWidget(QGroupBox):
    '''The location widgets to recall previous locations on the home page'''
    locationClickedSignal = pyqtSignal(str) # Define the signal

    def __init__(self, type = "normal", mainObj = None):
        super().__init__("")
        self.setMaximumWidth(400)
        self.setProperty("class", "locationInfoWidget")

        self._type = type
        self._mainObj = mainObj

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Horizontal layout for image and temperature
        top_layout = QHBoxLayout()



        #Top Label
        self.nameLabel = QPushButton("Location", self)
        self.nameLabel.setProperty("class","header1")
        self.nameLabel.setProperty("class2","locationButton")
        top_layout.addWidget(self.nameLabel)

        # Precipitation label
        self.restOfAddLabel = QLabel("Precipitation: - in", self)
        self.restOfAddLabel.setProperty("class","header3")

        # Set size policies to ensure expansion
        self.nameLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.restOfAddLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set minimum sizes to ensure layout allocation
        self.nameLabel.setMinimumSize(1,1)
        self.restOfAddLabel.setMinimumSize(1,1)

        # Add layouts to main layout with stretch factors
        main_layout.addLayout(top_layout, stretch=1)  # Top layout takes 50%
        main_layout.addWidget(self.restOfAddLabel, stretch=1) # precip label takes 50%

        # Set horizontal stretch factors for the top layout
        top_layout.setStretch(0, 1)  # weatherImageLabel takes 50%
        top_layout.setStretch(1, 1)  # nameLabel takes 50%

        self.nameLabel.clicked.connect(self.clickedLocationBudget)

        # Set layout for the QGroupBox
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")


    
    def clickedLocationBudget(self):
        if self._type == "normal":
            try:
                with open("cachedLocations.json", "r") as file:
                    loadedFile = json.load(file)

                    for location in loadedFile:
                        if location["address"].find(self.nameLabel.text()) != -1:
                            self.locationClickedSignal.emit(self.nameLabel.text()) # Emit signal
                            return #stop searching after finding the first match
            except FileNotFoundError:
                pass
        else:
            self._mainObj.searchBar.setText(self.nameLabel.text())
            self._mainObj.switch_to_second_page()
            global likeLocation
            likeLocation = True
            

    def updateLocationLabels(self, location, menuButton = False):
        if not menuButton:
            if location.getAddress().find(",") != -1:
                self.nameLabel.setText(location.getAddress()[:location.getAddress().find(",")])
                self.restOfAddLabel.setText(location.getAddress()[location.getAddress().find(",")+2:])
            else:
                self.nameLabel.setText(location.getAddress())
                self.restOfAddLabel.setText("")
        else:
            self.nameLabel.setText("Liked Locations")
            self.restOfAddLabel.setText("View liked locations here")
            self.setStyleSheet("[class2=\"locationButton\"]:hover {color: #FFC0CB}")