import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Diabetes Prediction App")

st.title("🩺 Diabetes Prediction Web App")
st.markdown("Decision Tree Classification (0 = No Diabetes, 1 = Diabetes)")

# -------- LOAD MODEL --------
@st.cache_resource
def load_model():
    return joblib.load("diabetes_model.pkl")

model = load_model()

# -------- LOAD DATASET --------
@st.cache_data
def load_data():
    return pd.read_csv("diabetes_data.csv")

data = load_data()

# Clean column names
data.columns = data.columns.str.strip()

# -------- MALE VS FEMALE COMPARISON --------
st.subheader("📊 Diabetes Comparison: Male vs Female")

data["Gender_Label"] = data["Gender"].map({0: "Male", 1: "Female"}).fillna("Unknown")

gender_counts = data.groupby(["Gender_Label", "Outcome"]).size().unstack()

st.bar_chart(gender_counts)

# -------- GET FEATURE NAMES FROM MODEL --------
FEATURES = list(model.feature_names_in_)

# -------- FEATURE IMPORTANCE --------
st.subheader("⭐ Feature Importance")

importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(by="Importance", ascending=False)

st.bar_chart(importance.set_index("Feature"))

# -------- MODEL ACCURACY --------
st.subheader("📈 Model Accuracy")

accuracy = 0.78
st.metric("Decision Tree Accuracy", f"{accuracy*100:.2f}%")

# -------- USER INPUT FORM --------
st.subheader("📝 Enter Patient Details")

gender = st.selectbox("Gender", ["Male", "Female"])
gender_value = 1 if gender == "Female" else 0
age = st.number_input("Age", min_value=0)
pregnancies = st.number_input("Pregnancies", min_value=0, value=0)
glucose = st.number_input("Glucose", min_value=0.0)
blood_pressure = st.number_input("Blood Pressure", min_value=0.0)
skin_thickness = st.number_input("Skin Thickness", min_value=0.0)
insulin = st.number_input("Insulin", min_value=0.0)
bmi = st.number_input("BMI", min_value=0.0)
dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)

# -------- PREDICTION --------
if st.button("🔍 Predict"):

    input_data = pd.DataFrame([[ 
        gender_value,
        age,
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        dpf
    ]], columns=FEATURES)

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("🔍 Prediction Result")

    if prediction == 1:
        st.error("⚠️ Person is likely Diabetic")
    else:
        st.success("✅ Person is NOT Diabetic")

    st.info(f"📊 Diabetes Risk Probability: {probability*100:.2f}%")
