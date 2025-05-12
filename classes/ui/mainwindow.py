from PyQt6.QtGui import * # Import necessary QtGui modules
from PyQt6.QtWidgets import * # Import necessary QtWidgets modules
from PyQt6.QtCore import * # Import necessary QtCore modules
from ..location import loadObjectFromJson                                               # Import the function to load location objects from JSON
import json
import sqlite3                                                                            # Import the json library for handling JSON data

currentLocation = None                                                                 # Initialize a variable to store the current location object

mode = "new"                                                                           # Initialize a variable to track the current mode (new or compare)
likeLocation = False

with open("user.id", "r") as file:                                                                  # Initialize a boolean to track if the current location is liked
    currentUser = file.read()                                                                   # Initialize a variable to store the current user's ID

# Widget Imports
from .widgets.WeatherWidget import WeatherWidget                                       # Import the WeatherWidget class
from .widgets.PovertyWidget import PovertyWidget                                       # Import the PovertyWidget class
from .widgets.MapWidget import MapWidget                                               # Import the MapWidget class
from .widgets.CrimeWidgets import CrimeWidget                                           # Import the CrimeWidget class
from .widgets.DescriptionWidget import DescriptionWidget                               # Import the DescriptionWidget class
from .widgets.ComparisonWidget import ComparisonWidget                                 # Import the ComparisonWidget class
from .widgets.LikesWidget import LikesWidget                                           # Import the LikesWidget class
from .widgets.LocationWidget import LocationWidget                                     # Import the LocationWidget class
from .widgets.loginUI import LoginUI
from .widgets.registerUI import registerUI

from ..location import Location

