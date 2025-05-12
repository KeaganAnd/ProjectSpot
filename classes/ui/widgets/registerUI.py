from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QHBoxLayout, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

import sqlite3
import hashlib

class registerUI(QWidget):
    def __init__(self, parentStackedWidget, centralWidget, mainWindow):
        super().__init__()
        self.setWindowTitle("Account - Register")
        self.resize(500, 600)
        self.setMaximumHeight(600)
        self.setMaximumWidth(500)
        self.setup_ui()
        self.parentStackedWidget = parentStackedWidget
        self.loginElement = None
        self.setProperty("class","mainWidget")
        self.setStyleSheet("[class=\"mainWidget\"] {background-color: transparent;} QScrollArea {background-color: transparent}")      
        self.centralWidget = centralWidget
        self.mainWindow = mainWindow

    def setup_ui(self):
        # Scroll area in case content overflows
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        scroll_content.setProperty("class","backdrop")
        scroll_content.setStyleSheet("[class=\"backdrop\"] {border-radius: 15px; background-color: #30343F}")

        # Welcome image and title
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        welcome_text = QLabel("Register")
        welcome_text.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_text)

        # Username or email input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(                                                   # Apply CSS styles to the search bar
            "QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        #self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(                                                   # Apply CSS styles to the search bar
            "QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        layout.addWidget(self.password_input)

        

        # Login button
        self.login_button = QPushButton("Register")
        self.login_button.setStyleSheet(
            "background-color: #2e7d32; color: white; padding: 10px; font-weight: bold; font-size: 14px;"
        )
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

       # Forgot password link
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        self.forgot_label = QLabel('<a href="#">Need To Login?</a>')
        self.forgot_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(False)
        self.forgot_label.setStyleSheet("color: blue; font-size: 12px; text-decoration: underline; font-weight: bold;")
        self.forgot_label.linkActivated.connect(self.open_login_page)
        forgot_layout.addWidget(self.forgot_label)
        layout.addLayout(forgot_layout)

        layout.addStretch()
        scroll.setWidget(scroll_content)
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll)
        self.setLayout(scroll_layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        hashedPassword = hashlib.sha256()
        hashedPassword.update(password.encode())
        hashedPassword = hashedPassword.hexdigest()


        if not username or not password:
            QMessageBox.warning(self, "Registration Failed", "Please enter both username and password.")
            return

        # Register

        conn = sqlite3.connect('spot_finder.db')
        cursor = conn.cursor()

        # 1. Check if the user exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row:
            # Logic if user already exists
            QMessageBox.information(self, "User Exists", f"{username} already exists! Please login or choose a different username")

        else:
            # 2. Insert the new user
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashedPassword))
            conn.commit()

            QMessageBox.information(self, "Success!", f"Registered and logged in as {username}!")

            
            

            with open("user.id", "w") as file:
                file.write(username)
                file.close()
                
            self.mainWindow.setCurrentUser(username)

            self.mainWindow.createLocationWidgets()
            self.parentStackedWidget.setCurrentWidget(self.centralWidget) #Switch to home page upon register

        conn.close()



    def open_login_page(self):  
        self.parentStackedWidget.setCurrentWidget(self.loginElement)
