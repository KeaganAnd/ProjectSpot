from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class PovertyWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(350, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)


        # Image label for weather icon
        self.medianIncomeLabel = QLabel("Median Income:",self)
        self.medianIncomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.medianIncomeLabel.setProperty("class","boldBody")
        self.medianIncomeLabel.setWordWrap(True)

        
        main_layout.addWidget(self.medianIncomeLabel)

        # Temperature label
        self.peopleInPovertyLabel = QLabel("People In Poverty:", self)
        self.peopleInPovertyLabel.setProperty("class","boldBody")
        self.peopleInPovertyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.peopleInPovertyLabel.setWordWrap(True)
        main_layout.addWidget(self.peopleInPovertyLabel)



        # Set size policies to ensure expansion
        self.medianIncomeLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.peopleInPovertyLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
      

        # Set minimum sizes to ensure layout allocation
        self.medianIncomeLabel.setMinimumSize(1,1)
        self.peopleInPovertyLabel.setMinimumSize(1,1)

        # Set layout for the QGroupBox
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")

    def updateLabels(self, location):
        if location.getCountry() == "United States":
            from functions.getPovertyData import getPovertyData
            data = getPovertyData(location)
            self.medianIncomeLabel.setText(f"Median Income: ${int(data[1][1]):,}")
            self.peopleInPovertyLabel.setText(f"People In Poverty: {int(data[1][2]):,}")
        else:
            self.medianIncomeLabel.setText("Sorry, economic information is only available within the USA.")
            self.peopleInPovertyLabel.setText("")