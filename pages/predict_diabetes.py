import streamlit as st
import pandas as pd
import joblib
import base64
from report import generate_pdf


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Diabetes Predictor",
    page_icon="🩺",
    layout="centered"
)


# =====================================================
# LOGIN CHECK
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.warning("⚠️ Please login first to access the system")
    st.switch_page("login.py")
    st.stop()


# =====================================================
# TITLE
# =====================================================

st.title("🩺 AI Powered Diabetes Predictor")
st.caption("AI-based prediction using patient health data")


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("👤 Doctor Panel")

if st.sidebar.button("🚪 Logout"):

    st.session_state["logged_in"] = False

    # Clear patient information
    st.session_state.pop("patient_data", None)
    st.session_state.pop("prediction", None)
    st.session_state.pop("proba", None)
    st.session_state.pop("patient_gender", None)

    st.switch_page("login.py")


# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():

    data = joblib.load("adaboost_model.pkl")

    if isinstance(data, dict) and "model" in data:
        return data["model"]

    return data


model = load_model()

FEATURES = list(model.feature_names_in_)


# =====================================================
# SOUND FUNCTION
# =====================================================

def play_sound(file):

    try:

        with open(file, "rb") as f:

            audio_data = base64.b64encode(
                f.read()
            ).decode()

        st.markdown(
            f"""
            <audio autoplay>
                <source
                    src="data:audio/mp3;base64,{audio_data}"
                    type="audio/mp3"
                >
            </audio>
            """,
            unsafe_allow_html=True
        )

    except FileNotFoundError:

        pass


# =====================================================
# INPUT SECTION
# =====================================================

st.subheader("📝 Enter Patient Details")

user_inputs = {}


for feature in FEATURES:

    feature_lower = feature.lower()

    # -------------------------------------------------
    # GENDER
    # -------------------------------------------------

    if feature_lower == "gender":

        gender = st.radio(
            "Gender",
            ["Male 👨", "Female 👩"]
        )

        # Human-readable value for PDF
        if gender == "Male 👨":

            st.session_state["patient_gender"] = "Male"

        else:

            st.session_state["patient_gender"] = "Female"

        # Numerical value for ML model
        # Male = 1
        # Female = 0

        user_inputs[feature] = (
            1 if gender == "Male 👨" else 0
        )


    # -------------------------------------------------
    # PREGNANCIES
    # -------------------------------------------------

    elif feature_lower == "pregnancies":

        user_inputs[feature] = st.number_input(
            "Pregnancies",
            min_value=0,
            max_value=20,
            value=0,
            step=1
        )


    # -------------------------------------------------
    # AGE
    # -------------------------------------------------

    elif feature_lower == "age":

        user_inputs[feature] = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25,
            step=1
        )


    # -------------------------------------------------
    # GLUCOSE
    # -------------------------------------------------

    elif feature_lower == "glucose":

        user_inputs[feature] = st.number_input(
            "Glucose",
            min_value=0.0,
            max_value=300.0,
            value=100.0,
            step=1.0
        )


    # -------------------------------------------------
    # BLOOD PRESSURE
    # -------------------------------------------------

    elif feature_lower in [
        "bloodpressure",
        "blood_pressure"
    ]:

        user_inputs[feature] = st.number_input(
            "Blood Pressure",
            min_value=0.0,
            max_value=200.0,
            value=70.0,
            step=1.0
        )


    # -------------------------------------------------
    # SKIN THICKNESS
    # -------------------------------------------------

    elif feature_lower in [
        "skinthickness",
        "skin_thickness"
    ]:

        user_inputs[feature] = st.number_input(
            "Skin Thickness",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0
        )


    # -------------------------------------------------
    # INSULIN
    # -------------------------------------------------

    elif feature_lower == "insulin":

        user_inputs[feature] = st.number_input(
            "Insulin",
            min_value=0.0,
            max_value=1000.0,
            value=80.0,
            step=1.0
        )


    # -------------------------------------------------
    # BMI
    # -------------------------------------------------

    elif feature_lower == "bmi":

        user_inputs[feature] = st.number_input(
            "BMI",
            min_value=0.0,
            max_value=80.0,
            value=25.0,
            step=0.1
        )


    # -------------------------------------------------
    # DIABETES PEDIGREE FUNCTION
    # -------------------------------------------------

    elif feature_lower in [
        "diabetespedigreefunction",
        "diabetes_pedigree_function"
    ]:

        user_inputs[feature] = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.01
        )


    # -------------------------------------------------
    # OTHER NUMERIC FEATURES
    # -------------------------------------------------

    else:

        user_inputs[feature] = st.number_input(
            feature,
            min_value=0.0,
            value=0.0
        )


# =====================================================
# PREDICTION
# =====================================================

if st.button("🔍 Predict", use_container_width=True):

    # Create DataFrame in EXACT model feature order
    input_data = pd.DataFrame(
        [[user_inputs[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    # Prediction
    prediction = model.predict(input_data)[0]

    # Probability
    proba = model.predict_proba(input_data)[0]

    # Convert numpy values to normal Python floats
    proba = [
        float(min(max(p, 0.0), 1.0))
        for p in proba
    ]

    # -------------------------------------------------
    # SAVE PATIENT DATA
    # -------------------------------------------------

    st.session_state["patient_data"] = input_data

    st.session_state["prediction"] = prediction

    st.session_state["proba"] = proba


    # =================================================
    # RESULT
    # =================================================

    st.markdown("---")

    st.subheader("🧠 Prediction Result")


    if prediction == 1:

        st.error(
            "⚠️ High Risk of Diabetes"
        )

        st.snow()

        play_sound("snow.mp3")

    else:

        st.success(
            "✅ Low Risk of Diabetes"
        )

        st.balloons()

        play_sound("balloon.mp3")


    # =================================================
    # PROBABILITY
    # =================================================

    st.subheader("📊 Prediction Probability")

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "🟢 Not Diabetic",
            f"{proba[0] * 100:.2f}%"
        )


    with col2:

        st.metric(
            "🔴 Diabetic",
            f"{proba[1] * 100:.2f}%"
        )


    st.progress(proba[0])

    st.progress(proba[1])


# =====================================================
# PATIENT REPORT
# =====================================================

if "patient_data" in st.session_state:

    st.markdown("---")

    st.subheader("📄 Generate Patient Report")


    if st.button(
        "Generate PDF Report",
        use_container_width=True
    ):

        file_path = generate_pdf(

            st.session_state["patient_data"],

            st.session_state["prediction"],

            st.session_state["proba"],

            # Pass readable gender
            st.session_state.get(
                "patient_gender",
                "Not specified"
            )
        )


        with open(file_path, "rb") as f:

            st.download_button(

                label="⬇️ Download Patient Report",

                data=f.read(),

                file_name="patient_report.pdf",

                mime="application/pdf",

                use_container_width=True
            )


# =====================================================
# DASHBOARD
# =====================================================

st.markdown("---")


if st.button(
    "📊 Go to Dashboard",
    use_container_width=True
):

    st.switch_page(
        "pages/predict_dashboard.py"
    )