class MainWindow(QMainWindow):                                                          # Define the main application window class, inheriting from QMainWindow

    def __init__(self, *args, **kwargs):                                               # Define the constructor for the MainWindow class
        super().__init__(*args, **kwargs)                                               # Call the constructor of the parent class (QMainWindow)
                                                               # Close the file

        # Window setup
        self.setWindowTitle("Spot Finder")                                              # Set the title of the main window
        self.setMaximumSize(1920, 1080)                                                 # Set the maximum size of the main window
        self.setMinimumSize(1440, 932)                                                  # Set the minimum size of the main window
        self.setWindowIcon(QIcon('classes/ui/imgs/searchIcon.png'))                    # Set the window icon

        #!HOME SCREEN

        # Central Widget and Main Layout
        self.centralWidget = QWidget()                                                  # Create a central widget to hold other widgets
        self.mainLayout = QVBoxLayout(self.centralWidget)                                   # Create a vertical layout for the central widget

        # Stacked Widget to switch between pages
        self.stacked_widget = QStackedWidget(self.centralWidget)                       # Create a stacked widget to manage different pages

        # Group Boxes for top and bottom sections
        self.topGroupBox = QGroupBox(self.centralWidget)                               # Create a group box for the top section of the home screen
        self.bottomGroupBox = QGroupBox(self.centralWidget)                            # Create a group box for the bottom section of the home screen

        # Layouts for Group Boxes
        self.topLayout = QVBoxLayout()                                                  # Create a vertical layout for the top group box
        self.bottomLayout = QHBoxLayout()                                                 # Create a horizontal layout for the bottom group box
        self.topGroupBox.setLayout(self.topLayout)                                      # Set the layout for the top group box
        self.bottomGroupBox.setLayout(self.bottomLayout)                                # Set the layout for the bottom group box

        # Set layout spacings
        self.topLayout.setSpacing(0)                                                   # Remove spacing within the top layout
        self.bottomLayout.setSpacing(0)                                                # Remove spacing within the bottom layout

        # Set margins for group boxes and main layout
        self.topGroupBox.setContentsMargins(0, 0, 0, 0)                                 # Remove margins around the top group box
        self.bottomGroupBox.setContentsMargins(0, 0, 0, 0)                              # Remove margins around the bottom group box
        self.mainLayout.setContentsMargins(0, 0, 0, 0)                                      # Remove margins around the main layout

        # Create widgets
        self.titleLabel = QLabel("Spot Finder")                                         # Create a label for the title
        self.searchBar = QLineEdit()                                                    # Create a line edit for the search bar
        self.loadingLabel = QLabel("Loading...")                                        # Create a label for the loading message
        self.stacked_widget.addWidget(self.loadingLabel)                               # Add the loading label to the stacked widget

        self.createLocationWidgets()                                                    # Call a method to create widgets for cached locations

        # Change widget elements
        self.searchBar.setPlaceholderText(f"Where's Your Next Spot?")                    # Set the placeholder text for the search bar

        # Add Widgets to layouts
        self.topLayout.addWidget(self.titleLabel)                                       # Add the title label to the top layout
        self.topLayout.addWidget(self.searchBar)                                          # Add the search bar to the top layout

        # Set Properties and Alignments
        self.titleLabel.setProperty("class", "header1")                                 # Set a CSS property for the title label
        self.topGroupBox.setProperty("id", "topBox")                                    # Set an ID property for the top group box
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)                       # Align the title label to the left
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter) # Center the content of the top layout
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)                      # Align the content of the bottom layout to the left
        self.titleLabel.setFixedHeight(60)                                             # Set a fixed height for the title label

        # Apply styles
        self.searchBar.setStyleSheet(                                                   # Apply CSS styles to the search bar
            "QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")

        # Add GroupBoxes to the main layout
        self.mainLayout.addWidget(self.topGroupBox)                                         # Add the top group box to the main layout
        self.mainLayout.addWidget(self.bottomGroupBox)                                      # Add the bottom group box to the main layout
        self.mainLayout.setSpacing(0)                                                      # Remove spacing between widgets in the main layout

        # Set layout stretch factors
        self.mainLayout.setStretch(0, 3)                                                    # Set the stretch factor for the top part of the main layout
        self.mainLayout.setStretch(1, 1)                                                    # Set the stretch factor for the bottom part of the main layout

        #!Location Page
        self.locationPage = QWidget()                                                   # Create a widget for the location page
        self.locationMainLayout = QVBoxLayout(self.locationPage)                       # Create a vertical layout for the location page
        self.locationPage.setLayout(self.locationMainLayout)                           # Set the layout for the location page
        self.locationMainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)                # Align the content of the location main layout to the top

        # Remove margins and spacing
        self.locationMainLayout.setContentsMargins(0, 0, 0, 0)                         # Remove margins around the location main layout
        self.locationMainLayout.setSpacing(0)                                         # Remove spacing between widgets in the location main layout

        # Header section
        self.header = QGroupBox()                                                       # Create a group box for the header of the location page
        self.locationMainLayout.addWidget(self.header)                                  # Add the header group box to the location main layout
        self.header.setMaximumHeight(100)                                               # Set the maximum height of the header
        self.header.setProperty("class", "header")                                      # Set a CSS property for the header

        self.headerLayout = QHBoxLayout(self.header)                                    # Create a horizontal layout for the header
        self.homeButton = QPushButton("Spot Finder")                                    # Create a button to go back to the home screen
        self.searchBar2 = QLineEdit()                                                   # Create a second search bar for the location page
        self.headerLayout.addWidget(self.homeButton)                                   # Add the home button to the header layout
        self.headerLayout.addWidget(self.searchBar2)                                  # Add the second search bar to the header layout
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)                     # Align the content of the header layout to the top

        # Remove margins and spacing from header layout
        self.headerLayout.setContentsMargins(0, 0, 0, 0)                               # Remove margins around the header layout
        self.headerLayout.setSpacing(0)                                                # Remove spacing between widgets in the header layout

        self.homeButton.setProperty("class", "homeButton")                              # Set a CSS property for the home button
        self.homeButton.setMaximumWidth(350)                                            # Set the maximum width of the home button
        self.homeButton.setMinimumHeight(80)                                           # Set the minimum height of the home button
        self.homeButton.clicked.connect(self.switch_to_home_page)                      # Connect the home button's click event to a method

        # Body
        self.locationHead = QGroupBox()                                                 # Create a group box for the location name header
        self.locationHead.setMaximumHeight(60)                                          # Set the maximum height of the location header
        self.locationHeadLayout = QVBoxLayout(self.locationHead)                        # Create a vertical layout for the location header
        self.locationMainLayout.addWidget(self.locationHead)                            # Add the location header group box to the main layout

        # Remove margins and spacing from location head layout
        self.locationHeadLayout.setContentsMargins(0, 0, 0, 0)                        # Remove margins around the location header layout
        self.locationHeadLayout.setSpacing(0)                                        # Remove spacing between widgets in the location header layout

        self.locationName = QLabel("Location Name")                                     # Create a label to display the location name
        self.locationName.setMaximumHeight(60)                                          # Set the maximum height of the location name label
        self.locationHeadLayout.addWidget(self.locationName)                            # Add the location name label to the location header layout
        self.locationHeadLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter) # Align the location name label to the top and center horizontally
        self.locationName.setProperty("class", "header1")                              # Set a CSS property for the location name label

        # Search Bar2
        self.searchBar2.setStyleSheet(                                                  # Apply CSS styles to the second search bar
            "QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        self.searchBar2.setPlaceholderText("Where's Your Next Spot?")                    # Set the placeholder text for the second search bar

        # Widget Container
        self.widgetContainer = QGroupBox()                                              # Create a group box to contain the information widgets
        self.widgetContainer.setProperty("class", "denimBackground")                    # Set a CSS property for the widget container
        self.widgetContainerLayout = QVBoxLayout()                                       # Create a vertical layout for the widget container
        self.widgetContainer.setLayout(self.widgetContainerLayout)                     # Set the layout for the widget container
        self.widgetContainerLayout.setStretch(0, 2)                                     # Set the stretch factor for the first part of the container layout
        self.widgetContainerLayout.setStretch(1, 2)                                     # Set the stretch factor for the second part of the container layout
        self.widgetContainerLayout.setSpacing(5)                                       # Reduce spacing between rows in the container layout
        self.widgetContainerLayout.setContentsMargins(0, 0, 0, 0)                      # Remove margins around the widget container layout

        # Top Row Widgets Box
        self.topRowWidgetsBox = QGroupBox()                                             # Create a group box to hold widgets in the top row
        self.topRowWidgetsLayout = QHBoxLayout()                                        # Create a horizontal layout for the top row widgets
        self.topRowWidgetsBox.setLayout(self.topRowWidgetsLayout)                      # Set the layout for the top row widgets box
        self.widgetContainerLayout.addWidget(self.topRowWidgetsBox)                     # Add the top row widgets box to the widget container layout

        # Bottom Row Widgets Box
        self.bottomRowWidgetsBox = QGroupBox()                                          # Create a group box to hold widgets in the bottom row
        self.bottomRowWidgetsLayout = QHBoxLayout()                                     # Create a horizontal layout for the bottom row widgets
        self.bottomRowWidgetsBox.setLayout(self.bottomRowWidgetsLayout)                # Set the layout for the bottom row widgets box
        self.widgetContainerLayout.addWidget(self.bottomRowWidgetsBox)                  # Add the bottom row widgets box to the widget container layout

        # Weather Widget
        self.weatherWidget = WeatherWidget()                                            # Create an instance of the WeatherWidget
        self.topRowWidgetsLayout.addWidget(self.weatherWidget)                           # Add the weather widget to the top row layout

        # Map Widget
        self.mapWidget = MapWidget()                                                    # Create an instance of the MapWidget
        self.topRowWidgetsLayout.addWidget(self.mapWidget)                               # Add the map widget to the top row layout

        # Poverty Widget
        self.povertyWidget = PovertyWidget()                                            # Create an instance of the PovertyWidget
        self.topRowWidgetsLayout.addWidget(self.povertyWidget)                           # Add the poverty widget to the top row layout

        # Description Widget
        self.descWidget = DescriptionWidget()                                          # Create an instance of the DescriptionWidget
        self.bottomRowWidgetsLayout.addWidget(self.descWidget)                         # Add the description widget to the bottom row layout

        # Crime Widget
        self.crimeWidget = CrimeWidget()                                                # Create an instance of the CrimeWidget
        self.topRowWidgetsLayout.addWidget(self.crimeWidget)                             # Add the crime widget to the top row layout

        # Compare Button
        self.comparisonButton = QPushButton()                                           # Create a button for comparison
        self.comparisonButton.setIcon(QIcon("classes/ui/imgs/compareButton.png"))      # Set the icon for the comparison button

        self.widgetContainerLayout.addChildWidget(self.comparisonButton)                # Add the comparison button directly to the container layout
        self.comparisonButton.setProperty("id", "comparisonButton")                     # Set an ID property for the comparison button
        self.comparisonButton.setGeometry(self.width() - 90, self.height() // 2 - 60, 60, 60) # Set the initial geometry of the comparison button
        self.comparisonButton.setIconSize(self.comparisonButton.size())                 # Set the icon size to the button size
        self.comparisonButton.clicked.connect(self.compareButtonClicked)                # Connect the button's click event to the compareButtonClicked method

        # Heart Button
        self.heartButton = QPushButton()                                                # Create a button for liking a location
        self.heartButton.setProperty("id", "heart")                                     # Set an ID property for the heart button
        self.widgetContainerLayout.addChildWidget(self.heartButton)                     # Add the heart button directly to the container layout
        # Determines button state
        global likeLocation                                                             # Access the global likeLocation variable
        if likeLocation:                                                                # Check if the location is currently liked
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))               # Set the icon to a filled heart
            likeLocation = False                                                       # Reset the global likeLocation flag
        else:                                                                         # If the location is not currently liked
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))           # Set the icon to an empty heart
            likeLocation = True                                                        # Set the global likeLocation flag
        self.heartButton.clicked.connect(self.heartButtonClicked)                       # Connect the button's click event to the heartButtonClicked method

        self.heartButton.setGeometry(self.width() - 90, self.height() // 2 + 60, 60, 60) # Set the initial geometry of the heart button
        self.heartButton.setIconSize(QSize(55, 55))                                     # Set the size of the heart icon

        # Adjust margins for the top and bottom row layouts
        self.topRowWidgetsLayout.setContentsMargins(0, 0, 0, 0)                        # Remove margins around the top row widgets layout
        self.bottomRowWidgetsLayout.setContentsMargins(0, 0, 0, 0)                     # Remove margins around the bottom row widgets layout

        # Add the widgetContainer to the locationMainLayout
        self.locationMainLayout.addWidget(self.widgetContainer)                        # Add the container holding widgets to the location page layout

        # Set Central Widget
        self.setCentralWidget(self.stacked_widget)                                      # Set the stacked widget as the central widget of the main window

        # Blur When Loading
        self.blur_effect = QGraphicsBlurEffect(self)                                   # Create a blur effect
        self.blur_effect.setBlurRadius(0)                                              # Initially set the blur radius to 0 (no blur)
        self.stacked_widget.setGraphicsEffect(self.blur_effect)                       # Apply the blur effect to the stacked widget

        self.comparePage = ComparisonWidget(self.centralWidget, self.locationPage, self) # Create an instance of the ComparisonWidget
        self.likesWidget = LikesWidget(self.centralWidget, self.locationPage, self, currentUser) # Create an instance of the LikesWidget

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.centralWidget)                              # Add the first page (home screen) to the stacked widget
        self.stacked_widget.addWidget(self.locationPage)                              # Add the second page (location page) to the stacked widget
        self.stacked_widget.addWidget(self.comparePage)                                # Add the comparison page to the stacked widget
        self.stacked_widget.addWidget(self.likesWidget)                                # Add the likes page to the stacked widget

        #Profile Button
        self.profileButton = QPushButton()
        profileImg = QPixmap("classes/ui/imgs/user.png")
        icon = QIcon(profileImg)
        self.profileButton.setIcon(icon)
        self.profileButton.setIconSize(QSize(75,75))
        self.profileButton.setStyleSheet("QPushButton {border-radius: 37px; background-color: #8FBC8F;} QPushButton:hover {background-color:#A2D1A2}")
        self.profileButton.clicked.connect(self.showLogin)
        self.mainLayout.addChildWidget(self.profileButton)
        self.profileButton.setGeometry(10,10,75,75)



        #Login

        self.loginBox = QWidget()            #Boxes to store each widget
        self.registerBox = QWidget()         #so that they can center in the window

        self.loginBoxLayout = QHBoxLayout()
        self.registerBoxLayout = QHBoxLayout()

        self.loginBox.setLayout(self.loginBoxLayout)
        self.registerBox.setLayout(self.registerBoxLayout) 

        self.loginBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.registerBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)



        self.loginUi = LoginUI(self.stacked_widget, self.centralWidget, self)
        self.registerUi = registerUI(self.stacked_widget, self.centralWidget, self)

        self.loginBoxLayout.addWidget(self.loginUi)
        self.registerBoxLayout.addWidget(self.registerUi)

        self.loginUi.registerElement = self.registerBox #Give elements the other object so they can switch between eachother
        self.registerUi.loginElement = self.loginBox



        self.stacked_widget.addWidget(self.loginBox)
        self.stacked_widget.addWidget(self.registerBox)

        with open("user.id", "a+") as file:
            file.seek(0)  # Move to the start of the file
            contents = file.read()
            if len(contents) == 0:
                self.stacked_widget.setCurrentWidget(self.registerBox) #If no ID is found prompt user to login or register
    
            else:
                # Default page to show
                self.setCurrentUser(contents)
                self.stacked_widget.setCurrentWidget(self.centralWidget)   #Otherwise bring to home page
                
            file.close()                    # Set the home screen as the default page

        self.searchBar.setPlaceholderText(f"Where's Your Next Spot {currentUser}?")

    def setCurrentUser(self, id):
        global currentUser
        currentUser = id

    def showLogin(self):
        self.stacked_widget.setCurrentWidget(self.loginBox)
        self.loginBox.show()
        self.loginUi.show()

    def showRegister(self):
        self.stacked_widget.setCurrentWidget(self.registerBox)

    def createLocationWidgets(self):


        clear_layout(self.bottomLayout)                                           # Clear the layout to prevent duplicate widgets

        
        conn = sqlite3.connect('spot_finder.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.formatted_address
            FROM searches s
            JOIN locations l ON s.location_id = l.id
            WHERE s.username = ?
            ORDER BY l.search_date DESC
            LIMIT 4;
        """, (currentUser,))

        results = cursor.fetchall()


        for address in results:                                               # Iterate over each location in the loaded data
            
            newLocoWidget = LocationWidget()                                     # Create a new LocationWidget
            

            self.bottomLayout.addWidget(newLocoWidget)                            # Add the LocationWidget to the layout
            newLocoWidget.updateLocationLabels(Location(address=address[0]))                    # Update the labels in the LocationWidget with location data
            newLocoWidget.locationClickedSignal.connect(self.handleLocationClicked) # Connect the widget's signal to the handler                                                       # Close the file

        likedLocationsButton = LocationWidget()                                     # Create a LocationWidget for liked locations
        self.bottomLayout.addWidget(likedLocationsButton)                             # Add the liked locations button to the layout
            
        likedLocationsButton.updateLocationLabels(currentLocation, True)                # Update the labels, indicating it's for liked locations

        likedLocationsButton.nameLabel.clicked.connect(self.switch_to_likes_page)      # Connect the click signal to show liked locations


    
    def switch_to_likes_page(self):
        '''Switched the stacked widget to the liked page'''
        self.stacked_widget.setCurrentWidget(self.likesWidget) 
        self.likesWidget.titleLabel.setText(f"Liked Locations For {currentUser}")                         # Switch to the LikesWidget page
        self.likesWidget.populateLocations()                                           # Populate the LikesWidget with location data

    def handleLocationClicked(self, location_name):
        """Handle the event when a location is clicked."""
        self.searchBar.setText(location_name)                      # Set the clicked location name in the search bar
        self.switch_to_second_page()                               # Switch to the second page

    def compareButtonClicked(self):
        """Switch to the compare page and update its labels."""
        self.stacked_widget.setCurrentWidget(self.centralWidget)   # Switch the stacked widget to the central widget
        self.titleLabel.setText("Where do you want to compare?")   # Set the titleLabel text
        global mode                                                # Access the global variable 'mode'
        mode = "compare"                                           # Set the mode to 'compare'

    def heartButtonClicked(self):
        """Handle the heart button click to like/unlike a location."""
        global likeLocation                                        # Access the global likeLocation variable

        conn = sqlite3.connect("spot_finder.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1 FROM likes
            WHERE username = ? AND location_id = ?
        """, (currentUser, currentLocation.db_id))
        
        result = cursor.fetchone()

        if result: #If a like record exists then user likes the location. Delete the record and make heart gray
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))  # Set the heart icon to empty
            likeLocation = False 

            cursor.execute('''
                DELETE FROM likes
                WHERE username = ? AND location_id = ?;
                           ''', (currentUser, currentLocation.db_id))  
            conn.commit()

        else: #If a like record doesnt exists then user doesnt like the location. Make the record and make heart red
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))  # Set the heart icon to filled
            likeLocation = True   

            cursor.execute("""
                INSERT INTO likes (username, location_id)
                VALUES (?, ?)
            """, (currentUser, currentLocation.db_id))
            conn.commit()
        
        '''for item in contents:                                 # Iterate through the contents again
            if item["address"] == currentLocation.getAddress():  # Find the current location
                if currentUser in item["likers"]:             # If the user has already liked the location
                    item["likers"].pop(item["likers"].index(currentUser))  # Remove the user from likers
                    self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))  # Set the heart icon to empty
                    likeLocation = False                      # Set likeLocation to False
                else:                                         # If the user has not liked the location
                    item["likers"].append(currentUser)        # Add the user to likers
                    self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))  # Set the heart icon to filled
                    likeLocation = True                       # Set likeLocation to True'''



    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:                      # Check if the Enter key was pressed
            if len(self.searchBar.text()) > 0:                    # If the home page search bar has text
                self.switch_to_second_page()                      # Switch to the second page
            elif len(self.searchBar2.text()) > 0:                 # If the location page search bar has text
                self.update_location_page()                       # Update the location page

    def update_location_page(self):
        """Update the location page with new data."""
        from main import getLocation, getWeather                  # Import required functions

        location = getLocation(self.searchBar2.text())            # Get the location from the search bar
        global currentLocation
        currentLocation = location                                # Set the global currentLocation
        getWeather(location)                                      # Get the weather for the location
        self.locationName.setText(location.getAddress())          # Update the location name label
        self.weatherWidget.updateWeatherLabels(currentLocation)   # Update the weather widget
        self.mapWidget.updateMap(currentLocation)                 # Update the map widget
        self.povertyWidget.updateLabels(currentLocation)          # Update the poverty widget
        self.descWidget.updateLabel(currentLocation)              # Update the description widget
        self.crimeWidget.updateCrime(currentLocation)             # Update the crime widget

        with open("heartDB.json", "r") as file:                   # Open the heartDB.json file in read mode
            contents = json.load(file)                           # Load the contents of the file
            likeLocation = False                                 # Reset the likeLocation flag

            for location in contents:                            # Iterate through the contents
                if currentLocation.getAddress() == location["address"] and currentUser in location["likers"]:  # Check if the location is liked
                    likeLocation = True                          # Set likeLocation to True

        if likeLocation:                                         # If the location is liked
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))  # Set the heart icon to filled
        else:                                                    # If the location is not liked
            self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))  # Set the heart icon to empty

        currentLocation.save_to_db(currentUser)                             # Save the location to the database
        currentLocation.save_weather_data()                      # Save the weather data for the location

    def switch_to_second_page(self):
        """Switch to the second page in the stacked widget."""
        from main import getLocation, getWeather                 # Import required functions from main
        self.blur_effect.setBlurRadius(5)                        # Apply blur effect to the UI
        QCoreApplication.processEvents()                         # Process UI events (keeps app responsive)

        if len(self.comparePage.searchBar3.text()) > 0:          # Check if compare search bar has input
            location = getLocation(self.comparePage.searchBar3.text())  # Get location based on compare bar
        else:
            location = getLocation(self.searchBar.text())        # Get location based on main search bar

        global mode                                              # Use global mode variable
        if mode == "new":                                        # If in 'new' mode, display location info
            getWeather(location)                                 # Fetch weather data for location
            self.stacked_widget.setCurrentWidget(self.locationPage)  # Switch to location display page
            global currentLocation                               # Use global currentLocation variable
            if location.getAddress() == "N/A":                   # If address not found
                self.locationName.setText("Sorry! We weren't able to find this location.")  # Show error
                self.weatherWidget.setVisible(False)             # Hide weather widget
                self.mapWidget.setVisible(False)                 # Hide map widget
                self.povertyWidget.setVisible(False)             # Hide poverty widget
                self.descWidget.setVisible(False)                # Hide description widget
                self.crimeWidget.setVisible(False)               # Hide crime widget
            else:
                self.locationName.setText(location.getAddress()) # Display found address
                currentLocation = location                       # Store location globally
                self.weatherWidget.updateWeatherLabels(currentLocation)  # Update weather info
                self.mapWidget.updateMap(currentLocation)        # Update map view
                self.povertyWidget.updateLabels(currentLocation) # Update poverty data
                self.descWidget.updateLabel(currentLocation)     # Update description
                self.crimeWidget.updateCrime(currentLocation)    # Update crime stats

                self.weatherWidget.setVisible(True)              # Show weather widget
                self.mapWidget.setVisible(True)                  # Show map widget
                self.povertyWidget.setVisible(True)              # Show poverty widget
                self.descWidget.setVisible(True)                 # Show description widget
                self.crimeWidget.setVisible(True)                # Show crime widget

                

        elif mode == "compare":                                 # If the app is in compare mode
            if currentLocation is not None:                     # If a current location exists
                self.comparePage.updateLabels(location, currentLocation)  # Compare new location to current
                self.stacked_widget.setCurrentWidget(self.comparePage)    # Switch to compare page
                mode = 'new'                                    # Reset mode to new

        self.searchBar.setPlaceholderText(f"Where's Your Next Spot {currentUser}?")      # Reset placeholder text
        self.searchBar.setText("")                            # Clear search bar input
        self.blur_effect.setBlurRadius(0)                     # Remove blur effect
        QCoreApplication.processEvents()                      # Process any remaining UI events

        if currentLocation != None and currentLocation.getAddress() != "N/A":  # If a valid location exists
            currentLocation.save_to_db(currentUser)                     # Save the location to the database
            currentLocation.save_weather_data()              # Save the weather data for the location

            #Update liked location from DB ANCHOR
            conn = sqlite3.connect("spot_finder.db")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 FROM likes
                WHERE username = ? AND location_id = ?
            """, (currentUser, location.db_id))
            
            result = cursor.fetchone()
            print(f"{currentUser, location}")
            print(result)




            if result:
                self.heartButton.setIcon(QIcon("classes/ui/imgs/heart.png"))        # Show filled heart
            else:
                self.heartButton.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))   # Show empty heart

    def switch_to_home_page(self):
        self.stacked_widget.setCurrentWidget(self.centralWidget)  # Switch to the main/home page
        self.searchBar2.setText("")                                # Clear the secondary search bar
        self.createLocationWidgets()                               # Recreate the location display widgets
        self.titleLabel.setText("Spot Finder")                     # Reset the main title label
        global likeLocation                                        # Use global likeLocation variable
        likeLocation = False                                       # Reset like state
        self.searchBar2.setPlaceholderText(f"Where's Your Next Spot {currentUser}?") #ANCHOR

def clear_layout(layout):
    while layout.count():                                         # While layout has items
        item = layout.takeAt(0)                                   # Take the next item
        widget = item.widget()                                    # Get the widget from the item
        if widget is not None:
            widget.deleteLater()                                  # Delete widget if it exists
        else:
            clear_layout(item.layout())                           # Recursively clear nested layouts
