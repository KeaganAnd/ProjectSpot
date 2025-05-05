from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from ..location import loadObjectFromJson
from ..location import Location
import json

currentLocation = None

mode = "new" #Mode can be new which searches for a completely new location and "compare" will search a location to compare
likeLocation = False
currentUser = None






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

        
        main_layout.addWidget(self.medianIncomeLabel)

        # Temperature label
        self.peopleInPovertyLabel = QLabel("People In Poverty:", self)
        self.peopleInPovertyLabel.setProperty("class","boldBody")
        self.peopleInPovertyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            
            print("Description Label Updated")

class CrimeWidget(QGroupBox):
    def __init__(self):
        super().__init__("")
        self.setMaximumSize(350, 300)
        self.setProperty("class", "locationInfoWidget")
        

        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Image label for weather icon
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
        from functions.getCrimeData import getCrimeData
        self.violentCrimesLabel.setText(f"Violent Crimes In 2023: {getCrimeData(location)}")

class LikesWidget(QWidget):
    def __init__(self, homeWidget, locationWidget, mainWindow):
        super().__init__()
        self.homeWidget = homeWidget
        self.mainWindow = mainWindow
        self.locationWidget = locationWidget
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
        self.homeButton.clicked.connect(self.switch_to_another_widget)

        # Body
        self.locationHead = QGroupBox()
        self.locationHead.setMaximumHeight(60)
        self.locationHeadLayout = QHBoxLayout(self.locationHead)  # Use QHBoxLayout for left and right alignment
        self.locationMainLayout.addWidget(self.locationHead)

        # Remove margins and spacing from location head layout
        self.locationHeadLayout.setContentsMargins(0, 0, 0, 0)
        self.locationHeadLayout.setSpacing(0)

        # Search Bar3
        self.searchBar3.setStyleSheet("QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        self.searchBar3.setPlaceholderText("Where's Your Next Spot?")

        # Widget Container
        # Group box
        group_box = QGroupBox("")
        group_layout = QVBoxLayout(group_box)

        # Combine content1 and content2 into a single scrollable frame
        combined_frame = QFrame()
        self.combined_layout = QVBoxLayout(combined_frame)
        combined_frame.setStyleSheet("background-color: transparent")

        combined_frame.setContentsMargins(0, 0, 0, 0)

        self.combined_layout.setContentsMargins(0, 0, 0, 0)
        self.combined_layout.setSpacing(0)

        # Create a single scroll area for the combined frame
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(combined_frame)
        scroll_area.setStyleSheet("QScrollArea {background: transparent; border: none;}")

        scroll_area.setContentsMargins(0, 0, 0, 0)

        # Add the scroll area to the group box layout
        self.titleLabel = QLabel("Liked Locations")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setProperty("class","header1")
        group_layout.addWidget(self.titleLabel)
        group_layout.addWidget(scroll_area)

        # Add group box to main layout
        self.locationMainLayout.addWidget(group_box)

    def switch_to_another_widget(self):
        global likeLocation
        likeLocation = False
        self.mainWindow.stacked_widget.setCurrentWidget(self.mainWindow.centralWidget)

    def populateLocations(self):
        clear_layout(self.combined_layout)
        with open("heartDB.json", "r") as file:
            content = json.load(file)
            for location in content:
                if currentUser in location["likers"]:
                    newLocationWidget = LocationWidget(mainObj=self.mainWindow, type="button")
                    newLocationWidget.nameLabel.setText(location["address"])
                    newLocationWidget.restOfAddLabel.setText("")
                    self.combined_layout.addWidget(newLocationWidget)
                    newLocationWidget.setMaximumHeight(150)
                    newLocationWidget.setMaximumWidth(100000)
                    newLocationWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    newLocationWidget.setContentsMargins(0, 0, 0, 0)
                    

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:  # Check if the Enter key was pressed
            from main import getLocation
            if len(self.searchBar3.text()) > 0:
                self.mainWindow.searchBar2.setText(self.searchBar3.text())
                self.mainWindow.update_location_page()
                self.mainWindow.searchBar2.setText("")
                self.switch_to_another_widget(self.locationWidget)
  
class ComparisonWidget(QWidget):
    def __init__(self, homeWidget, locationWidget, mainWindow):
        super().__init__()
        self.homeWidget = homeWidget
        self.mainWindow = mainWindow
        self.locationWidget = locationWidget
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

        # Add content1 and content2 to the combined layout
        combined_layout.addWidget(content1)
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
        self.switch_to_another_widget(self.homeWidget)

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

    
    def updateLabels(self, newLocation):
        self.leftLocationName.setText(currentLocation.getAddress())

        for varName, widget in self.widgets.items():
            if isinstance(widget, WeatherWidget):
                widget.updateWeatherLabels(currentLocation)
            elif isinstance(widget, MapWidget):
                widget.updateMap(currentLocation)
            elif isinstance(widget, PovertyWidget):
                widget.updateLabels(currentLocation)
            elif isinstance(widget, DescriptionWidget):
                widget.updateLabel(currentLocation)
            elif isinstance(widget, CrimeWidget):
                widget.updateCrime(currentLocation)

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
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("user.id", "r") as file:
            global currentUser
            currentUser = file.read()
            file.close()

        # Window setup
        self.setWindowTitle("Spot Finder")
        self.setMaximumSize(1920,1080)
        self.setMinimumSize(1440,932)
        self.setWindowIcon(QIcon('classes/ui/imgs/searchIcon.png'))


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
        self.bottomLayout = QHBoxLayout()
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
        self.loadingLabel = QLabel("Loading...")
        self.stacked_widget.addWidget(self.loadingLabel)
        
        self.createLocationWidgets()
        

        # Change widget elements
        self.searchBar.setPlaceholderText("Where's Your Next Spot?")

        # Add Widgets to layouts
        self.topLayout.addWidget(self.titleLabel)
        self.topLayout.addWidget(self.searchBar)

        # Set Properties and Alignments
        self.titleLabel.setProperty("class", "header1")
        self.topGroupBox.setProperty("id", "topBox")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
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
        self.locationHead.setMaximumHeight(60)
        self.locationHeadLayout = QVBoxLayout(self.locationHead)
        self.locationMainLayout.addWidget(self.locationHead)
        

        # Remove margins and spacing from location head layout
        self.locationHeadLayout.setContentsMargins(0, 0, 0, 0)
        self.locationHeadLayout.setSpacing(0)

        self.locationName = QLabel("Location Name")
        self.locationName.setMaximumHeight(60)
        self.locationHeadLayout.addWidget(self.locationName)
        self.locationHeadLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.locationName.setProperty("class", "header1")

        # Search Bar2
        self.searchBar2.setStyleSheet("QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        self.searchBar2.setPlaceholderText("Where's Your Next Spot?")

        # Widget Container
        self.widgetContainer = QGroupBox()
        self.widgetContainer.setProperty("class","denimBackground")
        self.widgetContainerLayout = QVBoxLayout()
        self.widgetContainer.setLayout(self.widgetContainerLayout)
        self.widgetContainerLayout.setStretch(0, 2)
        self.widgetContainerLayout.setStretch(1, 2)
        self.widgetContainerLayout.setSpacing(5)  # Reduce spacing between rows
        self.widgetContainerLayout.setContentsMargins(0, 0, 0, 0)

        # Top Row Widgets Box
        self.topRowWidgetsBox = QGroupBox()
        self.topRowWidgetsLayout = QHBoxLayout()
        self.topRowWidgetsBox.setLayout(self.topRowWidgetsLayout)
        self.widgetContainerLayout.addWidget(self.topRowWidgetsBox)

        # Bottom Row Widgets Box
        self.bottomRowWidgetsBox = QGroupBox()
        self.bottomRowWidgetsLayout = QHBoxLayout()
        self.bottomRowWidgetsBox.setLayout(self.bottomRowWidgetsLayout)
        self.widgetContainerLayout.addWidget(self.bottomRowWidgetsBox)

        # Weather Widget
        self.weatherWidget = WeatherWidget()
        self.topRowWidgetsLayout.addWidget(self.weatherWidget)

        # Map Widget
        self.mapWidget = MapWidget()
        self.topRowWidgetsLayout.addWidget(self.mapWidget)

        #Poverty Widget
        self.povertyWidget = PovertyWidget()
        self.topRowWidgetsLayout.addWidget(self.povertyWidget)

        #Description Widget
        self.descWidget = DescriptionWidget()
        self.bottomRowWidgetsLayout.addWidget(self.descWidget)

        #Crime Widget
        self.crimeWidget = CrimeWidget()
        self.topRowWidgetsLayout.addWidget(self.crimeWidget)

        #Compare Button
        self.comparisonButton = QPushButton()
        self.comparisonButton.setIcon(QIcon("classes/ui/imgs/compareButton.png"))
        
        self.widgetContainerLayout.addChildWidget(self.comparisonButton)
        self.comparisonButton.setProperty("id", "comparisonButton")
        self.comparisonButton.setGeometry(self.width() - 90, self.height() // 2 - 60, 60, 60)
        self.comparisonButton.setIconSize(self.comparisonButton.size())
        self.comparisonButton.clicked.connect(self.compareButtonClicked)

        # Heart Button
        self.heartButton = QPushButton()
        self.heartButton.setProperty("id","heart")
        self.widgetContainerLayout.addChildWidget(self.heartButton) 
        #Determines button state
        global likeLocation 
        if likeLocation:
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))
            likeLocation = False
        else:
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))
            likeLocation = True
        self.heartButton.clicked.connect(self.heartButtonClicked)
        
        self.heartButton.setGeometry(self.width() - 90, self.height() // 2 + 60, 60, 60)
        self.heartButton.setIconSize(QSize(55,55))

        # Adjust margins for the top and bottom row layouts
        self.topRowWidgetsLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.bottomRowWidgetsLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        

        # Add the widgetContainer to the locationMainLayout
        self.locationMainLayout.addWidget(self.widgetContainer)  # Ensure the container is added to the layout

        # Set Central Widget
        self.setCentralWidget(self.stacked_widget)

        # Blur When Loading
        self.blur_effect = QGraphicsBlurEffect(self)
        self.blur_effect.setBlurRadius(0)
        self.stacked_widget.setGraphicsEffect(self.blur_effect)

        self.comparePage = ComparisonWidget(self.centralWidget, self.locationPage, self)
        self.likesWidget = LikesWidget(self.centralWidget, self.locationPage, self)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.centralWidget)  # First page
        self.stacked_widget.addWidget(self.locationPage)  # Second page
        self.stacked_widget.addWidget(self.comparePage)
        self.stacked_widget.addWidget(self.likesWidget)


        # Default page to show
        self.stacked_widget.setCurrentWidget(self.centralWidget)

    

    def createLocationWidgets(self):
        try: #Opens json file, parses it, and generates the form for the user to select a location
            with open("cachedLocations.json", "r") as file:
                clear_layout(self.bottomLayout)
                loadedFile = json.load(file)
                
                for location in loadedFile:
                    locationObject = loadObjectFromJson(location)
                    newLocoWidget = LocationWidget()
                    
                    self.bottomLayout.addWidget(newLocoWidget)
                    newLocoWidget.updateLocationLabels(locationObject)
                    newLocoWidget.locationClickedSignal.connect(self.handleLocationClicked)
                file.close()

            likedLocationsButton = LocationWidget()
            self.bottomLayout.addWidget(likedLocationsButton)
             
            likedLocationsButton.updateLocationLabels(currentLocation, True)

            likedLocationsButton.nameLabel.clicked.connect(self.switch_to_likes_page)

        except FileNotFoundError: #This occurs if the user has not searched yet
            pass
    
    def switch_to_likes_page(self):
        '''Switched the stacked widget to the liked page'''
        self.stacked_widget.setCurrentWidget(self.likesWidget)
        self.likesWidget.populateLocations()

    def handleLocationClicked(self, location_name):
        # Access switch_to_second_page here

        self.searchBar.setText(location_name)
        self.switch_to_second_page()


    def compareButtonClicked(self):
        """Switch to the compare page and update its labels."""
        self.stacked_widget.setCurrentWidget(self.centralWidget)
        self.titleLabel.setText("Where do you want to compare?")
        global mode
        mode = "compare"

    def heartButtonClicked(self):
        global likeLocation

        with open("heartDB.json", "r") as file:
            contents = json.load(file)

            matched = False

            for item1 in contents:
                if currentLocation.getAddress() == item1["address"]:
                    matched = True

            if not matched:
                contents.append({"address" : currentLocation.getAddress(), "likers" : []})

            for item in contents:
                if item["address"] == currentLocation.getAddress():
                    if currentUser in item["likers"]:
                        item["likers"].pop(item["likers"].index(currentUser))
                        self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))
                        likeLocation = False
                    else:
                        item["likers"].append(currentUser)
                        self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))
                        likeLocation = True

            file.close()
        with open("heartDB.json", "w") as file:
            json.dump(contents, file)
            file.close()

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:  # Check if the Enter key was pressed
            
            if (len(self.searchBar.text()) > 0) or (len(self.searchBar.text()) > 0): #If the home page bar is typed in
                self.switch_to_second_page()  # Switch to the second page if text is entered
            elif len(self.searchBar2.text()) > 0:
                self.update_location_page()

    def update_location_page(self): 
        '''If searching from location page just update it'''
        from main import getLocation, getWeather
        
        location = getLocation(self.searchBar2.text())
        global currentLocation
        currentLocation = location
        getWeather(location)
        self.locationName.setText(location.getAddress())
        self.weatherWidget.updateWeatherLabels(currentLocation)
        self.mapWidget.updateMap(currentLocation)
        self.povertyWidget.updateLabels(currentLocation)
        self.descWidget.updateLabel(currentLocation)
        self.crimeWidget.updateCrime(currentLocation)

        with open("heartDB.json", "r") as file:
            contents = json.load(file)
            likeLocation = False
            for location in contents:
                if currentUser in location["likers"]:
                    likeLocation = True


        if likeLocation:
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))
        else:
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))

        currentLocation.save_to_db()
        currentLocation.save_weather_data()

    def switch_to_second_page(self):
        """Switch to the second page in the stacked widget."""
        from main import getLocation,getWeather
        self.blur_effect.setBlurRadius(5)
        QCoreApplication.processEvents()

        if len(self.comparePage.searchBar3.text()) > 0:
            location = getLocation(self.comparePage.searchBar3.text())
        else:
            location = getLocation(self.searchBar.text())
        global mode
        if mode == "new": 
            getWeather(location)
            self.stacked_widget.setCurrentWidget(self.locationPage)
            global currentLocation
            if location.getAddress() == "N/A":
                self.locationName.setText("Sorry! We weren't able to find this location.")
                self.weatherWidget.setVisible(False)
                self.mapWidget.setVisible(False)
                self.povertyWidget.setVisible(False)
                self.descWidget.setVisible(False)
                self.crimeWidget.setVisible(False)
            else:
                self.locationName.setText(location.getAddress())
                currentLocation = location
                self.weatherWidget.updateWeatherLabels(currentLocation)
                self.mapWidget.updateMap(currentLocation)
                self.povertyWidget.updateLabels(currentLocation)
                self.descWidget.updateLabel(currentLocation)
                self.crimeWidget.updateCrime(currentLocation)
                

                self.weatherWidget.setVisible(True)
                self.mapWidget.setVisible(True)
                self.povertyWidget.setVisible(True)
                self.descWidget.setVisible(True)
                self.crimeWidget.setVisible(True)

                if likeLocation:
                    self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))
                else:
                    self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))

        elif mode == "compare": #If the app is in compare mode do this logic
            if currentLocation is not None:
                self.comparePage.updateLabels(location)
                self.stacked_widget.setCurrentWidget(self.comparePage)
                mode = 'new'

        self.searchBar.setPlaceholderText("Where's Your Next Spot?")
        self.searchBar.setText("")
        self.blur_effect.setBlurRadius(0)
        QCoreApplication.processEvents()

        currentLocation.save_to_db()
        currentLocation.save_weather_data()

    def switch_to_home_page(self):
        self.stacked_widget.setCurrentWidget(self.centralWidget)
        self.searchBar2.setText("")
        self.createLocationWidgets()
        self.titleLabel.setText("Spot Finder")
        global likeLocation
        likeLocation = False
        

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            clear_layout(item.layout())