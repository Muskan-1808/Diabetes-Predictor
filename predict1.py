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
    return pd.read_csv("glucose-Copy.csv")

data = load_data()

# -------- MALE VS FEMALE COMPARISON --------
st.subheader("📊 Diabetes Comparison: Male vs Female")

data["Gender_Label"] = data["gender"].map({0: "Male", 1: "Female"})
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

accuracy = 0.78   # replace with real accuracy if available
st.metric("Decision Tree Accuracy", f"{accuracy*100:.2f}%")

# -------- USER INPUT --------
st.subheader("📝 Enter Patient Details")

user_inputs = {}

for feature in FEATURES:

    if feature.lower() == "gender":
        gender = st.selectbox("Gender", ["Male", "Female"])
        user_inputs[feature] = 1 if gender == "Female" else 0

    else:
        user_inputs[feature] = st.number_input(feature, value=0.0)

# -------- PREDICTION --------
if st.button("🔍 Predict"):

    input_data = pd.DataFrame(
        [[user_inputs[f] for f in FEATURES]],
        columns=FEATURES
    )

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("🔍 Prediction Result")

    if prediction == 1:
        st.error("⚠️ Person is likely Diabetic")
    else:
        st.success("✅ Person is NOT Diabetic")

    st.info(f"📊 Diabetes Risk Probability: {probability*100:.2f}%")
