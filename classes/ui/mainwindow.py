from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

currentLocation = None

class WeatherWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        # Layout inside QGroupBox
        layout = QHBoxLayout(self)

        # Image label for weather icon
        self.weatherImageLabel = QLabel(self)
        self.weatherImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.weatherImageLabel)

        # Temperature label
        self.tempLabel = QLabel("Temperature: 25°C", self)
        layout.addWidget(self.tempLabel)

        # Precipitation label
        self.precipLabel = QLabel("Precipitation: 10%", self)
        layout.addWidget(self.precipLabel)

        # Set layout for the QGroupBox
        self.setLayout(layout)
    
    def updateWeatherLabels(self):
        self.tempLabel.setText(str(currentLocation.getTemperature()))
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.setWindowTitle("Spot Finder")
        self.setMinimumSize(640, 360)
        self.setMaximumSize(1920, 1080)
        self.resize(2560, 1440)


        #!HOME SCREEN

        # Central Widget and Main Layout
        self.centralWidget = QWidget()
        mainLayout = QVBoxLayout(self.centralWidget)

        # Stacked Widget to switch between pages
        self.stacked_widget = QStackedWidget(self.centralWidget)

        # Group Boxes for top and bottom sections
        self.topGroupBox = QGroupBox(self.centralWidget)
        self.bottomGroupBox = QGroupBox(self.centralWidget)

        # Layouts for Group Boxes
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # Set layout spacings
        self.topLayout.setSpacing(0)
        self.bottomLayout.setSpacing(0)

        # Set margins for group boxes and main layout
        self.topGroupBox.setContentsMargins(0, 0, 0, 0)
        self.bottomGroupBox.setContentsMargins(0, 0, 0, 0)
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins between group box and window

        # Create widgets
        self.titleLabel = QLabel("Spot Finder")
        self.searchBar = QLineEdit()
        self.infoBox = QLabel("Bottom Info Box")
        

        # Change widget elements
        self.searchBar.setPlaceholderText("Where's Your Next Spot?")

        # Add Widgets to layouts
        self.topLayout.addWidget(self.titleLabel)
        self.topLayout.addWidget(self.searchBar)
        self.bottomLayout.addWidget(self.infoBox)

        # Set Properties and Alignments
        self.titleLabel.setProperty("class", "header1")
        self.topGroupBox.setProperty("id", "topBox")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setFixedHeight(60)

        # Apply styles
        self.searchBar.setStyleSheet("QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")

        # Add GroupBoxes to the main layout
        mainLayout.addWidget(self.topGroupBox)
        mainLayout.addWidget(self.bottomGroupBox)
        mainLayout.setSpacing(0)

        # Set layout stretch factors
        mainLayout.setStretch(0, 3)
        mainLayout.setStretch(1, 1)
        
        #!Location Page
        self.locationPage = QWidget()
        self.locationMainLayout = QVBoxLayout(self.locationPage)
        self.locationPage.setLayout(self.locationMainLayout)

        # Remove margins and spacing
        self.locationMainLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.locationMainLayout.setSpacing(0)  # No spacing

        # Header section
        self.header = QGroupBox()
        self.locationMainLayout.addWidget(self.header)
        self.header.setMaximumHeight(125)
        self.header.setProperty("class", "header")

        self.headerLayout = QHBoxLayout(self.header)
        self.homeButton = QPushButton("Spot Finder")
        self.searchBar2 = QLineEdit()
        self.headerLayout.addWidget(self.homeButton)
        self.headerLayout.addWidget(self.searchBar2)
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Remove margins and spacing from header layout
        self.headerLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.headerLayout.setSpacing(0)  # No spacing

        self.homeButton.setProperty("class", "homeButton")
        self.homeButton.setMaximumWidth(350)
        self.homeButton.setMinimumHeight(80)
        self.homeButton.clicked.connect(self.switch_to_home_page)

        # Body
        self.locationHead = QGroupBox()
        self.locationHeadLayout = QVBoxLayout(self.locationHead)
        self.locationMainLayout.addWidget(self.locationHead)

        # Remove margins and spacing from location head layout
        self.locationHeadLayout.setContentsMargins(0, 0, 0, 0)
        self.locationHeadLayout.setSpacing(0)

        self.locationName = QLabel("Location Name")
        self.locationHeadLayout.addWidget(self.locationName)
        self.locationHeadLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.locationName.setProperty("class", "header1")

        # Search Bar2
        self.searchBar2.setStyleSheet("QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        self.searchBar2.setPlaceholderText("Where's Your Next Spot?")

        # Weather Widget
        self.weatherWidget = WeatherWidget()
        self.locationMainLayout.addWidget(self.weatherWidget)


        # Set Central Widget
        self.setCentralWidget(self.stacked_widget)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.centralWidget)  # First page
        self.stacked_widget.addWidget(self.locationPage)  # Second page


        # Default page to show
        self.stacked_widget.setCurrentWidget(self.centralWidget)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:  # Check if the Enter key was pressed
            print("Return")
            if len(self.searchBar.text()) > 0: #If the home page bar is typed in
                self.switch_to_second_page()  # Switch to the second page if text is entered
            elif len(self.searchBar2.text()) > 0:
                self.update_location_page()

    def update_location_page(self):
        from main import getLocation
        location = getLocation(self.searchBar2.text())
        self.locationName.setText(location.getAddress())
        self.weatherWidget.updateWeatherLabels()

    def switch_to_second_page(self):
        """Switch to the second page in the stacked widget."""
        from main import getLocation
        location = getLocation(self.searchBar.text())
        self.stacked_widget.setCurrentWidget(self.locationPage)
        print(location.getAddress() == "N/A")
        if location.getAddress() == "N/A":
            self.locationName.setText("Sorry! We weren't able to find this location.")
            self.weatherWidget.updateWeatherLabels()
        else:
            self.locationName.setText(location.getAddress())
            global currentLocation
            currentLocation = location
            self.weatherWidget.updateWeatherLabels()
        self.searchBar.setText("")

    def switch_to_home_page(self):
        self.stacked_widget.setCurrentWidget(self.centralWidget)
        self.searchBar2.setText("")

