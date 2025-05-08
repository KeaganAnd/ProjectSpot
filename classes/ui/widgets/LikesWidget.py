from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import json


'''
Oval Shaped Boxes
Centered Vertically
Green Location Font
Smaller Font


'''

from .LocationWidget import LocationWidget

class LikesWidget(QWidget):
    def __init__(self, homeWidget, locationWidget, mainWindow, currentUser):
        super().__init__()
        self.homeWidget = homeWidget
        self.mainWindow = mainWindow
        self.locationWidget = locationWidget
        self.currentUser = currentUser


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
        from ..mainwindow import clear_layout
        clear_layout(self.combined_layout)
        with open("heartDB.json", "r") as file:
            content = json.load(file)
            for location in content:
                if self.currentUser in location["likers"]:
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