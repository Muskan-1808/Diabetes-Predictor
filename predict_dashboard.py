import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Diabetes Intelligence Dashboard")

# =====================================================
# 🧍 PATIENT DASHBOARD
# =====================================================

st.header("🧍 Patient-Specific Insights")

if "patient_data" not in st.session_state:
    st.warning("⚠️ No patient selected. Please go back and predict first.")

else:
    df = st.session_state["patient_data"]
    prediction = st.session_state["prediction"]
    proba = st.session_state["proba"]

    st.subheader("🧾 Patient Details")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error("⚠️ High Risk")
        else:
            st.success("✅ Low Risk")

    with col2:
        st.metric("Diabetic Probability", f"{proba[1]*100:.2f}%")

    st.subheader("📊 Probability Chart")

    fig, ax = plt.subplots()
    ax.bar(["Not Diabetic", "Diabetic"], proba)
    st.pyplot(fig)

# =====================================================
# 🌍 DATASET DASHBOARD
# =====================================================

st.header("🌍 Population-Level Insights")

df = pd.read_csv("diabetes_data.csv")

if 'Gender' in df.columns:
    df['Gender'] = df['Gender'].map({0: 'Male', 1: 'Female'})

st.dataframe(df)

# Sidebar filters
st.sidebar.header("Filters")

columns = df.columns.tolist()
x_col = st.sidebar.selectbox("X-axis", columns)
y_col = st.sidebar.selectbox("Y-axis", columns)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Histogram", "Scatter", "Boxplot", "Countplot"]
)

filtered_df = df.copy()

if df[x_col].dtype != "object":
    min_val = float(df[x_col].min())
    max_val = float(df[x_col].max())

    selected_range = st.sidebar.slider(
        f"{x_col} Range",
        min_val,
        max_val,
        (min_val, max_val)
    )

    filtered_df = df[
        (df[x_col] >= selected_range[0]) &
        (df[x_col] <= selected_range[1])
    ]
else:
    categories = df[x_col].unique().tolist()
    selected_cat = st.sidebar.multiselect(
        f"{x_col}",
        categories,
        default=categories
    )

    filtered_df = df[df[x_col].isin(selected_cat)]

# Charts
fig, ax = plt.subplots()

if chart_type == "Histogram":
    sns.histplot(filtered_df[x_col], kde=True, ax=ax)

elif chart_type == "Scatter":
    if filtered_df[y_col].dtype != "object":
        sns.scatterplot(x=filtered_df[x_col], y=filtered_df[y_col], ax=ax)

elif chart_type == "Boxplot":
    sns.boxplot(x=filtered_df[x_col], y=filtered_df[y_col], ax=ax)

elif chart_type == "Countplot":
    sns.countplot(x=filtered_df[x_col], ax=ax)

st.pyplot(fig)

# -------- BACK --------
st.markdown("---")

if st.button("⬅ Back to Prediction"):
    st.switch_page("predict_diabetes.py")