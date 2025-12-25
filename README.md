# Smart Academic Planner & GPA Predictor v1.0
**Bells University of Technology - New Horizons ICT Project (ICT323)**

## 📌 Project Overview
The **Smart Academic Planner** is a high-performance Python desktop application designed to help students manage academic records, visualize performance trends, and strategically plan their path to a target CGPA. 

[cite_start]Unlike basic calculators, this system utilizes **Predictive Modeling** to determine the exact grades required in future semesters to achieve a specific graduation class[cite: 32, 34].

## 🚀 Key Features
- [cite_start]**Modern GUI:** Built with PyQt6 for a professional, dark-themed user experience[cite: 38].
- [cite_start]**Data Analytics:** Interactive grade distribution and performance trend charts using Matplotlib and Seaborn[cite: 37, 38, 75].
- [cite_start]**GPA Predictor:** Logic-driven tool to calculate required future performance based on current standing[cite: 74].
- [cite_start]**Data Persistence:** Automatic CSV-based storage to ensure student records are saved locally[cite: 73, 89].
- [cite_start]**Official Export:** Generates a professional PDF Result Slip using the FPDF2 library[cite: 57, 103].

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **GUI Framework:** PyQt6
- [cite_start]**Data Handling:** Pandas, NumPy [cite: 37]
- [cite_start]**Visualization:** Matplotlib, Seaborn [cite: 37]
- **Document Generation:** FPDF2
- [cite_start]**Environment:** Docker (Recommended for compatibility) [cite: 23]

## 📂 Repository Structure
[cite_start]按照 guidelines [cite: 104-121]:
- `/src`: Core Python modules (`engine.py`, `visuals.py`)
- `/data`: Student record storage (`student_records.csv`)
- `/assets`: UI icons and university logos
- `/docs`: Project Report (Chapters 1-5) and User Manual
- `main.py`: Application entry point

## 📥 Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[Your-Username]/StudentGradeManager.git