import streamlit as st
import pandas as pd
import joblib
import base64
from report import generate_pdf

# =====================================================
# 🔐 LOGIN CHECK (IMPORTANT - MUST BE FIRST)
# =====================================================

# Check login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.warning("⚠️ Please login first to access the system")
    st.switch_page("login.py")   # use this if login.py is the main/root file
    st.stop()
# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Diabetes Predictor", layout="centered")

st.title("🩺 Diabetes Predictor Web App")
st.caption("AI-based prediction using patient health data")

# =====================================================
# LOGOUT BUTTON
# =====================================================
st.sidebar.title("👤 Doctor Panel")

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.switch_page("login.py")

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    data = joblib.load("diabetes_model.pkl")
    if isinstance(data, dict) and "model" in data:
        return data["model"]
    return data

model = load_model()
FEATURES = list(model.feature_names_in_)

# =====================================================
# SOUND FUNCTION
# =====================================================
def play_sound(file):
    with open(file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# INPUT SECTION
# =====================================================
st.subheader("📝 Enter Patient Details")

user_inputs = {}

for feature in FEATURES:

    if feature.lower() == "gender":
        gender = st.radio("Gender", ["Male 👨", "Female 👩"])
        user_inputs[feature] = 1 if gender == "Male 👨" else 0

    elif feature.lower() in ["age", "pregnancies"]:
        user_inputs[feature] = st.number_input(feature, min_value=0, value=0)

    else:
        user_inputs[feature] = st.number_input(feature, value=0.0)

# =====================================================
# PREDICTION
# =====================================================
if st.button("🔍 Predict"):

    input_data = pd.DataFrame([user_inputs], columns=FEATURES)

    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    # SAVE SESSION
    st.session_state["patient_data"] = input_data
    st.session_state["prediction"] = prediction
    st.session_state["proba"] = proba

    st.markdown("---")
    st.subheader("🧠 Result")

    if prediction == 1:
        st.error("⚠️ High Risk of Diabetes")
        st.snow()
        play_sound("snow.mp3")
    else:
        st.success("✅ Low Risk of Diabetes")
        st.balloons()
        play_sound("balloon.mp3")

    st.subheader("📊 Probability")

    proba = [float(min(max(p, 0), 1)) for p in proba]

    st.metric("Not Diabetic", f"{proba[0]*100:.2f}%")
    st.metric("Diabetic", f"{proba[1]*100:.2f}%")

    st.progress(proba[0])
    st.progress(proba[1])

# =====================================================
# REPORT SECTION
# =====================================================
if st.session_state.get("patient_data") is not None:

    st.markdown("---")
    st.subheader("📄 Generate Patient Report")

    if st.button("Generate PDF Report"):

        file_path = generate_pdf(
            st.session_state["patient_data"],
            st.session_state["prediction"],
            st.session_state["proba"]
        )

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download Report",
                data=f,
                file_name="patient_report.pdf",
                mime="application/pdf"
            )

# =====================================================
# NAVIGATION
# =====================================================
st.markdown("---")

if st.button("📊 Go to Dashboard"):
    st.switch_page("pages/predict_dashboard.py")
    
