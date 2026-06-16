# ==================================================
# ADD AFTER IMPORTS
# ==================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SEQ = px.colors.qualitative.Dark24

# ==================================================
# PROBABILITY BAR CHART
# ==================================================

fig_bar = px.bar(
    prob_df,
    x="Category",
    y="Probability",
    color="Category",
    color_discrete_sequence=COLOR_SEQ,
    text="Probability",
    title="Prediction Probability",
    height=320
)

fig_bar.update_traces(
    texttemplate="%{y:.2%}",
    textposition="outside"
)

# ==================================================
# RISK DISTRIBUTION PIE CHART
# ==================================================

fig_pie = px.pie(
    prob_df,
    names="Category",
    values="Probability",
    hole=0.55,
    color="Category",
    color_discrete_sequence=COLOR_SEQ,
    title="Risk Distribution"
)

# ==================================================
# HISTOGRAM
# ==================================================

if chart_type == "Histogram":

    fig = px.histogram(
        filtered_df,
        x=x_col,
        color=x_col,
        color_discrete_sequence=COLOR_SEQ,
        nbins=30,
        title=f"Distribution of {x_col}",
        height=400
    )

# ==================================================
# SCATTER PLOT
# ==================================================

elif chart_type == "Scatter":

    fig = px.scatter(
        filtered_df,
        x=x_col,
        y=y_col,
        color=y_col,
        color_continuous_scale="Turbo",
        title=f"{x_col} vs {y_col}",
        height=400,
        hover_data=filtered_df.columns
    )

# ==================================================
# BOXPLOT
# ==================================================

elif chart_type == "Boxplot":

    fig = px.box(
        filtered_df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_sequence=COLOR_SEQ,
        title=f"{x_col} vs {y_col}",
        height=400
    )

# ==================================================
# COUNTPLOT
# ==================================================

else:

    fig = px.histogram(
        filtered_df,
        x=x_col,
        color=x_col,
        color_discrete_sequence=COLOR_SEQ,
        title=f"Count of {x_col}",
        height=400
    )

# ==================================================
# OUTCOME PIE CHART
# ==================================================

outcome_fig = px.pie(
    df,
    names="Outcome",
    title="Diabetes vs Non-Diabetes",
    hole=0.5,
    color="Outcome",
    color_discrete_sequence=COLOR_SEQ
)