from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QHBoxLayout, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class LoginUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Account - Login")
        self.resize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        # Scroll area in case content overflows
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Welcome image and title
        image_label = QLabel()
        pixmap = QPixmap("classes/ui/imgs/welcomeback.jpg")
        image_label.setPixmap(pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        welcome_text = QLabel("Login")
        welcome_text.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_text)

        # Username or email input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Forgot password link
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        self.forgot_label = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(False)
        self.forgot_label.setStyleSheet("color: blue; font-size: 12px; text-decoration: underline; font-weight: bold;")
        self.forgot_label.linkActivated.connect(self.open_forgot_password)
        forgot_layout.addWidget(self.forgot_label)
        layout.addLayout(forgot_layout)

        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setStyleSheet(
            "background-color: #2e7d32; color: white; padding: 10px; font-weight: bold; font-size: 14px;"
        )
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Remember Me checkbox
        self.remember_me = QCheckBox("Remember Me")
        self.remember_me.setStyleSheet("color: gray;")
        layout.addWidget(self.remember_me)

        layout.addStretch()
        scroll.setWidget(scroll_content)
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll)
        self.setLayout(scroll_layout)

    def handle_login(self):
        username_or_email = self.username_input.text().strip()
        password = self.password_input.text()

        if not username_or_email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username/email and password.")
            return

        # Simulate successful login (replace with real database check)
        username = username_or_email.split("@")[0] if "@" in username_or_email else username_or_email
        user_id = "U1234567"  # This should come from the database
        email = username_or_email if "@" in username_or_email else f"{username}@example.com"

        # Pass user info to parent (main window)
        if self.parent() and hasattr(self.parent(), "set_user_info"):
            self.parent().set_user_info(username, user_id, email)

        QMessageBox.information(self, "Success", f"Welcome back, {username}!")
        self.close()

    def open_forgot_password(self):
        print("Opening Forgot Password UI...")  # 调试输出
        from classes.ui.forgot_password_ui import ForgotPasswordUI  # 延迟导入

        # 创建 ForgotPasswordUI 窗口实例
        forgot_window = ForgotPasswordUI(self)
        forgot_window.setWindowModality(Qt.WindowModality.NonModal)
        forgot_window.setWindowFlag(Qt.WindowType.Window)
        forgot_window.setFixedSize(300, 150)

        # 将窗口居中显示
        parent_geometry = self.geometry()
        center_x = parent_geometry.x() + (parent_geometry.width() - forgot_window.width()) // 2
        center_y = parent_geometry.y() + (parent_geometry.height() - forgot_window.height()) // 2
        forgot_window.move(center_x, center_y)
    
        print("Showing Forgot Password UI...")  # 调试输出
        forgot_window.show()
