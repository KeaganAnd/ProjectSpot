from PyQt6.QtWidgets import QMenuBar, QMenu, QLabel, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import Qt
import os

from classes.ui.ui_router import (
    open_login,
    open_register,
    open_wishlist,
    open_comparison,
    open_profile_dialog  
)
from classes.ui.wishlist_ui import WishlistDialog

def add_account_menu(window):
    menubar: QMenuBar = window.menuBar()
    menubar.setStyleSheet("QMenu::icon { width: 20px; height: 20px; }")
    
    # Clear previous menu
    menubar.clear()

    # Load and scale the account icon
    icon_path = os.path.join(os.path.dirname(__file__), "imgs", "account.png")
    account_icon = QIcon(QPixmap(icon_path).scaled(36, 36))

    # Create "Account" menu
    account_menu = menubar.addMenu(account_icon, "Account")
    account_menu.setStyleSheet("QMenu { font-weight: bold; font-size: 16px; }")

    # Load submenu icons
    icon_dir = os.path.join(os.path.dirname(__file__), "imgs")
    icons = {
        "login": QIcon(os.path.join(icon_dir, "login.jpg")),
        "register": QIcon(os.path.join(icon_dir, "register.png")),
        "wishlist": QIcon(os.path.join(icon_dir, "heart.png")),
        "compare": QIcon(os.path.join(icon_dir, "compareButton.png")),
        "profile": QIcon(os.path.join(icon_dir, "profile.png")),
        "logout": QIcon(os.path.join(icon_dir, "logout.png"))
    }

    # --- Actions ---
    login_action = QAction(icons["login"], "Login", window)
    login_action.triggered.connect(lambda _: open_login(window))
    account_menu.addAction(login_action)

    register_action = QAction(icons["register"], "Register", window)
    register_action.triggered.connect(lambda _: open_register(window))
    account_menu.addAction(register_action)

    wishlist_action = QAction(icons["wishlist"], "My Wishlist", window)
    wishlist_action.triggered.connect(lambda _: show_wishlist(window))
    account_menu.addAction(wishlist_action)

    compare_action = QAction(icons["compare"], "City Comparison", window)
    compare_action.triggered.connect(lambda _: window.open_comparison_dialog())
    account_menu.addAction(compare_action)

    profile_action = QAction(icons["profile"], "My Profile", window)
    profile_action.triggered.connect(lambda _: open_profile_dialog(window))  
    account_menu.addAction(profile_action)

    logout_action = QAction(icons["logout"], "Logout", window)
    logout_action.triggered.connect(lambda _: window.logout_user())
    account_menu.addAction(logout_action)

    # --- Show logged-in username (if available) ---
    if getattr(window, "current_username", ""):
        username = window.current_username
        username_label = QLabel(f"Logged in as: <b>{username}</b>")
        username_label.setStyleSheet("margin-right: 20px; color: #333; font-size: 13px;")

        # Put the label in a QWidget layout and add it to the top-right corner of the menu bar
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addStretch()
        layout.addWidget(username_label)
        layout.setContentsMargins(0, 0, 10, 0)
        container.setLayout(layout)

        menubar.setCornerWidget(container, Qt.Corner.TopRightCorner)

def show_wishlist(main_window):
    wishlist_data = main_window.get_current_wishlist() 
    wishlist_dialog = WishlistDialog(wishlist_data, main_window.user_id, main_window) 
    wishlist_dialog.exec()
