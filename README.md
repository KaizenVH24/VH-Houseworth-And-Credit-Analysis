# VH-HouseWorth & Credit Analysis

A property valuation and financial risk intelligence system built using Machine Learning and Streamlit.

This project estimates residential property prices across major Indian cities, forecasts long-term value growth and evaluates loan affordability based on financial risk indicators.

It is designed as a practical, end-to-end ML application - from dataset generation and model validation to UI design and deployment.

---

## What This Project Does

### 1️. Property Valuation  
- Predicts house price based on:
  - City  
  - Area (sq ft)  
  - BHK  
  - Bathrooms  
  - Parking  
  - Location type  
  - Property age  
  - Furnishing status  
- Shows city-level:
  - Lowest market value  
  - Average market value  
  - Highest market value  

---

### 2️. Investment Forecast  
- Projects future property value for:
  - 3 years  
  - 5 years  
  - 7 years  
- Uses city-specific annual growth rates  
- Includes visual growth chart  
- Clearly states projection assumptions  

---

### 3️. Credit & Loan Risk Assessment  
- Evaluates:
  - Debt-to-Income Ratio (DTI)  
  - Loan-to-Income Ratio (LTI)  
- Classifies user risk profile:
  - Low Risk  
  - Moderate Risk  
  - High Risk  
- Dynamically adjusts estimated interest rate  
- Calculates EMI using standard financial formula  
- Performs affordability check  
- Displays income vs EMI comparison chart  

---

## Machine Learning Approach

- Synthetic but realistic housing dataset generated with:
  - Skewed area distribution  
  - BHK-area correlation  
  - City-based pricing differences  
  - Market noise and volatility  
- Model:
  - Random Forest Regressor  
  - OneHot Encoding via ColumnTransformer  
  - Full Pipeline for deployment consistency  
- Evaluation:
  - Train-test split  
  - 5-fold cross-validation  
  - MAE, RMSE, R² metrics  
- Feature importance analysis included  

Current performance (after realism improvements):

- R² ≈ 0.96–0.97  
- Stable cross-validation results  

---

## Visual Analytics

- Forecast growth line chart (Plotly)  
- EMI vs Income comparison bar chart  
- Large headline-style property valuation display  
- Values formatted in Lakhs / Crores for readability  

---

## Tech Stack

- Python  
- Pandas  
- NumPy  
- Scikit-Learn  
- Plotly  
- Streamlit  
- Joblib  

---

## Project Structure

│
├── app.py
├── generate_dataset.py
├── train_model.py
│
├── data/
│ └── housing_data.csv
│
├── models/
│ └── house_price_model.pkl
│
├── requirements.txt
└── README.md


---

##  How To Run Locally

1. Clone the repository  

2. Create a virtual environment  

3. Install dependencies: pip install -r requirements.txt

4. Run the application: streamlit run app.py

---

## Why This Project Matters

Most ML projects stop at prediction.

This project goes further:

- Combines ML + financial logic  
- Integrates forecasting  
- Includes explainable evaluation  
- Focuses on user-centric presentation  
- Bridges technical modeling with practical decision-making  

It is built to simulate how a real-world financial analytics product would behave.

---

## Built By

VH24 aka Vinay Hulsurkar

- GitHub: https://github.com/KaizenVH24  
- LinkedIn: https://linkedin.com/in/vinayhulsurkar  
- LeetCode: https://leetcode.com/vinayhulsurkar24  