from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
import csv
from datetime import datetime

class ComparisonUI(QDialog):
    def __init__(self, parent_window, comparison_data=None):
        super().__init__(parent_window)
        self.setWindowTitle("City Comparison")
        self.window = parent_window
        self.comparison_results = comparison_data if comparison_data else []

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Label if no data
        self.empty_label = QLabel("No comparison data available.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.empty_label)

        # Table widget
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Buttons layout
        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_comparison)
        button_layout.addWidget(save_btn)

        download_btn = QPushButton("Download")
        download_btn.clicked.connect(self.download_comparison)
        button_layout.addWidget(download_btn)

        share_btn = QPushButton("Share")
        share_btn.clicked.connect(self.share_comparison)
        button_layout.addWidget(share_btn)

        self.layout.addLayout(button_layout)

        # Initialize table if data exists
        if self.comparison_results:
            self.update_comparison_results(self.comparison_results)

    def update_comparison_results(self, results):
        if not results:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.empty_label.setVisible(True)
            return

        self.comparison_results = results
        self.empty_label.setVisible(False)
        self.display_comparison_results()

    def display_comparison_results(self):
        self.table.clear()

        if not self.comparison_results:
            return

        recent = self.comparison_results[-1]
        headers = ["City", "Timestamp"] + list(recent["metrics"].keys())

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(2)

        city1 = recent.get("city1", "N/A")
        city2 = recent.get("city2", "N/A")
        timestamp = recent.get("timestamp", "N/A")
        metrics = recent.get("metrics", {})

        self.table.setItem(0, 0, QTableWidgetItem(city1))
        self.table.setItem(0, 1, QTableWidgetItem(timestamp))
        self.table.setItem(1, 0, QTableWidgetItem(city2))
        self.table.setItem(1, 1, QTableWidgetItem(timestamp))

        for col, metric in enumerate(headers[2:], start=2):
            val1 = metrics.get(metric, {}).get(city1, "N/A")
            val2 = metrics.get(metric, {}).get(city2, "N/A")
            self.table.setItem(0, col, QTableWidgetItem(str(val1)))
            self.table.setItem(1, col, QTableWidgetItem(str(val2)))

    def save_comparison(self):
        if not self.comparison_results:
            QMessageBox.warning(self, "No Data", "No comparison data to save.")
            return

        user_id = getattr(self.window, "current_user_id", None)
        if not user_id:
            QMessageBox.warning(self, "Not Logged In", "Please log in to save comparison data.")
            return

        try:
            from user.comparison_database import add_city_to_comparison
            recent = self.comparison_results[-1]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Assuming your metrics dictionary has 'population', 'gdp_per_capita', 'avg_temp'
            # Adjust these keys based on your actual data structure
            metrics = recent.get("metrics", {})

            for city in [recent["city1"], recent["city2"]]:
                add_city_to_comparison(
                    city,
                    metrics.get("population", {}).get(city, "N/A"),
                    metrics.get("gdp_per_capita", {}).get(city, "N/A"),
                    metrics.get("temperature (°F)", {}).get(city, "N/A"), # Adjusted key to match your stored data
                    "Compared",
                    timestamp
                )
            QMessageBox.information(self, "Saved", "Comparison data saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {e}")

    def download_comparison(self):
        if not self.comparison_results:
            QMessageBox.warning(self, "No Data", "No comparison data to download.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not filepath:
            return

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                recent = self.comparison_results[-1]
                headers = ["City", "Timestamp"] + list(recent["metrics"].keys())
                writer.writerow(headers)

                for city_index, city in enumerate([recent["city1"], recent["city2"]]):
                    row = [city, recent.get("timestamp", "N/A")]
                    for metric in headers[2:]:
                        value = recent["metrics"].get(metric, {}).get(city, "N/A")
                        row.append(value)
                    writer.writerow(row)

            QMessageBox.information(self, "Success", "Comparison data downloaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download file: {e}")

    def share_comparison(self):
        if not self.comparison_results:
            QMessageBox.warning(self, "No Data", "No comparison data to share.")
            return

        recent = self.comparison_results[-1]
        headers = ["City", "Timestamp"] + list(recent["metrics"].keys())
        rows = []

        for city in [recent["city1"], recent["city2"]]:
            row = [city, recent.get("timestamp", "N/A")]
            for metric in headers[2:]:
                value = recent["metrics"].get(metric, {}).get(city, "N/A")
                row.append(str(value))
            rows.append(", ".join(row))

        text = "City Comparison Results:\n" + ", ".join(headers) + "\n" + "\n".join(rows)

        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Comparison results copied to clipboard.")