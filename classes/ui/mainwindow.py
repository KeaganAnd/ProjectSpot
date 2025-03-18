from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Spot Finder")
        self.setMinimumSize(960, 540)

        self.titleLabel = QLabel("Welcome to Spot Finder!")


        layout = QVBoxLayout()
        layout.addWidget(self.titleLabel, Qt.AlignmentFlag.AlignHCenter)


        container = QWidget()
        container.setLayout(layout)



        self.setCentralWidget(container)

