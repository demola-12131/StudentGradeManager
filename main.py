import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, 
                             QTabWidget, QFrame, QHeaderView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

# Importing our custom modules from the src folder [cite: 116, 117]
from src.engine import GradeEngine
from src.visuals import AnalyticsCanvas

class BellsAcademicPlanner(QMainWindow):
    """
    Main Application Window for the Student Grade Management System.
    Fulfills the 'Proper GUI' and 'Interactive Charts' requirements[cite: 38, 70, 72].
    """
    def __init__(self):
        super().__init__()
        
        # Initialize the calculation engine
        self.engine = GradeEngine()
        
        # UI Setup [cite: 72]
        self.setWindowTitle("Bells University | Smart Academic Planner v1.0")
        self.resize(1200, 850)
        self.set_modern_style()
        
        # Central Tab Widget 
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialize Tabs
        self.init_dashboard_tab()
        self.init_predictor_tab()
        self.init_settings_tab()
        
        # Initial data load [cite: 73]
        self.refresh_ui_data()

    def set_modern_style(self):
        """Applies a professional dark-themed CSS (Unique Feature)."""
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; }
            QTabWidget::pane { border: 1px solid #1e293b; top: -1px; background-color: #0f172a; }
            QTabBar::tab {
                background: #1e293b; color: #94a3b8; padding: 12px 30px;
                border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px;
            }
            QTabBar::tab:selected { background: #3b82f6; color: white; }
            QLabel { color: #f8fafc; font-family: 'Segoe UI'; }
            QLineEdit { 
                background-color: #1e293b; color: white; border: 1px solid #334155; 
                padding: 10px; border-radius: 6px; font-size: 14px;
            }
            QPushButton { 
                background-color: #3b82f6; color: white; font-weight: bold; 
                padding: 12px; border-radius: 6px; border: none;
            }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton#danger { background-color: #ef4444; }
            QTableWidget { 
                background-color: #1e293b; color: white; border-radius: 8px;
                gridline-color: #334155; font-size: 13px;
            }
            QHeaderView::section { background-color: #334155; color: white; padding: 5px; }
        """)

    def init_dashboard_tab(self):
        """Main Dashboard with Data Entry and Analytics Visualizations[cite: 32, 75]."""
        self.dashboard = QWidget()
        layout = QHBoxLayout(self.dashboard)
        
        # LEFT PANEL: Control & Entry
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)
        
        header = QLabel("Academic Input")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        
        self.course_in = QLineEdit(); self.course_in.setPlaceholderText("Course Code (e.g., CVE311)")
        self.units_in = QLineEdit(); self.units_in.setPlaceholderText("Credit Units (1-6)")
        self.score_in = QLineEdit(); self.score_in.setPlaceholderText("Exam Score (0-100)")
        
        save_btn = QPushButton("Save Record")
        save_btn.clicked.connect(self.handle_save)
        
        pdf_btn = QPushButton("Generate PDF Result Slip")
        pdf_btn.setStyleSheet("background-color: #10b981;")
        pdf_btn.clicked.connect(self.handle_pdf_export)
        
        left_panel.addWidget(header)
        left_panel.addWidget(QLabel("Course Details:"))
        left_panel.addWidget(self.course_in)
        left_panel.addWidget(self.units_in)
        left_panel.addWidget(self.score_in)
        left_panel.addWidget(save_btn)
        left_panel.addWidget(pdf_btn)
        left_panel.addStretch()
        
        # RIGHT PANEL: Table & Visuals
        right_panel = QVBoxLayout()
        
        # GPA Stats Cards
        stats_layout = QHBoxLayout()
        self.gpa_card = QLabel("GPA: 0.00")
        self.gpa_card.setStyleSheet("font-size: 36px; font-weight: bold; color: #60a5fa; background: #1e293b; padding: 20px; border-radius: 10px;")
        stats_layout.addWidget(self.gpa_card)
        
        # Table [cite: 73]
        self.result_table = QTableWidget(0, 4)
        self.result_table.setHorizontalHeaderLabels(["Course", "Units", "Score", "Grade"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Analytics Visuals [cite: 75]
        self.canvas = AnalyticsCanvas()
        
        right_panel.addLayout(stats_layout)
        right_panel.addWidget(self.result_table)
        right_panel.addWidget(self.canvas)
        
        layout.addLayout(left_panel, 1)
        layout.addLayout(right_panel, 3)
        self.tabs.addTab(self.dashboard, "Performance Dashboard")

    def init_predictor_tab(self):
        """GPA Prediction Engine (Unique Competitive Advantage)[cite: 74]."""
        self.predictor = QWidget()
        layout = QVBoxLayout(self.predictor)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = QLabel("Target GPA Strategy Planner")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        
        desc = QLabel("Enter your target CGPA and the units you have left to find out what you need to score.")
        desc.setWordWrap(True)
        
        self.target_cgpa = QLineEdit(); self.target_cgpa.setPlaceholderText("Target CGPA (e.g., 4.50)")
        self.remaining_units = QLineEdit(); self.remaining_units.setPlaceholderText("Remaining Units in Semester")
        
        calc_btn = QPushButton("Calculate Required Grade Points")
        calc_btn.clicked.connect(self.handle_prediction)
        
        self.pred_output = QLabel("")
        self.pred_output.setStyleSheet("font-size: 18px; color: #fbbf24; padding: 20px;")
        
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(self.target_cgpa)
        layout.addWidget(self.remaining_units)
        layout.addWidget(calc_btn)
        layout.addWidget(self.pred_output)
        
        self.tabs.addTab(self.predictor, "GPA Predictor")

    def init_settings_tab(self):
        """System management and data clearing."""
        self.settings = QWidget()
        layout = QVBoxLayout(self.settings)
        
        clear_btn = QPushButton("Clear All Records (Reset System)")
        clear_btn.setObjectName("danger")
        clear_btn.clicked.connect(self.handle_reset)
        
        layout.addWidget(QLabel("System Maintenance"))
        layout.addWidget(clear_btn)
        layout.addStretch()
        self.tabs.addTab(self.settings, "Settings")

    def handle_save(self):
        """Validates input and saves to CSV via Engine[cite: 73, 76]."""
        try:
            code = self.course_in.text()
            units = int(self.units_in.text())
            score = float(self.score_in.text())
            
            if not (0 <= score <= 100) or not (1 <= units <= 6):
                raise ValueError
                
            self.engine.add_record(code, units, score)
            self.refresh_ui_data()
            self.course_in.clear(); self.units_in.clear(); self.score_in.clear()
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid course data.\nUnits: 1-6\nScore: 0-100")

    def handle_prediction(self):
        """Calculates needed GPA for target CGPA[cite: 74]."""
        try:
            target = float(self.target_cgpa.text())
            units = int(self.remaining_units.text())
            result = self.engine.predict_target(target, units)
            
            if result > 5.0:
                msg = f"Warning: You need a GPA of {result}. This is impossible on a 5.0 scale."
            else:
                msg = f"To achieve {target} CGPA, you must maintain an average GPA of {result} in your remaining units."
            
            self.pred_output.setText(msg)
        except:
            QMessageBox.critical(self, "Error", "Input valid numbers for prediction.")

    def handle_pdf_export(self):
        """Triggers PDF generation for result slip[cite: 57, 75]."""
        path = self.engine.export_pdf()
        QMessageBox.information(self, "PDF Export", f"Result slip exported to {path}")

    def handle_reset(self):
        """Wipes the CSV data file[cite: 73]."""
        reply = QMessageBox.question(self, 'Reset Data', "Are you sure you want to delete all records?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if os.path.exists(self.engine.data_path):
                os.remove(self.engine.data_path)
            self.engine.load_data()
            self.refresh_ui_data()

    def refresh_ui_data(self):
        """Updates Table, Stats, and Charts from Engine state[cite: 73, 74, 75]."""
        # 1. Update the GPA and Units display
        gpa, total_units, _ = self.engine.get_stats()
        self.gpa_card.setText(f"CGPA: {gpa}  |  Total Units: {total_units}")
        
        # 2. Update the Results Table
        self.result_table.setRowCount(0)
        for i, row in self.engine.df.iterrows():
            self.result_table.insertRow(i)
            # Fills the table with Course Code, Units, Score, and Grade
            self.result_table.setItem(i, 0, QTableWidgetItem(str(row['Course_Code'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(str(row['Units'])))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(row['Score'])))
            self.result_table.setItem(i, 3, QTableWidgetItem(str(row['Grade'])))
            
        # 3. Refresh the interactive charts
        self.canvas.update_charts(self.engine.df)

# THIS MUST BE AT THE VERY END OF main.py
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Optional: Setting a professional font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = BellsAcademicPlanner()
    window.show()
    sys.exit(app.exec())