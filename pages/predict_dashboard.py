import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Diabetes Intelligence Dashboard",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Diabetes Intelligence Dashboard")
st.caption("AI-powered diabetes risk analysis and population insights")

st.divider()


# ============================================================
# PATIENT-SPECIFIC DASHBOARD
# ============================================================

st.header("🧍 Patient-Specific Insights")

if "patient_data" not in st.session_state:

    st.warning(
        "⚠️ No patient selected. Please go back to the prediction page and predict first."
    )

else:

    patient_df = st.session_state["patient_data"]
    prediction = st.session_state["prediction"]
    proba = st.session_state["proba"]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        if prediction == 1:
            st.error("🔴 High Risk")
        else:
            st.success("🟢 Low Risk")

        st.metric(
            "Prediction",
            "Diabetic" if prediction == 1 else "Not Diabetic"
        )

    with col2:

        st.metric(
            "Diabetes Probability",
            f"{proba[1] * 100:.1f}%"
        )

    with col3:

        st.metric(
            "Model Confidence",
            f"{max(proba) * 100:.1f}%"
        )

    # --------------------------------------------------------
    # PATIENT DETAILS
    # --------------------------------------------------------

    st.subheader("🧾 Patient Input Details")

    st.dataframe(
        patient_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # PROBABILITY DATA
    # --------------------------------------------------------

    prob_df = pd.DataFrame(
        {
            "Category": [
                "Not Diabetic",
                "Diabetic"
            ],
            "Probability": proba
        }
    )

    # --------------------------------------------------------
    # PATIENT PROBABILITY CHARTS
    # --------------------------------------------------------

    st.subheader("📊 Patient Prediction Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig_bar = px.bar(
            prob_df,
            x="Category",
            y="Probability",
            text="Probability",
            title="Prediction Probability",
            color="Category",
            color_discrete_map={
                "Not Diabetic": "green",
                "Diabetic": "red"
            }
        )

        fig_bar.update_traces(
            texttemplate="%{y:.1%}",
            textposition="outside"
        )

        fig_bar.update_layout(
            yaxis_tickformat=".0%",
            height=400
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
            hole=0.5,
            title="Risk Distribution",
            color="Category",
            color_discrete_map={
                "Not Diabetic": "green",
                "Diabetic": "red"
            }
        )

        fig_pie.update_traces(
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# ============================================================
# POPULATION DASHBOARD
# ============================================================

st.divider()

st.header("🌍 Population-Level Insights")


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = pd.read_csv("diabetes_data.csv")

except FileNotFoundError:

    st.error("❌ diabetes_data.csv was not found.")
    st.stop()


# ============================================================
# GENDER CONVERSION
# ============================================================

if "Gender" in df.columns:

    df["Gender"] = df["Gender"].map(
        {
            0: "Male",
            1: "Female"
        }
    )


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader("📈 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "👥 Total Patients",
        f"{len(df):,}"
    )

with c2:

    st.metric(
        "📋 Total Features",
        len(df.columns)
    )

with c3:

    if "Age" in df.columns:

        st.metric(
            "🎂 Average Age",
            f"{df['Age'].mean():.1f}"
        )

    else:

        st.metric(
            "🎂 Average Age",
            "N/A"
        )

with c4:

    if "BMI" in df.columns:

        st.metric(
            "⚖️ Average BMI",
            f"{df['BMI'].mean():.1f}"
        )

    else:

        st.metric(
            "⚖️ Average BMI",
            "N/A"
        )


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.title("🎛 Dashboard Controls")

st.sidebar.write(
    "Select the variables you want to compare."
)


columns = df.columns.tolist()


# ------------------------------------------------------------
# CHART TYPE
# ------------------------------------------------------------

chart_type = st.sidebar.selectbox(
    "📊 Select Analysis Type",
    [
        "Feature vs Outcome",
        "Feature vs Feature",
        "Feature Distribution",
        "Category Comparison"
    ]
)


# ============================================================
# FEATURE VS OUTCOME
# ============================================================

if chart_type == "Feature vs Outcome":

    st.sidebar.subheader("🎯 Outcome Comparison")

    feature_columns = [
        col for col in columns
        if col != "Outcome"
    ]

    selected_feature = st.sidebar.selectbox(
        "Select Feature",
        feature_columns
    )

    st.subheader(
        f"📊 {selected_feature} vs Diabetes Outcome"
    )

    if "Outcome" in df.columns:

        # Numeric feature
        if pd.api.types.is_numeric_dtype(
            df[selected_feature]
        ):

            fig = px.box(
                df,
                x="Outcome",
                y=selected_feature,
                color="Outcome",
                title=f"{selected_feature} by Diabetes Outcome",
                color_discrete_sequence=[
                    "green",
                    "red"
                ]
            )

        # Categorical feature
        else:

            comparison_df = (
                df.groupby(
                    [selected_feature, "Outcome"]
                )
                .size()
                .reset_index(name="Patients")
            )

            fig = px.bar(
                comparison_df,
                x=selected_feature,
                y="Patients",
                color="Outcome",
                barmode="group",
                title=f"{selected_feature} vs Diabetes Outcome",
                color_discrete_sequence=[
                    "green",
                    "red"
                ]
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# FEATURE VS FEATURE
# ============================================================

elif chart_type == "Feature vs Feature":

    st.sidebar.subheader("🔗 Feature Comparison")

    x_col = st.sidebar.selectbox(
        "Select X-axis Feature",
        columns
    )

    y_col = st.sidebar.selectbox(
        "Select Y-axis Feature",
        columns
    )

    st.subheader(
        f"📊 {x_col} vs {y_col}"
    )

    x_numeric = pd.api.types.is_numeric_dtype(
        df[x_col]
    )

    y_numeric = pd.api.types.is_numeric_dtype(
        df[y_col]
    )

    # Both numeric
    if x_numeric and y_numeric:

        color_column = None

        if "Outcome" in df.columns:

            color_column = "Outcome"

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_column,
            title=f"{x_col} vs {y_col}",
            height=500
        )

    # Numeric X + categorical Y
    elif x_numeric and not y_numeric:

        fig = px.box(
            df,
            x=y_col,
            y=x_col,
            color=y_col,
            title=f"{x_col} by {y_col}",
            height=500
        )

    # Categorical X + numeric Y
    elif not x_numeric and y_numeric:

        fig = px.box(
            df,
            x=x_col,
            y=y_col,
            color=x_col,
            title=f"{y_col} by {x_col}",
            height=500
        )

    # Both categorical
    else:

        comparison_df = (
            df.groupby(
                [x_col, y_col]
            )
            .size()
            .reset_index(name="Patients")
        )

        fig = px.bar(
            comparison_df,
            x=x_col,
            y="Patients",
            color=y_col,
            barmode="group",
            title=f"{x_col} vs {y_col}",
            height=500
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FEATURE DISTRIBUTION
# ============================================================

elif chart_type == "Feature Distribution":

    st.sidebar.subheader("📈 Distribution")

    selected_feature = st.sidebar.selectbox(
        "Select Feature",
        columns
    )

    st.subheader(
        f"📊 Distribution of {selected_feature}"
    )

    if pd.api.types.is_numeric_dtype(
        df[selected_feature]
    ):

        fig = px.histogram(
            df,
            x=selected_feature,
            color="Outcome"
            if "Outcome" in df.columns
            else None,
            nbins=30,
            barmode="overlay",
            title=f"Distribution of {selected_feature}",
            height=500
        )

    else:

        count_df = (
            df[selected_feature]
            .value_counts()
            .reset_index()
        )

        count_df.columns = [
            selected_feature,
            "Patients"
        ]

        fig = px.bar(
            count_df,
            x=selected_feature,
            y="Patients",
            color=selected_feature,
            title=f"Distribution of {selected_feature}",
            height=500
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CATEGORY COMPARISON
# ============================================================

else:

    st.sidebar.subheader("📊 Category Analysis")

    category_column = st.sidebar.selectbox(
        "Select Category",
        [
            col for col in columns
            if not pd.api.types.is_numeric_dtype(
                df[col]
            )
        ]
    )

    value_column = st.sidebar.selectbox(
        "Select Numeric Feature",
        [
            col for col in columns
            if pd.api.types.is_numeric_dtype(
                df[col]
            )
        ]
    )

    st.subheader(
        f"📊 Average {value_column} by {category_column}"
    )

    comparison_df = (
        df.groupby(category_column)[value_column]
        .mean()
        .reset_index()
    )

    comparison_df.columns = [
        category_column,
        f"Average {value_column}"
    ]

    fig = px.bar(
        comparison_df,
        x=category_column,
        y=f"Average {value_column}",
        color=category_column,
        title=f"Average {value_column} by {category_column}",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FILTERED DATA
# ============================================================

st.divider()

st.subheader("📋 Population Dataset")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=300
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

csv = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name="diabetes_data.csv",
    mime="text/csv"
)


# ============================================================
# DIABETES OUTCOME ANALYSIS
# ============================================================

if "Outcome" in df.columns:

    st.divider()

    st.subheader("🩸 Diabetes Distribution")

    outcome_counts = (
        df["Outcome"]
        .value_counts()
        .reset_index()
    )

    outcome_counts.columns = [
        "Outcome",
        "Patients"
    ]

    outcome_counts["Outcome"] = (
        outcome_counts["Outcome"]
        .map({
            0: "Not Diabetic",
            1: "Diabetic"
        })
        .fillna(
            outcome_counts["Outcome"]
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        outcome_fig = px.pie(
            outcome_counts,
            names="Outcome",
            values="Patients",
            hole=0.5,
            title="Diabetes vs Non-Diabetes",
            color="Outcome",
            color_discrete_map={
                "Not Diabetic": "green",
                "Diabetic": "red"
            }
        )

        outcome_fig.update_traces(
            textinfo="percent+label"
        )

        st.plotly_chart(
            outcome_fig,
            use_container_width=True
        )

    with col2:

        outcome_bar = px.bar(
            outcome_counts,
            x="Outcome",
            y="Patients",
            color="Outcome",
            title="Number of Diabetic vs Non-Diabetic Patients",
            color_discrete_map={
                "Not Diabetic": "green",
                "Diabetic": "red"
            }
        )

        st.plotly_chart(
            outcome_bar,
            use_container_width=True
        )


# ============================================================
# BACK BUTTON
# ============================================================

st.divider()

if st.button(
    "⬅️ Back to Prediction",
    use_container_width=True
):

    st.switch_page(
        "login.py"
    )