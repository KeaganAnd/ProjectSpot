from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class CrimeWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(350, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        #Crime Icon
        self.crimeIconLabel = QLabel()
        crimeIcon = QPixmap("classes/ui/imgs/crime.png")

        self.crimeIconLabel.setPixmap(crimeIcon.scaled(100,100))
        self.crimeIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.crimeIconLabel)

        # Label for violent crimes
        self.violentCrimesLabel = QLabel(self)
        self.violentCrimesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.violentCrimesLabel.setWordWrap(True)
        self.violentCrimesLabel.setProperty("class","boldBody")

        
        
        self.violentCrimesLabel.setScaledContents(True)
        main_layout.addWidget(self.violentCrimesLabel)

        
        self.violentCrimesLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
       
        self.violentCrimesLabel.setMinimumSize(1,1)
        self.setLayout(main_layout)
        self.setStyleSheet("[class=\"locationInfoWidget\"] {padding: 5px 5px 5px 5px;} ")

    def updateCrime(self, location):
        if location.getCountry() == "USA" or location.getCountry() == "United States":
            from functions.getCrimeData import getCrimeData
            self.violentCrimesLabel.setText(f"Violent Crimes In 2023: {getCrimeData(location)}")
        else:
            self.violentCrimesLabel.setText("Sorry, this widget is only available within the USA.")