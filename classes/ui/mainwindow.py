from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


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
        centralWidget = QWidget()
        mainLayout = QVBoxLayout(centralWidget)

        # Stacked Widget to switch between pages
        self.stacked_widget = QStackedWidget(centralWidget)

        # Group Boxes for top and bottom sections
        self.topGroupBox = QGroupBox(centralWidget)
        self.bottomGroupBox = QGroupBox(centralWidget)

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
        self.secondPage = QWidget()

        


        # Set Central Widget
        self.setCentralWidget(self.stacked_widget)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(centralWidget)  # First page
        self.stacked_widget.addWidget(self.secondPage)  # Second page


        # Default page to show
        self.stacked_widget.setCurrentWidget(centralWidget)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return:  # Check if the Enter key was pressed
            if len(self.searchBar.text()) > 0:
                from main import getLocation
                print(getLocation(self.searchBar.text()))
                self.switch_to_second_page()  # Switch to the second page if text is entered

    def switch_to_second_page(self):
        """Switch to the second page in the stacked widget."""
        self.stacked_widget.setCurrentWidget(self.secondPage)


