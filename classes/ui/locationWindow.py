from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class locationWindows(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window setup
        self.setWindowTitle("Spot Finder")
        self.setMinimumSize(640, 360)
        self.setMaximumSize(1920, 1080)
        self.resize(2560, 1440)

        # Central Widget and Main Layout
        centralWidget = QWidget()
        mainLayout = QVBoxLayout(centralWidget)

        mainLayout.addWidget(QLabel("Hello"))

        # Set Central Widget
        self.setCentralWidget(centralWidget)



