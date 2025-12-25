import warnings; warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import os
from fpdf import FPDF

class GradeEngine:
    """
    Advanced Logic Engine for Student Grade Management.
    Handles data persistence (CSV), GPA math, and PDF generation.
    """
    def __init__(self, data_path='data/student_records.csv'):
        self.data_path = data_path
        # Bells University / Nigerian Standard Grading Scale
        self.grading_scale = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        self.load_data()

    def load_data(self):
        """Loads existing data or creates a new structure if none exists."""
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
        else:
            self.df = pd.DataFrame(columns=['Course_Code', 'Units', 'Score', 'Grade', 'GP', 'WP'])

    def calculate_grade(self, score):
        """Standard University grading logic."""
        if score >= 70: return 'A'
        elif score >= 60: return 'B'
        elif score >= 50: return 'C'
        elif score >= 45: return 'D'
        elif score >= 40: return 'E'
        else: return 'F'

    def add_record(self, code, units, score):
        """Adds a course and auto-calculates grade points."""
        grade = self.calculate_grade(score)
        gp = self.grading_scale[grade]
        wp = units * gp
        new_row = pd.DataFrame([{
            'Course_Code': code.upper(), 
            'Units': units, 
            'Score': score, 
            'Grade': grade, 
            'GP': gp, 
            'WP': wp
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.df.to_csv(self.data_path, index=False)

    def get_stats(self):
        """Calculates current GPA and total academic workload."""
        if self.df.empty: return 0.0, 0, 0
        total_units = self.df['Units'].sum()
        total_wp = self.df['WP'].sum()
        gpa = round(total_wp / total_units, 2)
        return gpa, int(total_units), int(total_wp)

    def predict_target(self, target_cgpa, remaining_units):
        """
        Unique Feature: Predicts the GPA needed in future courses 
        to reach a specific target CGPA.
        """
        current_gpa, current_units, current_wp = self.get_stats()
        # Total WP needed = Target * (Current Units + Remaining Units)
        required_total_wp = target_cgpa * (current_units + remaining_units)
        needed_wp = required_total_wp - current_wp
        
        if remaining_units <= 0: return 0.0
        return round(needed_wp / remaining_units, 2)

    def export_pdf(self, student_name="Student"):
        """Generates a professional PDF Result Slip."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"Bells University - Academic Result Slip", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Student: {student_name}", ln=True)
        pdf.ln(5)
        
        # Table Header
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(40, 10, "Course", 1, 0, 'C', True)
        pdf.cell(30, 10, "Units", 1, 0, 'C', True)
        pdf.cell(30, 10, "Score", 1, 0, 'C', True)
        pdf.cell(30, 10, "Grade", 1, 1, 'C', True)

        for _, row in self.df.iterrows():
            pdf.cell(40, 10, str(row['Course_Code']), 1)
            pdf.cell(30, 10, str(row['Units']), 1)
            pdf.cell(30, 10, str(row['Score']), 1)
            pdf.cell(30, 10, str(row['Grade']), 1, 1)

        gpa, _, _ = self.get_stats()
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, f"Cumulative GPA: {gpa}", ln=True)
        
        save_path = "docs/result_slip.pdf"
        pdf.output(save_path)
        return save_path