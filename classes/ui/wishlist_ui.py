from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QCheckBox, QWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from user.wishlist import save_user_wishlist_data
import functools


class WishlistDialog(QDialog):
    def __init__(self, wishlist_data, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Wishlist")
        self.resize(600, 400)
        self.user_id = user_id  # Store user ID for saving the wishlist

        # Use sets for easier add/remove logic
        self.original_data = set(wishlist_data) if wishlist_data else set()
        self.current_data = set(wishlist_data) if wishlist_data else set()

        # Main layout
        self.layout = QVBoxLayout(self)

        # Wishlist table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["City Name", "Keep"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

        self.load_table(self.current_data)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.close_button = QPushButton("Close")

        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.close_button)

        self.layout.addLayout(self.button_layout)

        # Connect buttons
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button.clicked.connect(self.cancel_changes)
        self.close_button.clicked.connect(self.accept)

    def load_table(self, data):
        self.table.setRowCount(len(data))
        for row, city in enumerate(data):
            # City Name cell
            city_item = QTableWidgetItem(city)
            city_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, 0, city_item)

            # Keep checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                functools.partial(self.on_keep_changed, city_name=city)
            )

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            self.table.setCellWidget(row, 1, widget)

    def on_keep_changed(self, state, city_name):
        """Called when a checkbox is toggled."""
        if state == Qt.CheckState.Unchecked:
            self.current_data.discard(city_name)
        else:
            self.current_data.add(city_name)

    def save_changes(self):
        """Save updated wishlist."""
        updated_data = []

        for row in range(self.table.rowCount()):
            city_item = self.table.item(row, 0)
            checkbox_widget = self.table.cellWidget(row, 1)
            if city_item is None or checkbox_widget is None:
                continue

            city_name = city_item.text()
            checkbox = checkbox_widget.layout().itemAt(0).widget()

            if checkbox.isChecked():
                updated_data.append(city_name)

        self.current_data = set(updated_data)

        save_user_wishlist_data(self.user_id, list(self.current_data))
        self.original_data = self.current_data.copy()

        self.accept()  # Close the dialog

    def cancel_changes(self):
        """Revert changes and reload original wishlist."""
        self.current_data = self.original_data.copy()
        self.load_table(self.current_data)
