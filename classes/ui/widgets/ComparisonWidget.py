from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from .WeatherWidget import WeatherWidget
from .PovertyWidget import PovertyWidget
from .MapWidget import MapWidget
from .CrimeWidgets import CrimeWidget
from .DescriptionWidget import DescriptionWidget

class ComparisonWidget(QWidget):
    def __init__(self, homeWidget, locationWidget, mainWindow):
        super().__init__()
        self.homeWidget = homeWidget
        self.mainWindow = mainWindow
        self.locationWidget = locationWidget
        self.currentLocation = None


        self.locationMainLayout = QVBoxLayout(self)
        self.setLayout(self.locationMainLayout)
        self.locationMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Remove margins and spacing
        self.locationMainLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.locationMainLayout.setSpacing(0)  # No spacing

        # Header section
        self.header = QGroupBox()
        self.locationMainLayout.addWidget(self.header)
        self.header.setMaximumHeight(100)
        self.header.setProperty("class", "header")

        self.headerLayout = QHBoxLayout(self.header)
        self.homeButton = QPushButton("Spot Finder")
        self.searchBar3 = QLineEdit()
        self.headerLayout.addWidget(self.homeButton)
        self.headerLayout.addWidget(self.searchBar3)
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Remove margins and spacing from header layout
        self.headerLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.headerLayout.setSpacing(0)  # No spacing

        self.homeButton.setProperty("class", "homeButton")
        self.homeButton.setMaximumWidth(350)
        self.homeButton.setMinimumHeight(80)
        self.homeButton.clicked.connect(self.switch_to_home)

        # Body
        self.locationHead = QGroupBox()
        self.locationHead.setMaximumHeight(60)
        self.locationHeadLayout = QHBoxLayout(self.locationHead)  # Use QHBoxLayout for left and right alignment
        self.locationMainLayout.addWidget(self.locationHead)

        # Remove margins and spacing from location head layout
        self.locationHeadLayout.setContentsMargins(0, 0, 0, 0)
        self.locationHeadLayout.setSpacing(0)

        # Left-aligned location name
        self.leftLocationName = QLabel("Left Location Name")
        self.leftLocationName.setProperty("class", "header1")
        self.leftLocationName.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.locationHeadLayout.addWidget(self.leftLocationName)
        self.leftLocationName.setStyleSheet("padding-left: 10px")

        # Spacer to push the right location name to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.locationHeadLayout.addItem(spacer)

        # Right-aligned location name
        self.rightLocationName = QLabel("Right Location Name")
        self.rightLocationName.setProperty("class", "header1")
        self.rightLocationName.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.locationHeadLayout.addWidget(self.rightLocationName)
        self.rightLocationName.setStyleSheet("padding-right: 10px")

        # Search Bar3
        self.searchBar3.setStyleSheet("QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        self.searchBar3.setPlaceholderText("Where's Your Next Spot?")

        # Widget Container
        # Group box
        group_box = QGroupBox("")
        group_layout = QHBoxLayout(group_box)

        # Combine content1 and content2 into a single scrollable frame
        combined_frame = QFrame()
        combined_layout = QHBoxLayout(combined_frame)
        combined_frame.setStyleSheet("background-color: transparent")

        # First content (content1)
        content1 = QFrame()
        content1_layout = QVBoxLayout(content1)
        content1_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Loc1 Widgets
        self.widgets = {
            "loc1Weather": WeatherWidget(),
            "loc1Map": MapWidget(),
            "loc1Poverty": PovertyWidget(),
            "loc1Crime": CrimeWidget(),
            "loc1Desc": DescriptionWidget()
        }
        # Add widgets to content1
        for varName, value in self.widgets.items():
            value.setMinimumSize(300, 300)
            value.setMaximumSize(300, 300)
            content1_layout.addWidget(value)

        # Second content (content2)
        content2 = QFrame()
        content2_layout = QVBoxLayout(content2)
        content2_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Loc2 Widgets
        self.widgets2 = {
            "loc1Weather": WeatherWidget(),
            "loc1Map": MapWidget(),
            "loc1Poverty": PovertyWidget(),
            "loc1Crime": CrimeWidget(),
            "loc1Desc": DescriptionWidget()
        }
        # Add widgets to content2
        for varName, value in self.widgets2.items():
            value.setMinimumSize(300, 300)
            value.setMaximumSize(300, 300)
            content2_layout.addWidget(value)



        # Third content (content3)
        content3 = QFrame()
        content3_layout = QVBoxLayout(content3)
        content3_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # In Between Widgets
        self.widgets3 = {
            "loc1Weather": WeatherWidget(),
            "loc1Map": MapWidget(),
            "loc1Poverty": PovertyWidget(),
            "loc1Crime": CrimeWidget(),
            "loc1Desc": DescriptionWidget()
        }



        # Add widgets to content3
        for varName, value in self.widgets3.items():
            value.setMinimumSize(300, 300)
            value.setMaximumSize(300, 300)
            content3_layout.addWidget(value)

        # Add content1 and content3 to the combined layout
        combined_layout.addWidget(content1)
        combined_layout.addWidget(content3)
        combined_layout.addWidget(content2)

        # Create a single scroll area for the combined frame
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(combined_frame)
        scroll_area.setStyleSheet("QScrollArea {background: transparent; border: none;}")

        # Add the scroll area to the group box layout
        group_layout.addWidget(scroll_area)

        # Add group box to main layout
        self.locationMainLayout.addWidget(group_box)

    def switch_to_home(self):
        self.mainWindow.stacked_widget.setCurrentWidget(self.homeWidget)
        self.mainWindow.titleLabel.setText("Spot Finder")

    def switch_to_another_widget(self):
        global likeLocation
        likeLocation = False
        self.mainWindow.stacked_widget.setCurrentWidget(self.mainWindow.centralWidget)
        

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:  # Check if the Enter key was pressed
            from main import getLocation
            if len(self.searchBar3.text()) > 0:
                self.mainWindow.searchBar2.setText(self.searchBar3.text())
                self.mainWindow.update_location_page()
                self.mainWindow.searchBar2.setText("")
                self.switch_to_another_widget(self.locationWidget)

    def setCurrentLocation(self, currentLocation):
        self.currentLocation = currentLocation

    def updateLabels(self, newLocation, currentLocation):
        self.currentLocation = currentLocation
        self.leftLocationName.setText(self.currentLocation.getAddress())

        for varName, widget in self.widgets.items():
            if isinstance(widget, WeatherWidget):
                widget.updateWeatherLabels(self.currentLocation)
            elif isinstance(widget, MapWidget):
                widget.updateMap(self.currentLocation)
            elif isinstance(widget, PovertyWidget):
                widget.updateLabels(self.currentLocation)
            elif isinstance(widget, DescriptionWidget):
                widget.updateLabel(self.currentLocation)
            elif isinstance(widget, CrimeWidget):
                widget.updateCrime(self.currentLocation)

        from main import getWeather
        from functions.getCrimeData import getCrimeData
        from functions.getPovertyData import getPovertyData

        
        getCrimeData(newLocation)
        getPovertyData(newLocation)
        getWeather(newLocation)

        self.rightLocationName.setText(newLocation.getAddress())
        for varName, widget in self.widgets2.items():
            if isinstance(widget, WeatherWidget):
                widget.updateWeatherLabels(newLocation)
            elif isinstance(widget, MapWidget):
                widget.updateMap(newLocation)
            elif isinstance(widget, PovertyWidget):
                widget.updateLabels(newLocation)
            elif isinstance(widget, DescriptionWidget):
                widget.updateLabel(newLocation)
            elif isinstance(widget, CrimeWidget):
                widget.updateCrime(newLocation)

        
        for varName, widget in self.widgets3.items():
            if isinstance(widget, WeatherWidget):
                print(f"Test: {self.widgets2["loc1Weather"].tempLabel.text()[:-2]}")
                difference = int(self.widgets2["loc1Weather"].tempLabel.text()[:-2]) - int(self.widgets["loc1Weather"].tempLabel.text()[:-2])
                widget.tempLabel.setText(f"{str(abs(difference))}")
            elif isinstance(widget, MapWidget):
                pass
            elif isinstance(widget, PovertyWidget):
                pass
            elif isinstance(widget, DescriptionWidget):
                pass
            elif isinstance(widget, CrimeWidget):
                pass