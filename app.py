import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(page_title="VH-HouseWorth & Credit Analysis", layout="wide")

# ---------------------------------------------------
# Styling (Clean White + Blue)
# ---------------------------------------------------
st.markdown("""
<style>
body { background-color: #ffffff; color: #111827; }

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
    font-weight: 500;
}
.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}

.big-value {
    font-size: 40px;
    font-weight: 700;
    color: #2563eb;
}

.footer {
    text-align: center;
    margin-top: 60px;
    font-size: 14px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Helper: Format Currency
# ---------------------------------------------------
def format_currency(value):
    if value >= 1e7:
        return f"{value/1e7:.2f} Cr"
    elif value >= 1e5:
        return f"{value/1e5:.2f} L"
    else:
        return f"{value:,.0f}"

# ---------------------------------------------------
# Load Model & Data
# ---------------------------------------------------
model = joblib.load("models/house_price_model.pkl")
data = pd.read_csv("data/housing_data.csv")

growth_rates = {
    "Mumbai": 0.07,
    "Delhi": 0.065,
    "Bengaluru": 0.09,
    "Pune": 0.08,
    "Hyderabad": 0.085,
    "Chennai": 0.07,
    "Kolkata": 0.06,
    "Ahmedabad": 0.065,
    "Jaipur": 0.06,
    "Lucknow": 0.055
}

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown("<h1 style='text-align:center;'>VH-HouseWorth & Credit Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#6b7280;'>Property Valuation & Financial Risk Intelligence</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================
# PROPERTY SECTION
# =====================================================

with st.expander("Property Valuation & Forecast", expanded=True):

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("City", list(growth_rates.keys()))
        area = st.number_input("Area (sq ft)", 300, 5000, 1000)
        bhk = st.slider("BHK", 1, 5, 2)
        bathrooms = st.slider("Bathrooms", 1, 4, 2)

    with col2:
        parking = st.selectbox("Parking Available", [0, 1])
        location = st.selectbox("Location Type", ["Premium", "Standard", "Developing"])
        age = st.slider("Property Age (years)", 0, 30, 5)
        furnishing = st.selectbox("Furnishing", ["Furnished", "Semi-Furnished", "Unfurnished"])

    if st.button("Estimate Property Value"):

        input_data = pd.DataFrame([{
            "city": city,
            "area_sqft": area,
            "bhk": bhk,
            "bathrooms": bathrooms,
            "parking": parking,
            "location_type": location,
            "property_age": age,
            "furnishing": furnishing
        }])

        prediction = model.predict(input_data)[0]

        st.subheader("Estimated Current Market Value")
        st.markdown(f"<div class='big-value'>{format_currency(prediction)}</div>", unsafe_allow_html=True)

        # Market Range
        city_data = data[data["city"] == city]
        min_price = city_data["price"].min()
        avg_price = city_data["price"].mean()
        max_price = city_data["price"].max()

        st.markdown("#### Market Range")
        c1, c2, c3 = st.columns(3)
        c1.metric("Lowest", format_currency(min_price))
        c2.metric("Average", format_currency(avg_price))
        c3.metric("Highest", format_currency(max_price))

        # Forecast
        rate = growth_rates[city]
        price_3 = prediction * ((1 + rate) ** 3)
        price_5 = prediction * ((1 + rate) ** 5)
        price_7 = prediction * ((1 + rate) ** 7)

        st.markdown(f"Projected values are calculated based on estimated current value at **{rate*100:.1f}% annual growth rate**.")

        f1, f2, f3 = st.columns(3)
        f1.metric("3 Years", format_currency(price_3))
        f2.metric("5 Years", format_currency(price_5))
        f3.metric("7 Years", format_currency(price_7))

        # Forecast Chart
        years = [0, 3, 5, 7]
        values = [prediction, price_3, price_5, price_7]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title="Projected Property Growth",
            xaxis_title="Years from Now",
            yaxis_title="Estimated Value (₹)",
            template="simple_white",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CREDIT SECTION
# =====================================================

with st.expander("Credit & Loan Risk Assessment", expanded=False):

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input("Monthly Income (₹)", 10000, 1000000, 50000)
        existing_emi = st.number_input("Existing Monthly EMI (₹)", 0, 500000, 10000)

    with col2:
        loan_amount = st.number_input("Desired Loan Amount (₹)", 500000, 50000000, 2000000)
        tenure = st.slider("Loan Tenure (Years)", 5, 30, 20)

    if st.button("Evaluate Loan Profile"):

        dti = existing_emi / income
        lti = loan_amount / (income * 12)

        base_rate = 8.5

        if dti < 0.30 and lti < 4:
            category = "Low Risk"
            rate_adjust = -0.3
        elif dti < 0.45 and lti < 6:
            category = "Moderate Risk"
            rate_adjust = 0.0
        else:
            category = "High Risk"
            rate_adjust = 0.8

        final_rate = base_rate + rate_adjust
        monthly_rate = final_rate / 100 / 12
        months = tenure * 12

        emi = (loan_amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

        st.subheader("Credit Profile")
        st.success(f"Risk Category: {category}")

        c1, c2 = st.columns(2)
        c1.metric("Estimated Interest Rate", f"{final_rate:.2f}%")
        c2.metric("Estimated Monthly EMI", f"₹ {emi:,.0f}")

        emi_ratio = emi / income

        if emi_ratio < 0.30:
            st.success("Loan appears financially comfortable.")
        elif emi_ratio < 0.45:
            st.warning("Loan is manageable but moderately stretched.")
        else:
            st.error("Loan may create financial stress.")

        # EMI vs Income Chart
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=["Income", "EMI"],
            y=[income, emi],
            marker_color=["#2563eb", "#ef4444"]
        ))

        fig2.update_layout(
            title="Income vs EMI Comparison",
            template="simple_white",
            height=400
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("""
<div class="footer">
Built by Vinay Hulsurkar aka VH24<br>
&copy VH24 2026 <br>
<a href="https://github.com/KaizenVH24" target="_blank">GitHub</a> |
<a href="https://linkedin.com/in/vinayhulsurkar" target="_blank">LinkedIn</a> |
<a href="https://leetcode.com/vinayhulsurkar24" target="_blank">LeetCode</a>
</div>
""", unsafe_allow_html=True)