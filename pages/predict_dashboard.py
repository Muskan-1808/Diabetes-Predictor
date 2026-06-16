import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Diabetes Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Diabetes Intelligence Dashboard")


# ==================================================
# PATIENT DASHBOARD
# ==================================================
st.header("🧍 Patient-Specific Insights")

if "patient_data" not in st.session_state:
    st.warning("⚠️ No patient selected. Please go back and predict first.")

else:
    patient_df = st.session_state["patient_data"]
    prediction = st.session_state["prediction"]
    proba = st.session_state["proba"]

    # KPI CARDS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Prediction",
            "High Risk" if prediction == 1 else "Low Risk"
        )

    with col2:
        st.metric(
            "Diabetes Risk",
            f"{proba[1]*100:.1f}%"
        )
    with col3:
        st.metric(
            "Model Confidence",
            f"{max(proba[1])*100:.1f}%"
        )

    st.subheader("🧾 Patient Details")
    st.dataframe(patient_df, use_container_width=True, height=150)

    # PROBABILITY CHART
    prob_df = pd.DataFrame({
        "Category": ["Not Diabetic", "Diabetic"],
        "Probability": proba
    })

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            prob_df,
            x="Category",
            y="Probability",
            text="Probability",
            title="Prediction Probability",
            height=320,
            marker_color=["#FF4B4B","#00CC96"]
        )
        fig_bar.update_traces(texttemplate="%{y:.2%}")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            prob_df,
            names="Category",
            values="Probability",
            hole=0.55,
            title="Risk Distribution"
            marker=dict(
                colors=["#2ECC71","#F1C40F"]
        )
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ==================================================
# DATASET DASHBOARD
# ==================================================
st.header("🌍 Population-Level Insights")

df = pd.read_csv("diabetes_data.csv")

if "Gender" in df.columns:
    df["Gender"] = df["Gender"].map({0: "Male", 1: "Female"})


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
st.subheader("📈 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Records", len(df))

with c2:
    st.metric("Features", len(df.columns))

with c3:
    if "Age" in df.columns:
        st.metric("Average Age", round(df["Age"].mean(), 1))

with c4:
    if "BMI" in df.columns:
        st.metric("Average BMI", round(df["BMI"].mean(), 1))


# --------------------------------------------------
# SIDEBAR FILTERS (FIXED LOGIC)
# --------------------------------------------------
st.sidebar.header("🎛 Filters")

columns = df.columns.tolist()

x_col = st.sidebar.selectbox("Select X-axis", columns)
y_col = st.sidebar.selectbox("Select Y-axis", columns)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Histogram", "Scatter", "Boxplot", "Countplot"]
)

filtered_df = df.copy()

# ----------------------------
# SAFE FILTERING LOGIC
# ----------------------------
if pd.api.types.is_numeric_dtype(df[x_col]):

    min_val = float(df[x_col].min())
    max_val = float(df[x_col].max())

    selected_range = st.sidebar.slider(
        x_col,
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )

    filtered_df = df[
        (df[x_col] >= selected_range[0]) &
        (df[x_col] <= selected_range[1])
    ]

else:
    selected_cat = st.sidebar.multiselect(
        f"{x_col} Categories",
        df[x_col].dropna().unique(),
        default=df[x_col].dropna().unique()
    )

    filtered_df = df[df[x_col].isin(selected_cat)]


# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)


# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_diabetes_data.csv",
    mime="text/csv"
)


# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.subheader("📊 Patient Data Analysis")

if chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=x_col, nbins=30, height=400,color_continuous_scale="Viridis")

elif chart_type == "Scatter":
    fig = px.scatter(filtered_df, x=x_col, y=y_col, height=400,color_continuous_scale="Rainbow")

elif chart_type == "Boxplot":
    fig = px.box(filtered_df, x=x_col, y=y_col, height=400,color_discrete_sequence=px.colors.qualitative.Set3)

else:
    fig = px.histogram(filtered_df, x=x_col, color=x_col, height=400,color_discrete_sequence=["#FF6B6B"])

st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# OUTCOME ANALYSIS
# --------------------------------------------------
if "Outcome" in df.columns:

    st.subheader("📉 Diabetes Distribution")

    outcome_fig = px.pie(
        df,
        names="Outcome",
        hole=0.5,
        title="Diabetes vs Non-Diabetes"
    )

    st.plotly_chart(outcome_fig, use_container_width=True,color_discrete_sequence=["#4ECDC4","#FFA15A"])


# --------------------------------------------------
# BACK BUTTON
# --------------------------------------------------
st.markdown("---")

if st.button("⬅ Back to Prediction"):
    st.switch_page("pages/predict_diabetes.py")