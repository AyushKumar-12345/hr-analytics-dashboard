# 👥 HR Analytics & Employee Attrition Intelligence

An end-to-end People Analytics project analyzing 1,470 employee records to uncover core turnover drivers, demographic attrition patterns, and compensation benchmarks. Built with Python data engineering, custom dark executive styling, and an interactive Power BI & Streamlit dashboard.

---

## 🎯 Executive Overview
This project transforms raw workforce data into actionable talent retention metrics. It evaluates employee attrition across departments, salary bands, tenure cohorts, and role levels to give HR leaders data-backed retention strategies.

---

## 📊 Core Workforce KPIs
* Total Workforce: 1,470
* Active Headcount: 1,233 (83.88%)
* Attrition Count: 237 (16.12%)
* Average Employee Age: 36.92 years
* Average Monthly Income: $6,503
* Average Tenure: 7.01 years

---

## 🛠️ Tech Stack & Scripts
* Python (Pandas, NumPy, Pillow):
  * process_hr_data.py: Drops invariant features, builds vectorized Age Brackets and Salary Bands, generates numeric attrition flags, and outputs HR_Data_cleaned.csv.
  * generate_hr_bg.py: Generates a 1920x1080 anti-banded corporate dark canvas (HR_Analytics_Background.png).
* Power BI Desktop:
  * High-contrast glassmorphic dark theme (HR_Analytics_Theme.json).
  * Custom DAX modeling for dynamic headcount and attrition slicing.
* Streamlit & Plotly (app.py):
  * Interactive web dashboard with real-time demographic filtering and deep catalog search.

---

## 📐 Primary DAX Measures
* Total Employees = COUNTROWS('HR_Data_cleaned')
* Attrition Count = CALCULATE(COUNTROWS('HR_Data_cleaned'), 'HR_Data_cleaned'[Attrition] = "Yes")
* Attrition Rate = DIVIDE([Attrition Count], [Total Employees], 0)
* Active Headcount = CALCULATE(COUNTROWS('HR_Data_cleaned'), 'HR_Data_cleaned'[Attrition] = "No")
* Avg Monthly Salary = AVERAGE('HR_Data_cleaned'[MonthlyIncome])

---

## 💡 Strategic HR Insights
1. Tenure Risk Window: Turnover is heavily concentrated in years 1 through 3, identifying onboarding and early-career engagement as critical intervention points.
2. Compensation Elasticity: Employees in the Low Salary Band (<$5,000/mo) exhibit an attrition rate nearly double that of the High Band.
3. Department Dynamics: Sales and R&D drive the highest absolute turnover volumes, particularly among Laboratory Technicians and Sales Representatives.
4. Overtime Impact: Employees frequently logging overtime show significantly higher departure likelihood compared to non-overtime peers.

---

## 🚀 How to Run the Project
1. Install dependencies:
   pip install pandas numpy pillow streamlit plotly
2. Run data transformation:
   python process_hr_data.py
3. Run background canvas generator:
   python generate_hr_bg.py
4. Launch interactive web dashboard:
   streamlit run app.py
5. Power BI:
   Open HR Analytics Dashboard.pbix and refresh data sources.

---

## 📁 Repository Structure
* HR_Data_cleaned.csv - Cleaned workforce dataset
* HR_Analytics_Theme.json - Executive glassmorphism Power BI theme
* HR_Analytics_Background.png - High-res canvas background
* process_hr_data.py - Data cleaning and feature engineering script
* generate_hr_bg.py - Canvas generation script
* app.py - Streamlit web application
* requirements.txt - App deployment dependencies
* HR Analytics Dashboard.pbix - Power BI dashboard report
* Screenshots/ - Dashboard preview visuals
* README.md - Project documentation

---

## 👤 Author
* Name: Ayush Kumar
* GitHub: [AyushKumar-12345](https://github.com/AyushKumar-12345)
