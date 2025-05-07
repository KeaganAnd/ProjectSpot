from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MapWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(350, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Image label for weather icon
        self.mapImageLabel = QLabel(self)
        self.mapImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        
        self.mapImageLabel.setScaledContents(True)
        main_layout.addWidget(self.mapImageLabel)

        
        self.mapImageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
       
        self.mapImageLabel.setMinimumSize(1,1)
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")

    def updateMap(self, location):
        from functions.getLocationMap import getLocationMap
        mapLocation = getLocationMap(location)

        weatherPixmap = QPixmap(mapLocation)
        self.mapImageLabel.setPixmap(weatherPixmap)
        print("Map Updated")