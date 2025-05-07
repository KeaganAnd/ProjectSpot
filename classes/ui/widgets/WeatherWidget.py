from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class WeatherWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(350, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Horizontal layout for image and temperature
        top_layout = QHBoxLayout()

        # Image label for weather icon
        self.weatherImageLabel = QLabel(self)
        self.weatherImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        self.weatherImageLabel.setScaledContents(True)
        top_layout.addWidget(self.weatherImageLabel)

        # Temperature label
        self.tempLabel = QLabel("Temperature: -°F", self)
        self.tempLabel.setProperty("class","header1")
        self.tempLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.tempLabel)

        # Precipitation label
        self.precipLabel = QLabel("Precipitation: - in", self)
        self.precipLabel.setProperty("class","header3")

        # Set size policies to ensure expansion
        self.weatherImageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tempLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.precipLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set minimum sizes to ensure layout allocation
        self.weatherImageLabel.setMinimumSize(1,1)
        self.tempLabel.setMinimumSize(1,1)
        self.precipLabel.setMinimumSize(1,1)

        # Add layouts to main layout with stretch factors
        main_layout.addLayout(top_layout, stretch=1)  # Top layout takes 50%
        main_layout.addWidget(self.precipLabel, stretch=1) # precip label takes 50%

        # Set horizontal stretch factors for the top layout
        top_layout.setStretch(0, 1)  # weatherImageLabel takes 50%
        top_layout.setStretch(1, 1)  # tempLabel takes 50%

        # Set layout for the QGroupBox
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")

    def updateWeatherLabels(self, location):
        if location != None:
            self.tempLabel.setText(f"{str(int(location.getTemperature()))}°F")
            location.jsonify()
            weatherPixmap = QPixmap('classes/ui/imgs/weatherIcons/sun.png')
            self.weatherImageLabel.setPixmap(weatherPixmap)
            self.precipLabel.setText(f"In the last 7 days: \n{location.getPrecipitation():.2f}in of precipitation")