import streamlit as st
import pandas as pd
import joblib
import re

st.set_page_config(page_title="Diabetes Prediction App")

st.title("🩺 Diabetes Prediction Web App")
st.markdown("Decision Tree Classification (0 = No Diabetes, 1 = Diabetes)")

# -------- LOAD TRAINED MODEL --------
@st.cache_resource
def load_model():
    return joblib.load("diabetes_model.pkl")

model = load_model()

# -------- LOAD DATASET FOR ANALYSIS --------
@st.cache_data
def load_data():
    return pd.read_csv("glucose-copy.csv")

data = load_data()

# -------- GENDER COMPARISON --------
st.subheader("📊 Diabetes Comparison: Male vs Female")

data["Gender_Label"] = data["gender"].map({0: "Male", 1: "Female"})
gender_counts = data.groupby(["Gender_Label", "Outcome"]).size().unstack()

st.bar_chart(gender_counts)

# -------- GET FEATURE NAMES FROM MODEL --------
FEATURES = list(model.feature_names_in_)

# -------- USER INPUT --------
st.subheader("📝 Enter Patient Details")

user_inputs = {}

for feature in FEATURES:

    if feature.lower() == "gender":
        gender = st.selectbox("Gender", ["Male", "Female"])
        user_inputs[feature] = 1 if gender == "Female" else 0

    else:
        user_inputs[feature] = st.text_input(feature)

# -------- HELPER FUNCTION --------
def is_number(value):
    return re.fullmatch(r"-?\d+(\.\d+)?", value) is not None

# -------- PREDICTION --------
if st.button("🔍 Predict"):

    values = []

    for v in user_inputs.values():
        if isinstance(v, str):
            values.append(v.strip())
        else:
            values.append(v)

    # Empty check
    if not all(str(v) != "" for v in values):
        st.warning("❗ Please fill all the fields before predicting")

    # Numeric validation
    elif not all(is_number(str(v)) for v in values):
        st.warning("❗ Please enter valid numeric values only")

    else:
        numeric_values = [float(v) for v in values]

        input_data = pd.DataFrame(
            [numeric_values],
            columns=FEATURES
        )

        result = model.predict(input_data)[0]

        if result == 1:
            st.error("⚠️ Person is likely Diabetic")
        else:
            st.success("✅ Person is NOT Diabetic")
```
