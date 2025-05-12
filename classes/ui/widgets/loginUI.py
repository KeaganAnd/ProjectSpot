from PyQt6.QtGui import * # Import necessary QtGui modules
from PyQt6.QtWidgets import * # Import necessary QtWidgets modules
from PyQt6.QtCore import * # Import necessary QtCore modules
import sqlite3
import hashlib

class LoginUI(QWidget):
    def __init__(self, parentStackedWidget, centralWidget, mainWindow):
        super().__init__()
        self.setWindowTitle("Account - Login")
        self.resize(500, 600)
        self.setMaximumHeight(600)
        self.setMaximumWidth(500)
        self.setProperty("class","mainWidget")
        self.setStyleSheet("[class=\"mainWidget\"] {background-color: transparent;} QScrollArea {background-color: transparent}")      
        self.setup_ui()
        self.parentStackedWidget = parentStackedWidget
        self.registerElement = None
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

        welcome_text = QLabel("Log In")
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
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(                                                   # Apply CSS styles to the search bar
            "QLineEdit { padding-left: 15px; padding-right: 10px; padding-top: 5px; padding-bottom: 5px; }")
        layout.addWidget(self.password_input)

        

        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setStyleSheet(
            "background-color: #2e7d32; color: white; padding: 10px; font-weight: bold; font-size: 14px;"
        )
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

       # Forgot password link
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        self.forgot_label = QLabel('<a href="#">Need To Register?</a>')
        self.forgot_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(False)
        self.forgot_label.setStyleSheet("color: blue; font-size: 12px; text-decoration: underline; font-weight: bold;")
        self.forgot_label.linkActivated.connect(self.open_register_page)
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
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return

        conn = sqlite3.connect('spot_finder.db')
        cursor = conn.cursor()
        
        # Query for the user
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row:
            password = row[0]

            if hashedPassword == password:
                QMessageBox.information(self, "Success!", f"Logged in as {username}!")

                self.parentStackedWidget.setCurrentWidget(self.centralWidget)

                with open("user.id", "a+") as file:
                    file.seek(0)
                    self.mainWindow.setCurrentUser(file.read())
                    file.close()
            else:
                QMessageBox.information(self, "Wrong Password!", f"Password Incorrect (Case Sensitive)")
                return

        else:
            QMessageBox.information(self, "Doesn't exist", f"The user {username} doesn't exist! Please check your spelling or sign up.")
            return

        conn.close()
                

        
        self.close()

    def open_register_page(self):  
        self.parentStackedWidget.setCurrentWidget(self.registerElement)