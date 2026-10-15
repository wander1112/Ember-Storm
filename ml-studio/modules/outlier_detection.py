"""
Outlier Detection Module
Interquartile Range (IQR) method, distribution comparison, and configurable treatment.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def compute_iqr_outliers(df, columns=None):
    """
    Compute IQR statistics and identify outlier counts across specified numerical columns.
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
    audit = []
    outlier_indices = set()
    
    for col in columns:
        series = df[col].dropna()
        if len(series) < 4:
            continue
            
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = float(q3 - q1)
        lower_bound = float(q1 - 1.5 * iqr)
        upper_bound = float(q3 + 1.5 * iqr)
        
        col_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
        outlier_indices.update(col_outliers)
        
        count = len(col_outliers)
        pct = (count / len(df)) * 100 if len(df) > 0 else 0
        
        audit.append({
            'Feature': col,
            'Q1 (25%)': round(q1, 3),
            'Q3 (75%)': round(q3, 3),
            'IQR': round(iqr, 3),
            'Lower Bound': round(lower_bound, 3),
            'Upper Bound': round(upper_bound, 3),
            'Outlier Count': count,
            'Outlier %': f"{pct:.2f}%"
        })
        
    return pd.DataFrame(audit), list(outlier_indices)

def treat_outliers(df, column, strategy='retain'):
    """
    Treat outliers in a specific column using 'retain', 'remove', or 'cap'.
    """
    df_treated = df.copy()
    series = df_treated[column].dropna()
    
    if len(series) < 4 or strategy == 'retain':
        return df_treated, "Outliers retained without modification."
        
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outlier_mask = (df_treated[column] < lower_bound) | (df_treated[column] > upper_bound)
    num_affected = int(outlier_mask.sum())
    
    if strategy == 'remove':
        df_treated = df_treated[~outlier_mask].reset_index(drop=True)
        msg = f"Successfully removed {num_affected} outlier rows from '{column}'."
    elif strategy == 'cap':
        df_treated[column] = np.clip(df_treated[column], lower_bound, upper_bound)
        msg = f"Successfully capped {num_affected} extreme values in '{column}' to [{lower_bound:.2f}, {upper_bound:.2f}]."
    else:
        msg = "No transformation applied."
        
    return df_treated, msg

def plot_outlier_comparison(df_orig, df_treated, col):
    """
    Compare original vs treated distributions side-by-side.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df_orig[col],
        name="Original",
        marker_color="#ef4444",
        boxpoints="outliers"
    ))
    
    fig.add_trace(go.Box(
        y=df_treated[col],
        name="Treated",
        marker_color="#10b981",
        boxpoints="outliers"
    ))
    
    fig.update_layout(
        title=f"Outlier Treatment Comparison: {col}",
        yaxis_title=col,
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig
