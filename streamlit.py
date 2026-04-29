import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import urllib.request
from utils.preprocessor import preprocess_input



st.image(
    "tree image.jpg",
    caption="Sustainable AI & Green Energy",
    use_container_width=True
)

st.markdown(
    """
    <p style='text-align: center; font-size:18px;'>
    Building sustainable AI models by balancing <b>accuracy</b> and <b>carbon emissions</b>.
    </p>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Green ML - Model Comparison", layout="centered")

# ---------------- TITLE ----------------
st.title("Green Machine Learning Model Comparison")

st.markdown("""
This application compares multiple machine learning models based on:

- **Accuracy (MSE)**
-  **Carbon Emissions (CO₂ footprint)**

The goal is to select a model that balances **performance and sustainability**.
""")

# ---------------- MODEL METRICS ----------------
st.subheader("Model Performance")

st.markdown("### Mean Squared Error (RMSE)")
st.write("**Linear Regression RMSE:** 0.000280")
st.write("**Random Forest RMSE:** 0.00614")
st.write("**Tuned Random Forest RMSE:** 0.0059")
st.write("**ANN RMSE:** 0.0012")

st.markdown("### 🌍 CO₂ Emissions")
st.write("**Linear Regression CO₂ Emissions:** 0.00000351 kg")
st.write("**Random Forest CO₂ Emissions:** 0.00000414 kg")
st.write("**Tuned Random Forest CO₂ Emissions:** 0.00009304 kg")
st.write("**ANN CO₂ Emissions:** 0.00013170 kg")

# ---------------- COMPARISON TABLE ----------------
st.subheader("Comparison Table")

data = {
    "Model": ["Linear Regression", "Random Forest","Tuned Random Forest", "ANN"],
    "RMSE / Loss": [
        "0.000280",
        "0.00614",
        "0.0059",
        "0.0012"
    ],
    "CO₂ Emissions (kg)": [
        "0.00000351",
        "0.00000414",
        "0.00009304",
        "0.00013170"
    ]
}

st.table(data)

# ---------------- FINAL CONCLUSION ----------------
st.subheader("Final Model Selection")

st.markdown("""
### Conclusion

Hence, the **final model selected is Linear Regression** because it provides the **best trade-off between accuracy and carbon emissions**.

- ✔ Lowest CO₂ emissions  
- ✔ Excellent prediction performance (very low MSE)  
- ✔ Computationally efficient  

This aligns with **Green AI principles**, focusing on both **performance and sustainability**.
""")











# ================================
# Download Model from Google Drive
# ================================
model_path = 'models/LR_model.pkl'
model_file_id = "1QhNBJWO3rCsyryA2QZubj_oLSf28Tsu2"

if not os.path.exists('models'):
    os.makedirs('models')

if not os.path.exists(model_path):
    url = f"https://drive.google.com/uc?id={model_file_id}"
    urllib.request.urlretrieve(url, model_path)

# ================================
# 🔄 Download Scaler from Google Drive
# ================================
scaler_path = 'models/scaler.pkl'
scaler_file_id = '1-glpXEH3tDF4p4wTpsWTHNqtYT04WBSB'

if not os.path.exists(scaler_path):
    url = f"https://drive.google.com/uc?id={scaler_file_id}"
    urllib.request.urlretrieve(url, scaler_path)

# ================================
# ✅ Load Model and Scaler
# ================================
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# ================================
# 🌐 Streamlit UI
# ================================
st.title("Supply Chain Emissions Prediction")

st.markdown("""
This app predicts **Supply Chain Emission Factors with Margins** based on DQ metrics and other parameters.
""")


# Input form
with st.form("prediction_form"):
    st.markdown("### 🌿 Enter Supply Chain Emission Details Below")

    substance = st.selectbox("Select Greenhouse Gas (GHG)", 
        ['carbon dioxide', 'methane', 'nitrous oxide', 'other GHGs'])

    unit = st.selectbox("Unit of Measurement", 
        ['kg/2018 USD, purchaser price', 'kg CO2e/2018 USD, purchaser price'])

    source = st.selectbox("Data Source Type", 
        ['Commodity', 'Industry'])

    supply_wo_margin = st.number_input(
        "Emission Factor (without Margins)", min_value=0.0, 
        help="Base supply chain emission factor before applying uncertainty margin."
    )

    margin = st.number_input(
        "Margin Value", min_value=0.0, 
        help="Represents the uncertainty or error range in emission factor reporting."
    )

    dq_reliability = st.slider(
        "📊 Data Quality - Reliability", 0.0, 1.0, help="How reliable or trustworthy the emission data is."
    )

    dq_temporal = st.slider(
        "🕒 Data Quality - Temporal Correlation", 0.0, 1.0, 
        help="How recent or timely the data is. Higher value = more recent."
    )

    dq_geo = st.slider(
        "🌍 Data Quality - Geographical Correlation", 0.0, 1.0, 
        help="How location-specific the data is. Higher value = better regional accuracy."
    )

    dq_tech = st.slider(
        "⚙️ Data Quality - Technological Correlation", 0.0, 1.0, 
        help="How closely the data aligns with current technologies."
    )

    dq_data = st.slider(
        "📥 Data Quality - Collection Method", 0.0, 1.0, 
        help="Quality of how the data was collected. Higher = better sampling method."
    )

    submit = st.form_submit_button("🔍 Predict Emission")

# Prediction and Explanation
if submit:
    input_data = {
        'Substance': substance,
        'Unit': unit,
        'Supply Chain Emission Factors without Margins': supply_wo_margin,
        'Margins of Supply Chain Emission Factors': margin,
        'DQ ReliabilityScore of Factors without Margins': dq_reliability,
        'DQ TemporalCorrelation of Factors without Margins': dq_temporal,
        'DQ GeographicalCorrelation of Factors without Margins': dq_geo,
        'DQ TechnologicalCorrelation of Factors without Margins': dq_tech,
        'DQ DataCollection of Factors without Margins': dq_data,
        'Source': source,
    }

    input_df = preprocess_input(pd.DataFrame([input_data]))
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]

    # Interpret the result
    if prediction < 0.5:
        level = "✅ Low emissions (Safe)"
        color = "green"
    elif 0.5 <= prediction < 1.5:
        level = "⚠️ Moderate emissions (Review Recommended)"
        color = "orange"
    else:
        level = "🚨 High emissions (Action Required)"
        color = "red"

    st.success(f"🎯 Predicted Emission Factor with Margin: **{prediction:.4f} kg CO₂e / USD**")

    st.markdown(f"### Emission Level: :{color}[{level}]")
    
    st.info(
        f"This means that for every **1 USD** spent in this supply chain activity, "
        f"approximately **{prediction:.4f} kilograms of greenhouse gases** are emitted into the environment."
    )

    st.markdown(
        """
        **🔍 Interpretation:**  
        - This value combines both the **base emission factor** and the **margin of uncertainty**.  
        - Use this information to target **high-emission sectors**, adopt **greener alternatives**, or prioritize **sustainable sourcing**.
        """
    )
    