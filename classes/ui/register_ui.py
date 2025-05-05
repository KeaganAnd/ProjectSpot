import uuid
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QCheckBox,
    QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from classes.ui.login_ui import LoginUI


class RegisterUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.resize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(10)

        # Top Image
        self.image_label = QLabel()
        pixmap = QPixmap("classes/ui/imgs/signup.jfif")
        self.image_label.setPixmap(pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Input Fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        layout.addWidget(self.first_name)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")
        layout.addWidget(self.last_name)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email Address")
        layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.verify_password = QLineEdit()
        self.verify_password.setPlaceholderText("Verify Password")
        self.verify_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.verify_password)

        # Terms and Conditions Checkbox
        self.terms_checkbox = QCheckBox()
        terms_label = QLabel(
            'By clicking confirm, you agree to the <b>SpotFinder Terms of Service</b> '
            'and the <b>SpotFinder Privacy Notice</b>.'
        )
        terms_label.setWordWrap(True)
        terms_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        terms_label.setOpenExternalLinks(True)
        terms_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        terms_layout = QHBoxLayout()
        terms_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        terms_layout.addWidget(self.terms_checkbox)
        terms_layout.addWidget(terms_label)
        layout.addLayout(terms_layout)

        # Confirm Button
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)
        self.confirm_button.clicked.connect(self.handle_register)
        layout.addWidget(self.confirm_button)

        # Login Link 
        login_label = QLabel('Already have an account? <a href="#">Login</a>')
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.setOpenExternalLinks(False)
        login_label.linkActivated.connect(self.open_login)
        login_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            a {
                color: #1a73e8;
                text-decoration: underline;
            }
        """)
        layout.addWidget(login_label)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email.text().strip()
        password = self.password.text()
        verify_password = self.verify_password.text()

        if not username or not email:
            QMessageBox.warning(self, "Input Error", "Please enter your username and email.")
            return
        if password != verify_password:
            QMessageBox.warning(self, "Password Error", "Passwords do not match.")
            return
        if not self.terms_checkbox.isChecked():
            QMessageBox.warning(self, "Terms", "You must agree to the terms.")
            return

        # Generate unique User ID
        user_id = self.generate_user_id()

        # Pass data to parent (e.g. MainWindow)
        if self.parent() and hasattr(self.parent(), "set_user_info"):
            self.parent().set_user_info(username, user_id, email)

        # Show success message
        QMessageBox.information(
            self, "Success",
            f"You have successfully registered!\n\nAccount - User ID: {user_id}"
        )

        self.close()

    def generate_user_id(self):
        """Generate a short unique User ID"""
        return str(uuid.uuid4())[:8].upper()

    def open_login(self):
        """Switch to Login window"""
        self.close()
        login_window = LoginUI(parent=self.parent())
        login_window.show()

        # Prevent garbage collection
        from classes.ui.ui_router import open_windows
        open_windows.append(login_window)
