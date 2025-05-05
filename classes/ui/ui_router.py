from PyQt6.QtWidgets import (
    QMessageBox, QDialog, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from classes.ui.register_ui import RegisterUI
from classes.ui.login_ui import LoginUI
from classes.ui.comparison_ui import ComparisonUI
from classes.ui.wishlist_ui import WishlistDialog
from classes.ui.profile_dialog import MyProfileDialog

from user.wishlist import get_user_wishlist_data, save_user_wishlist_data

# Store references to open windows to prevent garbage collection
open_windows = []

def center_window(child_window, parent):
    """Center a child window over its parent."""
    child_window.resize(500, 400)
    width = child_window.width()
    height = child_window.height()

    if parent:
        parent_geometry = parent.geometry()
        center_x = parent_geometry.x() + (parent_geometry.width() - width) // 2
        center_y = parent_geometry.y() + (parent_geometry.height() - height) // 2
    else:
        screen = child_window.screen().geometry()
        center_x = screen.x() + (screen.width() - width) // 2
        center_y = screen.y() + (screen.height() - height) // 2

    child_window.move(center_x, center_y)

def open_login(parent=None):
    """Open the login window."""
    login_window = LoginUI(parent)
    login_window.setWindowModality(Qt.WindowModality.NonModal)
    login_window.setWindowFlag(Qt.WindowType.Window)
    login_window.show()
    center_window(login_window, parent)
    open_windows.append(login_window)

def open_register(parent=None):
    """Open the registration window."""
    register_window = RegisterUI(parent)
    register_window.setWindowModality(Qt.WindowModality.NonModal)
    register_window.setWindowFlag(Qt.WindowType.Window)
    register_window.show()
    center_window(register_window, parent)
    open_windows.append(register_window)

def open_forgot_password(parent=None):
    """Open the forgot password window."""
    from classes.ui.forgot_password_ui import ForgotPasswordUI
    forgot_window = ForgotPasswordUI(parent)
    forgot_window.setWindowModality(Qt.WindowModality.NonModal)
    forgot_window.setWindowFlag(Qt.WindowType.Window)
    forgot_window.show()
    center_window(forgot_window, parent)
    open_windows.append(forgot_window)

def open_wishlist(parent_window, user_id):
    """Open the wishlist dialog."""
    wishlist_data = get_user_wishlist_data(user_id)
    
    if hasattr(parent_window, "wishlist_dialog") and parent_window.wishlist_dialog:
        parent_window.wishlist_dialog.reload(wishlist_data)
        parent_window.wishlist_dialog.raise_()
        parent_window.wishlist_dialog.activateWindow()
    else:
        dialog = WishlistDialog(wishlist_data, parent=parent_window, user_id=user_id)
        parent_window.wishlist_dialog = dialog  
        dialog.finished.connect(lambda: setattr(parent_window, "wishlist_dialog", None))  
        dialog.exec()

def open_comparison(main_window):
    """Open the city comparison window."""
    comparison_data = main_window.get_current_comparisons()  
    window = ComparisonUI(main_window, comparison_data)
    
    print(f"Data passed to ComparisonUI: {comparison_data}")
    
    window.update_comparison_results(comparison_data) 
    window.exec()  

def handle_logout(parent=None):
    """Display a logout message."""
    msg = QMessageBox(parent)
    msg.setWindowTitle("Logout")
    msg.setText("You have been logged out.")
    msg.exec()

    clear_user_info(parent)
    open_login(parent)

def update_heart_button_and_wishlist(current_window, user_id, city_name, heart_button):
    """Add or remove city from wishlist and update heart icon."""
    wishlist_data = get_user_wishlist_data(user_id)

    if city_name in wishlist_data:
        wishlist_data.remove(city_name)
        heart_button.setIcon(QIcon("classes/ui/imgs/heart.png"))  # Empty heart
    else:
        wishlist_data.append(city_name)
        heart_button.setIcon(QIcon("classes/ui/imgs/heartEmpty.png"))  # Filled heart

    save_user_wishlist_data(user_id, wishlist_data)

def open_profile_dialog(window):
    """Open the My Profile dialog."""
    dialog = MyProfileDialog(window)
    dialog.exec()

def clear_user_info(window):
    """Clear the current user's stored information."""
    window.current_username = ""
    window.current_user_id = ""
    window.current_email = ""

# Clear open windows when they are closed
def remove_closed_window(window):
    if window in open_windows:
        open_windows.remove(window)
