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

    # -------------------------------
    # KPI CARDS
    # -------------------------------

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
            f"{max(proba)*100:.1f}%"
        )

    st.subheader("🧾 Patient Details")

    st.dataframe(
        patient_df,
        use_container_width=True,
        height=150
    )

    # -------------------------------
    # PROBABILITY CHARTS
    # -------------------------------

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
            height=320
        )

        fig_bar.update_traces(
            texttemplate="%{y:.2%}",
            textposition="outside"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col2:
        fig_pie = px.pie(
            prob_df,
            names="Category",
            values="Probability",
            hole=0.55,
            title="Risk Distribution"
        )

        fig_pie.update_layout(height=320)

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

# ==================================================
# DATASET DASHBOARD
# ==================================================

st.header("🌍 Population-Level Insights")

df = pd.read_csv("diabetes_data.csv")

if "Gender" in df.columns:
    df["Gender"] = df["Gender"].map({
        0: "Male",
        1: "Female"
    })

# --------------------------------------------------
# DATASET SUMMARY
# --------------------------------------------------

st.subheader("📈 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Records", len(df))

with c2:
    st.metric("Features", len(df.columns))

with c3:
    if "Age" in df.columns:
        st.metric(
            "Average Age",
            round(df["Age"].mean(), 1)
        )

with c4:
    if "BMI" in df.columns:
        st.metric(
            "Average BMI",
            round(df["BMI"].mean(), 1)
        )

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("🎛 Filters")

columns = df.columns.tolist()

x_col = st.sidebar.selectbox(
    "Select X-axis",
    columns
)

y_col = st.sidebar.selectbox(
    "Select Y-axis",
    columns
)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    [
        "Histogram",
        "Scatter",
        "Countplot"
    ]
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
        f"{x_col} Categories",
        categories,
        default=categories
    )

    filtered_df = df[
        df[x_col].isin(selected_cat)
    ]

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
# DOWNLOAD BUTTON
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_diabetes_data.csv",
    mime="text/csv"
)

# --------------------------------------------------
# MAIN INTERACTIVE CHART
# --------------------------------------------------

st.subheader("📊 Patient Data Analysis")

if chart_type == "Histogram":

    fig = px.histogram(
        filtered_df,
        x=x_col,
        nbins=30,
        title=f"Distribution of {x_col}",
        height=400
    )

elif chart_type == "Scatter":

    fig = px.scatter(
        filtered_df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}",
        height=400,
        hover_data=filtered_df.columns
    )

elif chart_type == "Boxplot":

    fig = px.box(
        filtered_df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}",
        height=400
    )

else:

    fig = px.histogram(
        filtered_df,
        x=x_col,
        color=x_col,
        title=f"Count of {x_col}",
        height=400
    )

st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# OUTCOME ANALYSIS
# --------------------------------------------------

if "Outcome" in df.columns:

    st.subheader("📉 Diabetes Distribution")

    outcome_fig = px.pie(
        df,
        names="Outcome",
        title="Diabetes vs Non-Diabetes",
        hole=0.5
    )

    st.plotly_chart(
        outcome_fig,
        use_container_width=True
    )

# --------------------------------------------------
# BACK BUTTON
# --------------------------------------------------

st.markdown("---")

if st.button("⬅ Back to Prediction"):
    st.switch_page("pages/predict_diabetes.py")