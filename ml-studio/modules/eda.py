"""
Exploratory Data Analysis (EDA) Module
Interactive Plotly charts, statistical moments, and automated data-derived insights.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

def compute_statistics_table(df):
    """
    Compute extended descriptive statistics for all numerical columns.
    """
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return pd.DataFrame()
    
    stats_list = []
    for col in num_df.columns:
        series = num_df[col].dropna()
        if len(series) == 0:
            continue
        
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        
        # Calculate moments
        mean_val = series.mean()
        std_val = series.std()
        skew_val = series.skew()
        kurt_val = series.kurtosis()
        
        stats_list.append({
            'Feature': col,
            'Count': int(series.count()),
            'Mean': round(mean_val, 3),
            'Std Dev': round(std_val, 3),
            'Min': round(series.min(), 3),
            'Q1 (25%)': round(q1, 3),
            'Median (50%)': round(series.median(), 3),
            'Q3 (75%)': round(q3, 3),
            'Max': round(series.max(), 3),
            'IQR': round(iqr, 3),
            'Skewness': round(skew_val, 3),
            'Kurtosis': round(kurt_val, 3)
        })
    return pd.DataFrame(stats_list)

def plot_histogram(df, col, bins=30):
    """
    Plot interactive distribution histogram with mean/median indicator.
    """
    series = df[col].dropna()
    mean_val = series.mean()
    median_val = series.median()
    skew_val = series.skew()
    
    fig = px.histogram(
        df, x=col, nbins=bins, marginal="box",
        title=f"Distribution of {col}",
        color_discrete_sequence=['#2563eb'],
        opacity=0.8
    )
    
    fig.add_vline(x=mean_val, line_dash="dash", line_color="#ef4444", annotation_text=f"Mean: {mean_val:.2f}")
    fig.add_vline(x=median_val, line_dash="dot", line_color="#10b981", annotation_text=f"Median: {median_val:.2f}")
    
    fig.update_layout(
        template="plotly_white",
        xaxis_title=col,
        yaxis_title="Frequency",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    # Data-derived observation
    skew_desc = "symmetrical" if abs(skew_val) < 0.5 else ("right-skewed" if skew_val > 0 else "left-skewed")
    observation = f"**Data Insight:** `{col}` has a mean of {mean_val:.2f} and a median of {median_val:.2f}. The distribution is **{skew_desc}** (skewness = {skew_val:.2f})."
    
    return fig, observation

def plot_boxplot(df, col, group_by=None):
    """
    Plot interactive box plot with optional categorical grouping.
    """
    fig = px.box(
        df, y=col, x=group_by, points="outliers",
        color=group_by if group_by else None,
        title=f"Outlier & Spread Analysis: {col}" + (f" by {group_by}" if group_by else ""),
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=50, b=40))
    
    series = df[col].dropna()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    outlier_count = ((series < (q1 - 1.5*iqr)) | (series > (q3 + 1.5*iqr))).sum()
    
    observation = f"**Data Insight:** The interquartile range (IQR) for `{col}` spans from {q1:.2f} to {q3:.2f} (IQR = {iqr:.2f}). There are **{outlier_count} statistical outlier points** beyond the 1.5 × IQR whiskers."
    return fig, observation

def plot_scatter(df, x_col, y_col, color_col=None):
    """
    Interactive 2D scatter plot with trendline.
    """
    valid_df = df[[x_col, y_col] + ([color_col] if color_col else [])].dropna()
    
    corr = valid_df[x_col].corr(valid_df[y_col]) if pd.api.types.is_numeric_dtype(valid_df[x_col]) and pd.api.types.is_numeric_dtype(valid_df[y_col]) else 0
    
    fig = px.scatter(
        valid_df, x=x_col, y=y_col, color=color_col,
        trendline="ols" if not color_col and len(valid_df) > 2 else None,
        title=f"Feature Interaction: {y_col} vs. {x_col}",
        color_discrete_sequence=px.colors.qualitative.Safe,
        opacity=0.75
    )
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=40, t=50, b=40))
    
    strength = "strong" if abs(corr) > 0.6 else ("moderate" if abs(corr) > 0.3 else "weak")
    direction = "positive" if corr > 0 else "negative"
    observation = f"**Data Insight:** Pearson correlation between `{x_col}` and `{y_col}` is **r = {corr:.3f}**, indicating a **{strength} {direction} linear relationship**."
    return fig, observation

def plot_correlation_heatmap(df):
    """
    Plot interactive correlation matrix heatmap for numerical variables.
    """
    num_df = df.select_dtypes(include=[np.number])
    if num_df.shape[1] < 2:
        return None, "Not enough numerical columns to compute a correlation heatmap."
    
    corr = num_df.corr().round(3)
    
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Interactive Correlation Matrix (Pearson r)"
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_tickangle=-45
    )
    
    # Find strongest correlation pair (excluding diagonals)
    corr_unstack = corr.unstack()
    corr_unstack = corr_unstack[corr_unstack < 0.9999].abs().sort_values(ascending=False)
    if not corr_unstack.empty:
        top_pair = corr_unstack.index[0]
        top_val = corr.loc[top_pair[0], top_pair[1]]
        observation = f"**Data Insight:** The strongest correlation observed is between `{top_pair[0]}` and `{top_pair[1]}` (r = {top_val:.3f})."
    else:
        observation = "**Data Insight:** Correlation matrix computed across all numerical columns."
        
    return fig, observation

def plot_categorical_distribution(df, col):
    """
    Bar chart for categorical frequency distribution.
    """
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, 'Count']
    
    fig = px.bar(
        counts, x=col, y='Count',
        title=f"Category Distribution: {col}",
        color=col,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text='Count'
    )
    fig.update_layout(template="plotly_white", showlegend=False, margin=dict(l=40, r=40, t=50, b=40))
    
    top_cat = counts.iloc[0][col]
    top_cnt = counts.iloc[0]['Count']
    pct = (top_cnt / len(df)) * 100
    observation = f"**Data Insight:** The majority category in `{col}` is **'{top_cat}'** with {top_cnt} occurrences ({pct:.1f}% of total samples)."
    return fig, observation
