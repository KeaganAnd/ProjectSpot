import os
import re
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from dotenv import load_dotenv
from email_sender import send_verification_email

load_dotenv()

class ForgotPasswordUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forgot Password")
        self.resize(500, 650)
        self.setMinimumSize(400, 500)

        self.verification_code = None
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 15, 30, 15)
        self.main_layout.setSpacing(12)

        title = QLabel("Reset Your Password")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.main_layout.addWidget(self.email_input)

        # Send code button
        self.send_code_btn = QPushButton("Send Verification Code")
        self.send_code_btn.clicked.connect(self.send_verification_code)
        self.main_layout.addWidget(self.send_code_btn)

        # Verification code input (initially hidden)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter verification code")
        self.code_input.setMaxLength(6)
        self.code_input.hide()
        self.main_layout.addWidget(self.code_input)

        # New password
        self.new_pass_input = QLineEdit()
        self.new_pass_input.setPlaceholderText("New Password")
        self.new_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pass_input.hide()
        self.main_layout.addWidget(self.new_pass_input)

        # Confirm password
        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setPlaceholderText("Confirm New Password")
        self.confirm_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pass_input.hide()
        self.main_layout.addWidget(self.confirm_pass_input)

        # Confirm button
        self.confirm_btn = QPushButton("Confirm Reset")
        self.confirm_btn.clicked.connect(self.confirm_reset)
        self.confirm_btn.hide()
        self.main_layout.addWidget(self.confirm_btn)

        self.main_layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(self.main_layout)
        scroll_area.setWidget(container)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def send_verification_code(self):
        email = self.email_input.text().strip()

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            self.email_input.clear()
            return

        self.verification_code = str(random.randint(100000, 999999))
        print(f"[Debug] Verification code for {email}: {self.verification_code}")

        if send_verification_email(email, self.verification_code):
            QMessageBox.information(self, "Email Sent", f"Verification code sent to: {email}")
            # Show additional fields
            self.code_input.show()
            self.new_pass_input.show()
            self.confirm_pass_input.show()
            self.confirm_btn.show()
            self.email_input.setReadOnly(True)
            self.send_code_btn.setEnabled(False)
        else:
            QMessageBox.critical(self, "Error", "Failed to send verification code. Try again later.")

    def confirm_reset(self):
        entered_code = self.code_input.text().strip()
        new_password = self.new_pass_input.text().strip()
        confirm_password = self.confirm_pass_input.text().strip()

        if entered_code != self.verification_code:
            QMessageBox.warning(self, "Invalid Code", "The verification code is incorrect.")
            return

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Empty Fields", "Please enter and confirm your new password.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return

        # Simulate password update (replace with DB logic)
        print(f"[Debug] Password for {self.email_input.text().strip()} updated to: {new_password}")
        QMessageBox.information(self, "Success", "Your password has been reset successfully.")
        self.close()

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None
