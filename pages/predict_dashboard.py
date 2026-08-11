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


# ============================================================
# TITLE
# ============================================================

st.title("🩺 Diabetes Intelligence Dashboard")
st.caption("AI-powered diabetes risk analysis and patient insights")

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
    # PATIENT KPI
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
    # PROBABILITY CHARTS
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

    st.error(
        "❌ diabetes_data.csv was not found."
    )

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
# SIDEBAR
# ============================================================

st.sidebar.title("🎛 Dashboard Controls")

st.sidebar.write(
    "Use the controls below to explore the dataset."
)


columns = df.columns.tolist()


x_col = st.sidebar.selectbox(
    "📌 Select X-axis",
    columns
)


y_col = st.sidebar.selectbox(
    "📌 Select Y-axis",
    columns
)


chart_type = st.sidebar.selectbox(
    "📊 Select Chart",
    [
        "Histogram",
        "Scatter",
        "Countplot"
    ]
)


# ============================================================
# FILTER
# ============================================================

filtered_df = df.copy()


if pd.api.types.is_numeric_dtype(
    df[x_col]
):

    min_val = float(
        df[x_col].min()
    )

    max_val = float(
        df[x_col].max()
    )


    selected_range = st.sidebar.slider(
        f"🔎 {x_col} Range",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )


    filtered_df = df[
        (df[x_col] >= selected_range[0])
        &
        (df[x_col] <= selected_range[1])
    ]


else:

    categories = (
        df[x_col]
        .dropna()
        .unique()
        .tolist()
    )


    selected_categories = st.sidebar.multiselect(
        f"🔎 Select {x_col}",
        categories,
        default=categories
    )


    filtered_df = df[
        df[x_col].isin(selected_categories)
    ]


# ============================================================
# FILTERED DATA
# ============================================================

st.subheader("📋 Filtered Patient Data")


st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=300
)


# ============================================================
# DOWNLOAD
# ============================================================

csv = filtered_df.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv,
    file_name="filtered_diabetes_data.csv",
    mime="text/csv"
)


# ============================================================
# POPULATION CHART
# ============================================================

st.subheader("📊 Population Data Analysis")


fig = None


# ------------------------------------------------------------
# HISTOGRAM
# ------------------------------------------------------------

if chart_type == "Histogram":

    fig = px.histogram(
        filtered_df,
        x=x_col,
        title=f"📊 Distribution of {x_col}",
        color_discrete_sequence=["royalblue"],
        height=450
    )


# ------------------------------------------------------------
# SCATTER
# ------------------------------------------------------------

elif chart_type == "Scatter":

    if (
        pd.api.types.is_numeric_dtype(
            filtered_df[x_col]
        )
        and
        pd.api.types.is_numeric_dtype(
            filtered_df[y_col]
        )
    ):

        fig = px.scatter(
            filtered_df,
            x=x_col,
            y=y_col,
            title=f"🔵 {x_col} vs {y_col}",
            color_discrete_sequence=["purple"],
            height=450
        )

    else:

        st.warning(
            "⚠️ Scatter plot requires numeric X and Y columns."
        )


# ------------------------------------------------------------
# COUNTPLOT
# ------------------------------------------------------------

elif chart_type == "Countplot":

    fig = px.histogram(
        filtered_df,
        x=x_col,
        color=x_col,
        title=f"📊 Count of {x_col}",
        height=450
    )


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

if fig is not None:

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# OUTCOME ANALYSIS
# ============================================================

if "Outcome" in df.columns:

    st.divider()

    st.subheader("🩸 Diabetes Distribution")


    outcome_fig = px.pie(
        df,
        names="Outcome",
        hole=0.5,
        title="Diabetes vs Non-Diabetes",
        color="Outcome",
        color_discrete_sequence=[
            "green",
            "red"
        ]
    )


    outcome_fig.update_traces(
        textinfo="percent+label"
    )


    st.plotly_chart(
        outcome_fig,
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