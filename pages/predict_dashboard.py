import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Diabetes Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Diabetes Intelligence Dashboard")
st.caption("Patient-specific prediction and population-level diabetes analytics")


# =====================================================
# PATIENT-SPECIFIC DASHBOARD
# =====================================================

st.header("🧍 Patient-Specific Insights")

if "patient_data" not in st.session_state:

    st.warning(
        "⚠️ No patient selected. Please go back and predict first."
    )

else:

    patient_df = st.session_state["patient_data"]
    prediction = st.session_state["prediction"]
    proba = st.session_state["proba"]

    # -------------------------------------------------
    # KPI CARDS
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Prediction",
            "🔴 High Risk" if prediction == 1 else "🟢 Low Risk"
        )

    with col2:

        st.metric(
            "Diabetes Risk",
            f"{float(proba[1]) * 100:.1f}%"
        )

    with col3:

        st.metric(
            "Model Confidence",
            f"{max(proba) * 100:.1f}%"
        )

    # -------------------------------------------------
    # PATIENT DETAILS
    # -------------------------------------------------

    st.subheader("🧾 Patient Details")

    st.dataframe(
        patient_df,
        use_container_width=True
    )

    # -------------------------------------------------
    # PROBABILITY DATA
    # -------------------------------------------------

    prob_df = pd.DataFrame(
        {
            "Category": [
                "Not Diabetic",
                "Diabetic"
            ],
            "Probability": [
                float(proba[0]),
                float(proba[1])
            ]
        }
    )

    # -------------------------------------------------
    # PATIENT PROBABILITY CHARTS
    # -------------------------------------------------

    st.subheader("📊 Prediction Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig_bar = px.bar(
            prob_df,
            x="Category",
            y="Probability",
            text="Probability",
            title="Prediction Probability",
            color="Category",
            color_discrete_sequence=[
                "#2ECC71",
                "#FF4B4B"
            ]
        )

        fig_bar.update_traces(
            texttemplate="%{y:.2%}"
        )

        fig_bar.update_yaxes(
            tickformat=".0%"
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
            title="Risk Distribution",
            color_discrete_sequence=[
                "#2ECC71",
                "#FF4B4B"
            ]
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# =====================================================
# POPULATION LEVEL DASHBOARD
# =====================================================

st.markdown("---")

st.header("🌍 Population-Level Insights")
st.caption("Explore relationships and patterns across the complete diabetes dataset")


# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("diabetes_data.csv")


# =====================================================
# GENDER CONVERSION
# =====================================================

if "Gender" in df.columns:

    df["Gender"] = df["Gender"].map(
        {
            0: "Female",
            1: "Male"
        }
    )


# =====================================================
# DATASET OVERVIEW
# =====================================================

st.subheader("📈 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "👥 Records",
        len(df)
    )

with c2:

    st.metric(
        "📋 Features",
        len(df.columns)
    )

with c3:

    if "Age" in df.columns:

        st.metric(
            "🎂 Average Age",
            round(df["Age"].mean(), 1)
        )

with c4:

    if "BMI" in df.columns:

        st.metric(
            "⚖️ Average BMI",
            round(df["BMI"].mean(), 1)
        )


# =====================================================
# POPULATION ANALYSIS CONTROLS
# =====================================================

st.subheader("🎛 Population Data Analysis Controls")

st.sidebar.markdown("## 🎛 Population Analysis")

columns = df.columns.tolist()

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    exclude="number"
).columns.tolist()


# -----------------------------------------------------
# CHART TYPE
# -----------------------------------------------------

chart_type = st.sidebar.selectbox(
    "📊 Select Chart Type",
    [
        "Histogram",
        "Scatter Plot",
        "Bar Chart",
        "Count Plot",
        "Pie Chart"
    ]
)


# =====================================================
# HISTOGRAM
# =====================================================

