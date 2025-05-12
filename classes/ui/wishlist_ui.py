from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QCheckBox, QWidget, QHeaderView, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
import os
import json
import functools

class WishlistDialog(QDialog):
    def __init__(self, wishlist_data, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Wishlist")
        self.resize(600, 400)
        self.parent = parent  # Store parent for updating
        self.user_id = user_id  # Store user ID for saving the wishlist
        
        # Use lists for data
        self.original_data = list(wishlist_data) if wishlist_data else []
        self.current_data = list(wishlist_data) if wishlist_data else []
        
        # Dictionary to store checkboxes
        self.checkboxes = {}
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Display user info
        if self.user_id:
            username = ""
            if hasattr(parent, 'current_username'):
                username = parent.current_username
            
            info_label = QLabel(f"Wishlist for: {username} (ID: {user_id})")
            info_label.setStyleSheet("color: green; font-weight: bold;")
            main_layout.addWidget(info_label)
        
        # Instructions
        instructions = QLabel("Select cities to keep in your wishlist:")
        main_layout.addWidget(instructions)
        
        # Wishlist table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["City Name", "Keep in Wishlist"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 120)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                background-color: #ffffff;
                alternate-background-color: #f8f8f8;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                font-weight: bold;
                border: none;
            }
        """)
        main_layout.addWidget(self.table)
        
        # Load cities into table
        self.load_table()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_style = """
            QPushButton {
                background-color: #2e8b57;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a9d6e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """
        
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(button_style)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(button_style)
        
        self.delete_all_button = QPushButton("Delete All")
        self.delete_all_button.setStyleSheet(button_style)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.delete_all_button)
        
        main_layout.addLayout(button_layout)
        
        # Connect buttons
        self.save_button.clicked.connect(self.save_changes)
        self.cancel_button.clicked.connect(self.reject)  # Just close the dialog
        self.delete_all_button.clicked.connect(self.delete_all)
        
        # Initially enable save button
        self.save_button.setEnabled(True)
    
    def load_table(self):
        """Load cities into the table"""
        # Clear existing items
        self.table.setRowCount(0)
        self.checkboxes.clear()
        
        # No cities message
        if not self.current_data:
            self.table.setRowCount(1)
            item = QTableWidgetItem("No cities in wishlist")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(0, 0, item)
            # Hide the checkbox column for empty wishlist
            self.table.setColumnHidden(1, True)
            return
        
        # Show checkbox column
        self.table.setColumnHidden(1, False)
        
        # Add cities
        self.table.setRowCount(len(self.current_data))
        for row, city in enumerate(self.current_data):
            # City Name cell
            city_item = QTableWidgetItem(city)
            city_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, 0, city_item)
            
            # Keep checkbox
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            
            checkbox = QCheckBox()
            checkbox.setChecked(True)  # Default to checked
            
            # Connect state change signal
            checkbox.stateChanged.connect(
                lambda state, row=row: self.on_checkbox_changed(state, row)
            )
            
            # Store checkbox in dictionary with row as key
            self.checkboxes[row] = checkbox
            
            checkbox_layout.addWidget(checkbox)
            checkbox_widget.setLayout(checkbox_layout)
            
            self.table.setCellWidget(row, 1, checkbox_widget)
    
    def on_checkbox_changed(self, state, row):
        """Handle checkbox state change"""
        checked = state == Qt.CheckState.Checked
        
        # Get city name from the table
        city_item = self.table.item(row, 0)
        if city_item:
            city = city_item.text()
            print(f"City '{city}' checkbox changed to: {'checked' if checked else 'unchecked'}")
    
    def delete_all(self):
        """Uncheck all cities"""
        # Ask for confirmation
        reply = QMessageBox.question(
            self, 
            "Delete All",
            "Are you sure you want to remove ALL cities from your wishlist?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Uncheck all checkboxes
            for row, checkbox in self.checkboxes.items():
                checkbox.setChecked(False)
            
            # Enable save button
            self.save_button.setEnabled(True)
    
    def save_changes(self):
        """Save updated wishlist"""
        # Collect cities to keep
        cities_to_keep = []
        
        for row in range(self.table.rowCount()):
            city_item = self.table.item(row, 0)
            if city_item and row in self.checkboxes and self.checkboxes[row].isChecked():
                cities_to_keep.append(city_item.text())
        
        print(f"Cities to keep: {cities_to_keep}")
        
        # First try to save using the standard method
        try:
            from user.wishlist import save_user_wishlist_data
            success = save_user_wishlist_data(self.user_id, cities_to_keep)
            if not success:
                # If standard method fails, try direct save
                success = self.save_direct_to_file(cities_to_keep)
        except Exception as e:
            print(f"Error using standard save method: {e}")
            # Try direct save as fallback
            success = self.save_direct_to_file(cities_to_keep)
        
        if success:
            # Update parent window wishlist if it exists
            if self.parent and hasattr(self.parent, 'wishlist'):
                self.parent.wishlist = cities_to_keep
                print(f"Updated parent.wishlist with {len(cities_to_keep)} cities")
            
            # Show success message
            QMessageBox.information(self, "Success", "Your wishlist has been updated successfully!")
            self.accept()  # Close dialog
        else:
            QMessageBox.warning(self, "Error", "Failed to save wishlist changes.")
    
    def save_direct_to_file(self, wishlist_data):
        """save to dir"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            data_dir = os.path.join(base_dir, 'data')
            if not os.path.exists(data_dir):
                try:
                    os.makedirs(data_dir)
                except Exception as e:
                    print(f"Could not create data directory: {e}")
                    # save to current dir
                    data_dir = os.path.join(os.path.dirname(__file__), 'data')
                    if not os.path.exists(data_dir):
                        os.makedirs(data_dir)
            
            # save as JSON file
            file_path = os.path.join(data_dir, f'wishlist_{self.user_id}.json')
            
            print(f"Saving to file: {file_path}")
            print(f"Data to save: {wishlist_data}")
            
            with open(file_path, 'w') as f:
                json.dump(wishlist_data, f)
            
            print(f"Save successful to {file_path}")
            return True
        except Exception as e:
            import traceback
            print(f"Error saving to file: {e}")
            print(traceback.format_exc())
            
            # save to tempfile
            try:
                import tempfile
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, f'wishlist_{self.user_id}.json')
                
                with open(file_path, 'w') as f:
                    json.dump(wishlist_data, f)
                
                print(f"Save successful to temp file: {file_path}")
                return True
            except Exception as temp_error:
                print(f"Final save attempt failed: {temp_error}")
                return False