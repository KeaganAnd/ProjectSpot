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

        # Buttons layout - 只保留下载和分享按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # 增加按钮间距
        button_layout.setContentsMargins(0, 10, 0, 5)  # 上下添加更多间距

        # Define button style 
        button_style = """
            QPushButton {
                background-color: #3a9d6e;  /* 深绿色 */
                color: white;  /* 白色文字 */
                font-weight: bold;  /* 粗体文字 */
                border: none;  /* 无边框 */
                border-radius: 6px;  /* 圆角 */
                padding: 10px 20px;  /* 内边距增加 */
                font-size: 14px;  /* 字体大小增加 */
                min-width: 120px;  /* 最小宽度 */
                min-height: 40px;  /* 最小高度 */
            }
            QPushButton:hover {
                background-color: #4aad7e;  /* 悬停时颜色变亮 */
            }
            QPushButton:pressed {
                background-color: #2e8b57;  /* 按下时颜色变暗 */
            }
        """
        
        # 下载按钮
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.download_comparison)
        self.download_btn.setStyleSheet(button_style)
        button_layout.addWidget(self.download_btn)

        # 分享按钮
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
        
        # Table styling - 使用交替的白色和浅绿色背景
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #a9dfbf;  /* Light green gridlines */
                background-color: white;
                alternate-background-color: #e8f5e9;  /* 更浅的绿色作为交替行背景 */
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
        """下载比较数据为CSV文件"""
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to download.")
            return

        # 获取并确保文件名
        try:
            # 从比较结果中获取两个城市名称用于文件名
            city1_name = self.comparison_result.get("city1", "city1").split(',')[0].strip()
            city2_name = self.comparison_result.get("city2", "city2").split(',')[0].strip()
            default_filename = f"comparison_{city1_name}_vs_{city2_name}.csv"
            
            # 获取保存路径
            filepath, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Comparison as CSV", 
                default_filename, 
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not filepath:
                return  # 用户取消
                
            # 确保文件名有.csv扩展名
            if not filepath.lower().endswith('.csv'):
                filepath += '.csv'
                
            print(f"Saving comparison to: {filepath}")
            
            # 写入CSV文件
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                headers = ["City", "Timestamp"]
                metrics = self.comparison_result.get("metrics", {})
                for metric in metrics.keys():
                    headers.append(metric)
                writer.writerow(headers)
                
                # 写入第一个城市数据
                city1 = self.comparison_result.get("city1", "N/A")
                timestamp = self.comparison_result.get("timestamp", "N/A")
                row1 = [city1, timestamp]
                
                for metric in metrics.keys():
                    value = metrics.get(metric, {}).get(city1, "N/A")
                    row1.append(value)
                writer.writerow(row1)
                
                # 写入第二个城市数据
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
        """分享比较结果到社交媒体"""
        if not self.comparison_result:
            QMessageBox.warning(self, "No Data", "No comparison data to share.")
            return

        try:
            # 准备分享内容
            city1 = self.comparison_result.get("city1", "").split(',')[0].strip()
            city2 = self.comparison_result.get("city2", "").split(',')[0].strip()
            
            # 创建分享文本
            share_text = f"Check out my city comparison between {city1} and {city2} on Spot Finder!"
            metrics = self.comparison_result.get("metrics", {})
            
            # 添加温度比较（如果有）
            temp_key = None
            for key in metrics.keys():
                if "temperature" in key.lower() or "temp" in key.lower():
                    temp_key = key
                    break
                    
            if temp_key and city1 in metrics.get(temp_key, {}) and city2 in metrics.get(temp_key, {}):
                temp1 = metrics[temp_key][city1]
                temp2 = metrics[temp_key][city2]
                share_text += f"\n\nTemperature: {city1}: {temp1}°F vs {city2}: {temp2}°F"
            
            # 添加收入比较（如果有）
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
            
            # URL编码文本用于分享链接
            encoded_text = urllib.parse.quote(share_text)
            
            # 创建分享菜单 - 使用黑色粗体字和交替颜色背景
            share_menu = QMenu(self)
            
            # 设置菜单整体样式 - 黑色粗体字和增加每项高度
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
                /* 为偶数项设置浅绿色背景 */
                QMenu::item:!selected:nth-child(even) {
                    background-color: #e8f5e9;
                }
                /* 为奇数项设置白色背景 */
                QMenu::item:!selected:nth-child(odd) {
                    background-color: white;
                }
            """)
            
            # Twitter选项
            twitter_action = share_menu.addAction("Share on Twitter/X")
            twitter_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://twitter.com/intent/tweet?text={encoded_text}")
                )
            )
            
            # Facebook选项
            facebook_action = share_menu.addAction("Share on Facebook")
            facebook_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.facebook.com/sharer/sharer.php?u=https://spotfinder.app&quote={encoded_text}")
                )
            )
            
            # LinkedIn选项
            linkedin_action = share_menu.addAction("Share on LinkedIn")
            linkedin_action.triggered.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl(f"https://www.linkedin.com/sharing/share-offsite/?url=https://spotfinder.app&summary={encoded_text}")
                )
            )
            
            # 复制到剪贴板选项
            clipboard_action = share_menu.addAction("Copy to Clipboard")
            clipboard_action.triggered.connect(
                lambda: self._copy_to_clipboard(share_text)
            )
            
            # 在分享按钮位置显示菜单
            share_menu.exec(self.share_btn.mapToGlobal(self.share_btn.rect().bottomLeft()))
            
        except Exception as e:
            print(f"Error sharing: {str(e)}")
            QMessageBox.critical(self, "Share Error", f"Could not share comparison: {str(e)}")
    
    def _copy_to_clipboard(self, text):
        """将文本复制到剪贴板"""
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Success", "Comparison copied to clipboard!")