if chart_type == "Histogram":

    x_col = st.sidebar.selectbox(
        "Select Feature",
        numeric_columns
    )

    bins = st.sidebar.slider(
        "Number of Bins",
        min_value=5,
        max_value=50,
        value=20
    )

    st.subheader(
        f"📊 Distribution of {x_col}"
    )

    fig = px.histogram(
        df,
        x=x_col,
        nbins=bins,
        title=f"Distribution of {x_col}",
        color_discrete_sequence=["#3498DB"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# SCATTER PLOT
# =====================================================

elif chart_type == "Scatter Plot":

    x_col = st.sidebar.selectbox(
        "Select X-axis",
        numeric_columns,
        key="scatter_x"
    )

    y_col = st.sidebar.selectbox(
        "Select Y-axis",
        numeric_columns,
        index=min(
            1,
            len(numeric_columns) - 1
        ),
        key="scatter_y"
    )

    color_option = st.sidebar.selectbox(
        "Compare / Color By",
        ["None"] + columns,
        key="scatter_color"
    )

    st.subheader(
        f"🔵 {x_col} vs {y_col}"
    )

    if color_option == "None":

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"{x_col} vs {y_col}",
            hover_data=columns
        )

    else:

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_option,
            title=f"{x_col} vs {y_col} by {color_option}",
            hover_data=columns
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# BAR CHART
# =====================================================

elif chart_type == "Bar Chart":

    category_col = st.sidebar.selectbox(
        "Select Category",
        columns,
        key="bar_category"
    )

    value_col = st.sidebar.selectbox(
        "Select Numeric Feature",
        numeric_columns,
        key="bar_value"
    )

    aggregation = st.sidebar.selectbox(
        "Select Aggregation",
        [
            "Average",
            "Sum",
            "Maximum",
            "Minimum"
        ]
    )

    # Group data

    if aggregation == "Average":

        bar_df = (
            df.groupby(category_col)[value_col]
            .mean()
            .reset_index()
        )

    elif aggregation == "Sum":

        bar_df = (
            df.groupby(category_col)[value_col]
            .sum()
            .reset_index()
        )

    elif aggregation == "Maximum":

        bar_df = (
            df.groupby(category_col)[value_col]
            .max()
            .reset_index()
        )

    else:

        bar_df = (
            df.groupby(category_col)[value_col]
            .min()
            .reset_index()
        )

    st.subheader(
        f"📊 {aggregation} {value_col} by {category_col}"
    )

    fig = px.bar(
        bar_df,
        x=category_col,
        y=value_col,
        text_auto=".2f",
        title=f"{aggregation} {value_col} by {category_col}",
        color=category_col
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# COUNT PLOT
# =====================================================

elif chart_type == "Count Plot":

    category_col = st.sidebar.selectbox(
        "Select Category",
        columns,
        key="count_category"
    )

    comparison_col = st.sidebar.selectbox(
        "Compare By",
        ["None"] + columns,
        key="count_compare"
    )

    st.subheader(
        f"📊 Count of {category_col}"
    )

    if comparison_col == "None":

        count_df = (
            df[category_col]
            .value_counts()
            .reset_index()
        )

        count_df.columns = [
            category_col,
            "Count"
        ]

        fig = px.bar(
            count_df,
            x=category_col,
            y="Count",
            text="Count",
            title=f"Count of {category_col}",
            color=category_col
        )

    else:

        count_df = (
            df.groupby(
                [category_col, comparison_col]
            )
            .size()
            .reset_index(
                name="Count"
            )
        )

        fig = px.bar(
            count_df,
            x=category_col,
            y="Count",
            color=comparison_col,
            barmode="group",
            text="Count",
            title=f"{category_col} compared by {comparison_col}"
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# PIE CHART
# =====================================================

elif chart_type == "Pie Chart":

    category_col = st.sidebar.selectbox(
        "Select Category",
        columns,
        key="pie_category"
    )

    pie_df = (
        df[category_col]
        .value_counts()
        .reset_index()
    )

    pie_df.columns = [
        category_col,
        "Count"
    ]

    st.subheader(
        f"🥧 Distribution of {category_col}"
    )

    fig = px.pie(
        pie_df,
        names=category_col,
        values="Count",
        hole=0.45,
        title=f"Distribution of {category_col}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# FILTERED DATASET
# =====================================================

st.markdown("---")

st.subheader("📋 Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=300
)


# =====================================================
# DOWNLOAD DATA
# =====================================================

csv = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Diabetes Dataset",
    data=csv,
    file_name="diabetes_data.csv",
    mime="text/csv"
)


# =====================================================
# DIABETES OUTCOME ANALYSIS
# =====================================================

if "Outcome" in df.columns:

    st.markdown("---")

    st.subheader("📉 Diabetes Outcome Distribution")

    outcome_df = (
        df["Outcome"]
        .value_counts()
        .reset_index()
    )

    outcome_df.columns = [
        "Outcome",
        "Count"
    ]

    outcome_df["Outcome"] = outcome_df[
        "Outcome"
    ].map(
        {
            0: "Not Diabetic",
            1: "Diabetic"
        }
    )

    fig_outcome = px.pie(
        outcome_df,
        names="Outcome",
        values="Count",
        hole=0.5,
        title="Diabetic vs Non-Diabetic Patients",
        color_discrete_sequence=[
            "#2ECC71",
            "#E74C3C"
        ]
    )

    st.plotly_chart(
        fig_outcome,
        use_container_width=True
    )


# =====================================================
# BACK BUTTON
# =====================================================

st.markdown("---")

if st.button("⬅️ Back to Prediction"):

    st.switch_page(
        "pages/predict_diabetes.py"
    )