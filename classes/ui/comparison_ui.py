import csv
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLabel,
    QHeaderView, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime


class ComparisonUI(QDialog):
    def __init__(self, parent_window, comparison_data=None):
        super().__init__(parent_window)
        self.setWindowTitle("City Comparison")
        self.resize(800, 600)
        self.setMinimumSize(500, 400)
        
        self.window = parent_window
        self.comparison_result = comparison_data[0] if comparison_data else None

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Label if no data
        self.empty_label = QLabel("No comparison data available.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.empty_label)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Table widget
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.scroll_area.setWidget(self.table)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Define button style 
        button_style = """
            QPushButton {
                background-color: #3a9d6e;  /* Slightly lighter deep green */
                color: white;  /* White text */
                font-weight: bold;  /* Bold text */
                border: none;  /* No border */
                border-radius: 4px;  /* Rounded corners */
                padding: 8px 15px;  /* Padding */
            }
            QPushButton:hover {
                background-color: #4aad7e;  /* Slightly lighter green on hover */
            }
            QPushButton:pressed {
                background-color: #2e8b57;  /* Slightly darker green when pressed */
            }
        """

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_comparison)
        self.save_btn.setMinimumWidth(100)
        self.save_btn.setStyleSheet(button_style)  # Apply style
        button_layout.addWidget(self.save_btn)

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.download_comparison)
        self.download_btn.setMinimumWidth(100)
        self.download_btn.setStyleSheet(button_style)  # Apply style
        button_layout.addWidget(self.download_btn)

        self.share_btn = QPushButton("Share")
        self.share_btn.clicked.connect(self.share_comparison)
        self.share_btn.setMinimumWidth(100)
        self.share_btn.setStyleSheet(button_style)  # Apply style
        button_layout.addWidget(self.share_btn)

                
        self.layout.addLayout(button_layout)
        
        # Display the data
        if self.comparison_result:
            self.empty_label.setVisible(False)
            self.display_comparison_result()
        else:
            self.table.setVisible(False)

    def is_user_logged_in(self):
        """Check if the user is logged in"""
        if hasattr(self.window, 'user_id') and self.window.user_id:
            return True
    
        if hasattr(self.window, 'current_user_id') and self.window.current_user_id:
            return True
        
        return False
    
    def is_user_logged_in(self):
        """Check if the user is logged in"""
        try:            
            if hasattr(self.parent, 'is_user_logged_in') and callable(getattr(self.parent, 'is_user_logged_in')):
                return self.parent.is_user_logged_in()
            
        
            if hasattr(self.parent, 'user_id') and self.parent.user_id:
                print(f"User is logged in with user_id: {self.parent.user_id}")
                return True
        
            if hasattr(self.parent, 'current_user_id') and self.parent.current_user_id:
                print(f"User is logged in with current_user_id: {self.parent.current_user_id}")
                return True
            
            print("User is NOT logged in")
            return False
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False  

    def update_button_states(self):
        """Update button states based on user login status"""
        is_logged_in = self.is_user_logged_in()
        
        print(f"Updating comparison buttons, logged in: {is_logged_in}")
        if hasattr(self.window, 'current_username'):
            print(f"User: {self.window.current_username}")
        
        # Set button enabled state
        self.save_btn.setEnabled(is_logged_in)
        self.download_btn.setEnabled(is_logged_in)
        self.share_btn.setEnabled(is_logged_in)
        
        # Set button tooltip
        login_tip = "Please log in to use this feature" if not is_logged_in else ""
        self.save_btn.setToolTip(login_tip)
        self.download_btn.setToolTip(login_tip)
        self.share_btn.setToolTip(login_tip)
        
        # Set button style
        if is_logged_in:
            self.save_btn.setStyleSheet(self.button_style)
            self.download_btn.setStyleSheet(self.button_style)
            self.share_btn.setStyleSheet(self.button_style)
        else:
            self.save_btn.setStyleSheet(self.disabled_style)
            self.download_btn.setStyleSheet(self.disabled_style)
            self.share_btn.setStyleSheet(self.disabled_style)

    def display_comparison_result(self):
        self.table.clear()

        city1 = self.comparison_result.get("city1", "N/A")
        city2 = self.comparison_result.get("city2", "N/A")
        timestamp = self.comparison_result.get("timestamp", "N/A")
        metrics = self.comparison_result.get("metrics", {})

        headers = ["City", "Timestamp"] + list(metrics.keys())
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(2)
        
        # Format headers with HTML tags for line breaks
        for col, header_text in enumerate(headers):
            # Use HTML to format header text
            if header_text == "precipitation (in last 7 days)":
                header_text = "Precipitation(in last 7 days)"
            elif header_text == "temperature (°F)":
                header_text = "Temperature(°F)"
            elif header_text == "violent crimes (2023)":
                header_text = "Violent Crimes(2023)"
            elif header_text == "people in poverty":
                header_text = "People in Poverty"
            elif header_text == "median income":
                header_text = "Median Income"
            elif header_text == "state description":
                header_text = "State Description"
            
            header_item = QTableWidgetItem(header_text)
            
            # Set bold font
            font = QFont()
            font.setBold(True)
            font.setPointSize(11)  # Set explicit font size
            header_item.setFont(font)
            
            # Ensure text wrapping is enabled
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            
            # Set the header item
            self.table.setHorizontalHeaderItem(col, header_item)
        
        # Force header height and style
        header = self.table.horizontalHeader()
        header.setMinimumHeight(100)  # Set explicit minimum height
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set default column widths
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, 180)
        
        # Use enhanced CSS styling with light green header background
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #d5f5e3 !important;  /* Light green */
                padding: 8px !important;
                border: 1px solid #a9dfbf !important;  /* Light green border */
                font-weight: bold !important;
                text-align: center !important;
                font-size: 12px !important;
                padding-left: 10px !important;
                padding-right: 10px !important;
                padding-top: 10px !important;
                padding-bottom: 10px !important;
                min-height: 80px !important;
                white-space: normal !important;
                qproperty-wordWrap: true !important;
            }
        """)
        
        # Table styling
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #a9dfbf;  /* Light green gridlines */
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QTableWidget::item {
                padding: 5px;
                white-space: normal;
            }
        """)

        # City 1
        self.table.setItem(0, 0, QTableWidgetItem(city1))
        self.table.setItem(0, 1, QTableWidgetItem(timestamp))
        for col, metric in enumerate(headers[2:], start=2):
            value = metrics.get(metric, {}).get(city1, "N/A")
            
            # Format values based on metric type
            if metric == "precipitation (in last 7 days)":
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"{float(value):.2f} in"
                    except (ValueError, TypeError):
                        formatted_value = f"{value} in"
                else:
                    formatted_value = f"{value} in"
                item = QTableWidgetItem(formatted_value)
            elif metric == "temperature (°F)":
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"{float(value):.1f} °F"
                    except (ValueError, TypeError):
                        formatted_value = f"{value} °F"
                else:
                    formatted_value = f"{value} °F"
                item = QTableWidgetItem(formatted_value)
            elif "income" in metric.lower():
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"${int(float(value)):,}"
                    except (ValueError, TypeError):
                        formatted_value = f"${value}"
                else:
                    formatted_value = f"${value}"
                item = QTableWidgetItem(formatted_value)
            elif "poverty" in metric.lower() or "%" in str(value):
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        if "%" in str(value):
                            formatted_value = f"{value}"
                        else:
                            formatted_value = f"{float(value):.1f}%"
                    except (ValueError, TypeError):
                        formatted_value = f"{value}%"
                else:
                    formatted_value = f"{value}%"
                item = QTableWidgetItem(formatted_value)
            else:
                item = QTableWidgetItem(str(value))
            
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(0, col, item)

        # City 2
        self.table.setItem(1, 0, QTableWidgetItem(city2))
        self.table.setItem(1, 1, QTableWidgetItem(timestamp))
        for col, metric in enumerate(headers[2:], start=2):
            value = metrics.get(metric, {}).get(city2, "N/A")
            
            # Same formatting logic as above
            if metric == "precipitation (in last 7 days)":
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"{float(value):.2f} in"
                    except (ValueError, TypeError):
                        formatted_value = f"{value} in"
                else:
                    formatted_value = f"{value} in"
                item = QTableWidgetItem(formatted_value)
            elif metric == "temperature (°F)":
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"{float(value):.1f} °F"
                    except (ValueError, TypeError):
                        formatted_value = f"{value} °F"
                else:
                    formatted_value = f"{value} °F"
                item = QTableWidgetItem(formatted_value)
            elif "income" in metric.lower():
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        formatted_value = f"${int(float(value)):,}"
                    except (ValueError, TypeError):
                        formatted_value = f"${value}"
                else:
                    formatted_value = f"${value}"
                item = QTableWidgetItem(formatted_value)
            elif "poverty" in metric.lower() or "%" in str(value):
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    try:
                        if "%" in str(value):
                            formatted_value = f"{value}"
                        else:
                            formatted_value = f"{float(value):.1f}%"
                    except (ValueError, TypeError):
                        formatted_value = f"{value}%"
                else:
                    formatted_value = f"{value}%"
                item = QTableWidgetItem(formatted_value)
            else:
                item = QTableWidgetItem(str(value))
            
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(1, col, item)
        
        # Set row heights
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 40)
        
        # Disable auto resize mode, use fixed mode instead
        for col in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        
        # Force update table layout
        self.table.resizeRowsToContents()
        self.table.viewport().update()

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        
        if hasattr(self, 'table') and self.table.isVisible():
            width = self.width()
            if width < 600:
                if self.table.columnCount() > 3:
                    self.table.setColumnWidth(0, int(width * 0.3))
                    self.table.setColumnWidth(1, int(width * 0.3))
                    remaining_width = int(width * 0.4)
                    for col in range(2, self.table.columnCount()):
                        col_width = int(remaining_width / (self.table.columnCount() - 2))
                        self.table.setColumnWidth(col, col_width)
            
            self.table.resizeRowsToContents()
            
            # Ensure header height is always sufficient
            header = self.table.horizontalHeader()
            if header.height() < 80:
                header.setMinimumHeight(80)

    def save_comparison(self):
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to save.")
            return

        # Use the new is_user_logged_in method to check login status
        if not self.is_user_logged_in():
            QMessageBox.warning(self, "Not Logged In", "Please log in to save comparison data.")
            return

        try:
            from user.comparison_database import add_city_to_comparison
            metrics = self.comparison_result.get("metrics", {})
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for city in [self.comparison_result["city1"], self.comparison_result["city2"]]:
                add_city_to_comparison(
                    city,
                    metrics.get("population", {}).get(city, "N/A"),
                    metrics.get("gdp_per_capita", {}).get(city, "N/A"),
                    metrics.get("temperature (°F)", {}).get(city, "N/A"),
                    "Compared",
                    timestamp
                )
            QMessageBox.information(self, "Saved", "Comparison data saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {e}")

    def download_comparison(self):
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to download.")
            return

        # Added login check
        if not self.is_user_logged_in():
            QMessageBox.warning(self, "Not Logged In", "Please log in to download comparison data.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not filepath:
            return

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                metrics = self.comparison_result.get("metrics", {})
                headers = ["City", "Timestamp"] + list(metrics.keys())
                writer.writerow(headers)

                for city in [self.comparison_result["city1"], self.comparison_result["city2"]]:
                    row = [city, self.comparison_result.get("timestamp", "N/A")]
                    for metric in headers[2:]:
                        row.append(metrics.get(metric, {}).get(city, "N/A"))
                    writer.writerow(row)

            QMessageBox.information(self, "Success", "Comparison data downloaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download file: {e}")

    def share_comparison(self):
        """Share the comparison result"""
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to share.")
            return

        # check if user login
        if not self.is_user_logged_in():
            QMessageBox.warning(self, "Not Logged In", "Please log in to share comparison data.")
            return

        try:
            from PyQt6.QtWidgets import QMenu, QApplication
            from PyQt6.QtGui import QDesktopServices
            from PyQt6.QtCore import QUrl
            import urllib.parse
            
            # prepare the content
            city1 = self.comparison_result.get("city1", "")
            city2 = self.comparison_result.get("city2", "")
            metrics = self.comparison_result.get("metrics", {})
            
            # create share text
            share_text = f"Check out my city comparison between {city1} and {city2} on Spot Finder!"
            
            
            if "Temperature (°F)" in metrics:
                temp1 = metrics["Temperature (°F)"].get(city1, "N/A")
                temp2 = metrics["Temperature (°F)"].get(city2, "N/A")
                share_text += f"\n\nTemperature: {city1}: {temp1}°F vs {city2}: {temp2}°F"
            
            share_text += "\n\n#SpotFinder #CityComparison"
                        
            encoded_text = urllib.parse.quote(share_text)
            
            # create share menu
            share_menu = QMenu(self)
            
            # Add options to share on Twitter/X 
            twitter_action = share_menu.addAction("Share on Twitter/X")
            twitter_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://twitter.com/intent/tweet?text={encoded_text}")
                )
            )
            
            # Add options to shre on Fackbook
            facebook_action = share_menu.addAction("Share on Facebook")
            facebook_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.facebook.com/sharer/sharer.php?u=https://spotfinder.app&quote={encoded_text}")
                )
            )
            
            # Add options to share on LinkedIn
            linkedin_action = share_menu.addAction("Share on LinkedIn")
            linkedin_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.linkedin.com/sharing/share-offsite/?url=https://spotfinder.app&summary={encoded_text}")
                )
            )
            
            # Copy to Clipboard
            clipboard_action = share_menu.addAction("Copy to Clipboard")
            clipboard_action.triggered.connect(
                lambda: QApplication.clipboard().setText(share_text)
            )
            
            share_menu.exec(self.share_btn.mapToGlobal(self.share_btn.rect().bottomLeft()))
            
        except Exception as e:
            QMessageBox.critical(self, "Share Error", f"Could not share comparison: {e}")

        def share_comparison(self):
            if not self.comparison_result:
                QMessageBox.warning(self, "No Data", "No comparison data to share.")
                return

            # Added login check
            if not self.is_user_logged_in():
                QMessageBox.warning(self, "Not Logged In", "Please log in to share comparison data.")
                return

            metrics = self.comparison_result.get("metrics", {})
            headers = ["City", "Timestamp"] + list(metrics.keys())
            text = ""

            for city in [self.comparison_result["city1"], self.comparison_result["city2"]]:
                row = [city, self.comparison_result.get("timestamp", "N/A")]
                for metric in headers[2:]:
                    row.append(str(metrics.get(metric, {}).get(city, "N/A")))
                text += ", ".join(row) + "\n"

            QMessageBox.information(self, "Share", f"Comparison data:\n\n{text}")

