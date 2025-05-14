import csv
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLabel,
    QHeaderView, QSizePolicy, QScrollArea, QMenu, QApplication
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices
from datetime import datetime
import urllib.parse
import os

class ComparisonUI(QDialog):
    def __init__(self, parent_window, comparison_data=None):
        super().__init__(parent_window)
        self.setWindowTitle("City Comparison")
        self.resize(800, 600)
        self.setMinimumSize(500, 400)
        
        self.parent = parent_window
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
        button_layout.setSpacing(15)  
        button_layout.setContentsMargins(0, 10, 0, 5)  

        # Define button style 
        button_style = """
            QPushButton {
                background-color: #3a9d6e;  
                color: white;  
                font-weight: bold;
                border: none;  
                border-radius: 6px;  
                padding: 10px 20px;  
                font-size: 14px; 
                min-width: 120px;  
                min-height: 40px;  
            }
            QPushButton:hover {
                background-color: #4aad7e;  
            }
            QPushButton:pressed {
                background-color: #2e8b57; 
            }
        """
        
        # Download button
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.download_comparison)
        self.download_btn.setStyleSheet(button_style)
        button_layout.addWidget(self.download_btn)

        # Share Button
        self.share_btn = QPushButton("Share")
        self.share_btn.clicked.connect(self.share_comparison)
        self.share_btn.setStyleSheet(button_style)
        button_layout.addWidget(self.share_btn)
                
        self.layout.addLayout(button_layout)
        
        # Display the data
        if self.comparison_result:
            self.empty_label.setVisible(False)
            self.display_comparison_result()
        else:
            self.table.setVisible(False)

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
                gridline-color: #a9dfbf;  
                background-color: white;
                alternate-background-color: #e8f5e9;  
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

    def download_comparison(self):
        """Download comparison result"""
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to download.")
            return

        
        try:
            
            city1_name = self.comparison_result.get("city1", "city1").split(',')[0].strip()
            city2_name = self.comparison_result.get("city2", "city2").split(',')[0].strip()
            default_filename = f"comparison_{city1_name}_vs_{city2_name}.csv"
            
            
            filepath, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Comparison as CSV", 
                default_filename, 
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not filepath:
                return  
                
           
            if not filepath.lower().endswith('.csv'):
                filepath += '.csv'
                
            print(f"Saving comparison to: {filepath}")
            
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                
                headers = ["City", "Timestamp"]
                metrics = self.comparison_result.get("metrics", {})
                for metric in metrics.keys():
                    headers.append(metric)
                writer.writerow(headers)
                
               
                city1 = self.comparison_result.get("city1", "N/A")
                timestamp = self.comparison_result.get("timestamp", "N/A")
                row1 = [city1, timestamp]
                
                for metric in metrics.keys():
                    value = metrics.get(metric, {}).get(city1, "N/A")
                    row1.append(value)
                writer.writerow(row1)
                
                city2 = self.comparison_result.get("city2", "N/A")
                row2 = [city2, timestamp]
                
                for metric in metrics.keys():
                    value = metrics.get(metric, {}).get(city2, "N/A")
                    row2.append(value)
                writer.writerow(row2)
            
            QMessageBox.information(self, "Success", f"Comparison data saved to {filepath}")
            
        except Exception as e:
            print(f"Error downloading CSV: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to download comparison: {str(e)}")

    def share_comparison(self):
        """Share on social media"""
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to share.")
            return

        try:
            # geT comparison result
            city1 = self.comparison_result.get("city1", "").split(',')[0].strip()
            city2 = self.comparison_result.get("city2", "").split(',')[0].strip()
            
            # create share text
            share_text = f"Check out my city comparison between {city1} and {city2} on Spot Finder!"
            metrics = self.comparison_result.get("metrics", {})
            
            # add temp
            temp_key = None
            for key in metrics.keys():
                if "temperature" in key.lower() or "temp" in key.lower():
                    temp_key = key
                    break
                    
            if temp_key and city1 in metrics.get(temp_key, {}) and city2 in metrics.get(temp_key, {}):
                temp1 = metrics[temp_key][city1]
                temp2 = metrics[temp_key][city2]
                share_text += f"\n\nTemperature: {city1}: {temp1}°F vs {city2}: {temp2}°F"
            
            # add income comparison
            income_key = None
            for key in metrics.keys():
                if "income" in key.lower():
                    income_key = key
                    break
                    
            if income_key and city1 in metrics.get(income_key, {}) and city2 in metrics.get(income_key, {}):
                try:
                    income1 = int(metrics[income_key][city1])
                    income2 = int(metrics[income_key][city2])
                    share_text += f"\nMedian Income: {city1}: ${income1:,} vs {city2}: ${income2:,}"
                except (ValueError, TypeError):
                    pass
                    
            share_text += "\n\n#SpotFinder #CityComparison"
                        
            encoded_text = urllib.parse.quote(share_text)
            
            # Share menu
            share_menu = QMenu(self)
            
            # Set Menu Style
            share_menu.setStyleSheet("""
                QMenu {
                    font-family: Arial;
                    font-weight: bold;
                    color: black;
                    background-color: white;
                    border: 1px solid #a9dfbf;
                }
                QMenu::item {
                    padding: 10px 30px 10px 30px;
                    min-width: 200px;
                }
                QMenu::item:selected {
                    background-color: #a9dfbf;
                }
                
                QMenu::item:!selected:nth-child(even) {
                    background-color: #e8f5e9;
                }
               
                QMenu::item:!selected:nth-child(odd) {
                    background-color: white;
                }
            """)
            
            # Twitter Option
            twitter_action = share_menu.addAction("Share on Twitter/X")
            twitter_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://twitter.com/intent/tweet?text={encoded_text}")
                )
            )
            
            # Facebook Option
            facebook_action = share_menu.addAction("Share on Facebook")
            facebook_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.facebook.com/sharer/sharer.php?u=https://spotfinder.app&quote={encoded_text}")
                )
            )
            
            # LinkedIn Option
            linkedin_action = share_menu.addAction("Share on LinkedIn")
            linkedin_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.linkedin.com/sharing/share-offsite/?url=https://spotfinder.app&summary={encoded_text}")
                )
            )
            
            # Copy to clipboard option
            clipboard_action = share_menu.addAction("Copy to Clipboard")
            clipboard_action.triggered.connect(
                lambda: self._copy_to_clipboard(share_text)
            )
            
            # Dislay share menu
            share_menu.exec(self.share_btn.mapToGlobal(self.share_btn.rect().bottomLeft()))
            
        except Exception as e:
            print(f"Error sharing: {str(e)}")
            QMessageBox.critical(self, "Share Error", f"Could not share comparison: {str(e)}")
    
    def _copy_to_clipboard(self, text):
        """Copy to clipboard"""
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Success", "Comparison copied to clipboard!")
