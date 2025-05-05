from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout
)


class MyProfileDialog(QDialog):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Profile")
        self.setFixedSize(350, 250)

        self.window = window  # Access to main window attributes

        layout = QVBoxLayout()

        # Editable fields
        self.username_input = QLineEdit(window.current_username)
        self.user_id_input = QLineEdit(window.current_user_id)
        self.email_input = QLineEdit(window.current_email)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        layout.addWidget(QLabel("E-mail:"))
        layout.addWidget(self.email_input)

        # Buttons: Save | Delete
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_and_close)
        button_layout.addWidget(save_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_and_close)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_and_close(self):
        self.window.current_username = self.username_input.text()
        self.window.current_user_id = self.user_id_input.text()
        self.window.current_email = self.email_input.text()
        self.accept()  # Close dialog

    def delete_and_close(self):
        self.window.current_username = ""
        self.window.current_user_id = ""
        self.window.current_email = ""
        self.accept()  # Close dialog
