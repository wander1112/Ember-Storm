"""
Evaluation & Comparison Module
Multi-track benchmark tables, interactive ranking charts, and best-model selector.
"""

import pandas as pd
import numpy as np
import plotly.express as px

def get_best_model_info(track_type, benchmark_df):
    """
    Select best model based on actual calculated metrics.
    """
    if benchmark_df is None or benchmark_df.empty:
        return None, "No models evaluated yet."
        
    if track_type == 'Regression':
        # Sort by R2 Score
        best_row = benchmark_df.sort_values(by='R2 Score', ascending=False).iloc[0]
        model_name = best_row['Model']
        r2 = best_row['R2 Score']
        rmse = best_row['RMSE']
        explanation = f"**{model_name}** achieved the highest test performance with an **R² score of {r2:.4f}** and the lowest prediction error (**RMSE = {rmse:.4f}**)."
        metrics = {'R² Score': r2, 'RMSE': rmse, 'MAE': best_row['MAE']}
        
    elif track_type == 'Classification':
        # Sort by Accuracy or F1-Score
        best_row = benchmark_df.sort_values(by='Accuracy', ascending=False).iloc[0]
        model_name = best_row['Algorithm']
        acc = best_row['Accuracy']
        f1 = best_row['F1-Score']
        explanation = f"**{model_name}** is the top-performing classifier, achieving **{acc*100:.2f}% accuracy** and a weighted **F1-Score of {f1:.4f}**."
        metrics = {'Accuracy': f"{acc*100:.2f}%", 'F1-Score': f1, 'Precision': best_row['Precision'], 'Recall': best_row['Recall']}
        
    else:  # Clustering
        best_row = benchmark_df.sort_values(by='Silhouette Score', ascending=False).iloc[0]
        model_name = f"{best_row['Algorithm']} ({best_row['Linkage / Criterion']})"
        sil = best_row['Silhouette Score']
        db = best_row['Davies-Bouldin Index']
        explanation = f"**{model_name}** demonstrated the highest cluster cohesion and separation with a **Silhouette Score of {sil:.4f}** and a **Davies-Bouldin Index of {db:.4f}**."
        metrics = {'Silhouette': sil, 'Davies-Bouldin': db, 'Calinski-Harabasz': best_row['Calinski-Harabasz Index']}
        
    return {
        'name': model_name,
        'metrics': metrics,
        'explanation': explanation
    }

def plot_benchmark_bar(df, metric_col, model_col, title="Model Performance Benchmark", higher_is_better=True):
    """
    Create a clean horizontal bar chart ranking all models.
    """
    sorted_df = df.sort_values(by=metric_col, ascending=higher_is_better)
    
    fig = px.bar(
        sorted_df, x=metric_col, y=model_col, orientation='h',
        title=title,
        color=metric_col,
        color_continuous_scale="Blues" if higher_is_better else "Reds_r",
        text=metric_col
    )
    fig.update_layout(
        template="plotly_white",
        yaxis_title="",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig
