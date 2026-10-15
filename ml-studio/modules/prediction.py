"""
Live Prediction Module
Dynamic input form generation, real-time model inference, probability breakdowns, and history tracking.
"""

import pandas as pd
import numpy as np
import plotly.express as px

def make_prediction(model, input_dict, feature_names, preprocessor=None, track_type='Regression'):
    """
    Run genuine prediction through the trained estimator.
    """
    input_df = pd.DataFrame([input_dict])
    
    # Ensure all required features are present and correctly ordered
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_names]
    
    # Preprocess if transformer exists
    if preprocessor is not None:
        try:
            X_input = preprocessor.transform(input_df)
        except Exception:
            X_input = input_df.values
    else:
        X_input = input_df.values
        
    result = {}
    
    if track_type == 'Regression':
        pred_val = float(model.predict(X_input)[0])
        result['prediction'] = round(pred_val, 3)
        result['probabilities'] = None
        result['explanation'] = f"The model predicts an estimated value of **{pred_val:.3f}**."
        
    elif track_type == 'Classification':
        pred_class = model.predict(X_input)[0]
        result['prediction'] = pred_class
        
        # Probabilities
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X_input)[0]
            classes = getattr(model, 'classes_', [f"Class {i}" for i in range(len(probs))])
            result['probabilities'] = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
            max_prob = max(probs) * 100
            result['explanation'] = f"The model classifies this instance as **'{pred_class}'** with **{max_prob:.1f}% confidence**."
        else:
            result['probabilities'] = None
            result['explanation'] = f"The model predicts class **'{pred_class}'**."
            
    else:  # Clustering
        if hasattr(model, 'predict'):
            cluster_id = int(model.predict(X_input)[0])
            result['prediction'] = f"Cluster {cluster_id}"
            result['probabilities'] = None
            result['explanation'] = f"Based on feature centroid distances, this observation belongs to **Cluster {cluster_id}**."
        else:
            result['prediction'] = "N/A"
            result['probabilities'] = None
            result['explanation'] = "Agglomerative Hierarchical Clustering builds a linkage tree across the fixed dataset and does not support out-of-sample inference. Use K-Means for real-time cluster assignments."
            
    return result

def plot_prediction_probabilities(prob_dict):
    """
    Bar chart of class prediction probabilities.
    """
    if not prob_dict:
        return None
        
    df_prob = pd.DataFrame(list(prob_dict.items()), columns=['Class', 'Probability'])
    df_prob['Percentage'] = (df_prob['Probability'] * 100).round(1)
    
    fig = px.bar(
        df_prob, x='Class', y='Percentage',
        title="Prediction Probability Breakdown (%)",
        color='Percentage',
        color_continuous_scale="Blues",
        text='Percentage'
    )
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Probability (%)",
        yaxis_range=[0, 100],
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig
