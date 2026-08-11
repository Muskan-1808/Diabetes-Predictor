```python
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f5f9ff 0%,
            #eef7f5 50%,
            #fdf5fa 100%
        );
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #17324D;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #607D8B;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* Section headings */
    .section-title {
        background: linear-gradient(
            90deg,
            #2563EB,
            #7C3AED
        );
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #2563EB;
        text-align: center;
    }

    .kpi-title {
        color: #607D8B;
        font-size: 15px;
        font-weight: 600;
    }

    .kpi-value {
        color: #17324D;
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* Patient information box */
    .patient-box {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #78909C;
        padding: 20px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🩺 Diabetes Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered patient risk analysis and population insights</div>',
    unsafe_allow_html=True
)


# ============================================================
# PATIENT-SPECIFIC DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">🧍 Patient-Specific Insights</div>',
    unsafe_allow_html=True
)


if "patient_data" not in st.session_state:

    st.warning(
        "⚠️ No patient selected. Please go back to the prediction page and test a patient first."
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

        prediction_text = (
            "🔴 High Risk"
            if prediction == 1
            else "🟢 Low Risk"
        )

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Prediction</div>
                <div class="kpi-value">{prediction_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Diabetes Risk</div>
                <div class="kpi-value">
                    {proba[1] * 100:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Model Confidence</div>
                <div class="kpi-value">
                    {max(proba) * 100:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # --------------------------------------------------------
    # PATIENT DETAILS
    # --------------------------------------------------------

    st.subheader("🧾 Patient Details")

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

    st.subheader("📊 Prediction Analysis")

    col1, col2 = st.columns(2)


    # BAR CHART
    with col1:

        fig_bar = px.bar(
            prob_df,
            x="Category",
            y="Probability",
            text="Probability",
            title="🧠 Prediction Probability",
            color="Category",
            color_discrete_map={
                "Not Diabetic": "#2ECC71",
                "Diabetic": "#E74C3C"
            },
            height=350
        )

        fig_bar.update_traces(
            texttemplate="%{y:.1%}",
            textposition="outside"
        )

        fig_bar.update_layout(
            yaxis=dict(
                tickformat=".0%"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#17324D"
            )
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


    # PIE CHART
    with col2:

        fig_pie = px.pie(
            prob_df,
            names="Category",
            values="Probability",
            hole=0.55,
            title="🎯 Risk Distribution",
            color="Category",
            color_discrete_map={
                "Not Diabetic": "#2ECC71",
                "Diabetic": "#E74C3C"
            }
        )

        fig_pie.update_traces(
            textinfo="percent+label"
        )

        fig_pie.update_layout(
            paper_bgcolor="white",
            font=dict(
                color="#17324D"
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# ============================================================
# POPULATION-LEVEL DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Population-Level Insights</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

try:

    df = pd.read_csv("diabetes_data.csv")

except FileNotFoundError:

    st.error(
        "❌ diabetes_data.csv was not found."
    )

    st.stop()


# ------------------------------------------------------------
# GENDER CONVERSION
# ------------------------------------------------------------

if "Gender" in df.columns:

    df["Gender"] = df["Gender"].map(
        {
            0: "Male",
            1: "Female"
        }
    )


# ============================================================
# DATASET SUMMARY
# ============================================================

st.subheader("📈 Dataset Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Total Records</div>
            <div class="kpi-value">{len(df):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📋 Features</div>
            <div class="kpi-value">{len(df.columns)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    if "Age" in df.columns:

        avg_age = df["Age"].mean()

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">🎂 Average Age</div>
                <div class="kpi-value">{avg_age:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


with c4:

    if "BMI" in df.columns:

        avg_bmi = df["BMI"].mean()

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">⚖️ Average BMI</div>
                <div class="kpi-value">{avg_bmi:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    "## 🎛 Dashboard Controls"
)

st.sidebar.info(
    "Use these controls to explore the diabetes dataset."
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


# BOX PLOT REMOVED
chart_type = st.sidebar.selectbox(
    "📊 Chart Type",
    [
        "Histogram",
        "Scatter",
        "Countplot"
    ]
)


# ============================================================
# FILTER DATA
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


    selected_cat = st.sidebar.multiselect(
        f"🔎 {x_col} Categories",
        categories,
        default=categories
    )


    filtered_df = df[
        df[x_col].isin(selected_cat)
    ]


# ============================================================
# FILTERED DATA
# ============================================================

st.subheader("📋 Filtered Patient Dataset")


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
# DATA VISUALIZATION
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
        height=450,
        title=f"📊 Distribution of {x_col}",
        color_discrete_sequence=["#6366F1"]
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
            height=450,
            title=f"🔵 {x_col} vs {y_col}",
            color_discrete_sequence=["#8E44AD"],
            opacity=0.75
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
        height=450,
        title=f"📊 Count of {x_col}",
        color_discrete_sequence=[
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#DDA0DD"
        ]
    )


# ------------------------------------------------------------
# DISPLAY CHART
# ------------------------------------------------------------

if fig is not None:

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            color="#17324D"
        ),
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# OUTCOME ANALYSIS
# ============================================================

if "Outcome" in df.columns:

    st.subheader("📉 Diabetes Distribution")


    outcome_fig = px.pie(
        df,
        names="Outcome",
        hole=0.55,
        title="🩸 Diabetes vs Non-Diabetes",
        color="Outcome",
        color_discrete_sequence=[
            "#2ECC71",
            "#E74C3C"
        ]
    )


    outcome_fig.update_traces(
        textinfo="percent+label"
    )


    outcome_fig.update_layout(
        paper_bgcolor="white",
        font=dict(
            color="#17324D"
        )
    )


    st.plotly_chart(
        outcome_fig,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🩺 Diabetes Intelligence Dashboard
        <br>
        AI-powered analysis for healthcare insights
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BACK BUTTON
# ============================================================

st.markdown("---")


if st.button(
    "⬅️ Back to Prediction",
    use_container_width=True
):

    st.switch_page(
        "login.py"
    )
```
