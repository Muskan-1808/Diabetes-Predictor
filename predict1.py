import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Diabetes Prediction App")

st.title("🩺 Diabetes Prediction Web App")
st.markdown("Decision Tree Classification (0 = No Diabetes, 1 = Diabetes)")

# -------- LOAD MODEL + ACCURACY --------
@st.cache_resource
def load_model():
    # Load the saved model and accuracy from .pkl
    data = joblib.load("diabetes_model.pkl")
    
    # If your current pkl only has model, use fallback
    if isinstance(data, dict) and "model" in data and "accuracy" in data:
        return data["model"], data["accuracy"]
    else:
        # fallback if only model is saved
        return data, None

model, accuracy = load_model()

# -------- LOAD DATASET --------
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes_data.csv")
    # Clean column names
    df.columns = df.columns.str.strip()
    return df

data = load_data()

# -------- MALE VS FEMALE COMPARISON --------
st.subheader("📊 Diabetes Comparison: Male vs Female")

if "Gender" in data.columns:
    data["Gender_Label"] = data["Gender"].map({0: "Male", 1: "Female"}).fillna("Unknown")
    gender_counts = data.groupby(["Gender_Label", "Outcome"]).size().unstack()
    st.bar_chart(gender_counts)
else:
    st.warning("⚠️ Dataset does not have a 'Gender' column for comparison.")

# -------- GET FEATURE NAMES FROM MODEL --------
FEATURES = list(model.feature_names_in_)

# -------- FEATURE IMPORTANCE --------
st.subheader("⭐ Feature Importance")

importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

st.bar_chart(importance.set_index("Feature"))

# -------- MODEL ACCURACY --------
st.subheader("📈 Model Accuracy")

if accuracy is not None:
    st.metric("Decision Tree Accuracy", f"{accuracy*100:.2f}%")
else:
    st.info("ℹ️ Accuracy not saved in model file. Use training script to save it.")

# -------- USER INPUT FORM --------
st.subheader("📝 Enter Patient Details")

# Prepare dictionary for user input
user_inputs = {}

for feature in FEATURES:
    if feature.lower() == "gender":
        gender = st.selectbox("Gender", ["Male", "Female"])
        user_inputs[feature] = 1 if gender == "Female" else 0
    elif feature.lower() == "age":
        user_inputs[feature] = st.number_input("Age", min_value=0, value=30)
    elif feature.lower() == "pregnancies":
        user_inputs[feature] = st.number_input("Pregnancies", min_value=0, value=0)
    else:
        user_inputs[feature] = st.number_input(feature, min_value=0.0, value=0.0)

# -------- PREDICTION --------
if st.button("🔍 Predict"):
    # Create DataFrame with exact feature order
    input_data = pd.DataFrame([[user_inputs[f] for f in FEATURES]], columns=FEATURES)
    
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    st.subheader("🔍 Prediction Result")

    if prediction == 1:
        st.error("⚠️ Person is likely Diabetic")
    else:
        st.success("✅ Person is NOT Diabetic")

    st.info(f"📊 Probability of NOT Diabetes: {proba[0]*100:.2f}%")
    st.info(f"📊 Probability of Diabetes: {proba[1]*100:.2f}%")