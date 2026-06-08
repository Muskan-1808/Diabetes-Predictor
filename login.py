import streamlit as st

st.title("🩺 Diabetes Predictor Web App")
st.markdown("### 🔐 Doctor Login")

USERNAME = "doctor"
PASSWORD = "1234"

u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Login"):
    if u == USERNAME and p == PASSWORD:
        st.session_state["logged_in"] = True
        st.switch_page("pages/predict_diabetes.py")
    else:
        st.error("Invalid credentials")