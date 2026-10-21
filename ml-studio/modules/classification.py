"""
Classification Track Module
Implements all 10 required classification algorithms, multi-class ROC-AUC (OvR), and Plotly diagnostics.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, auc, confusion_matrix
)

# 10 Algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier, AdaBoostClassifier,
    GradientBoostingClassifier, BaggingClassifier
)
from sklearn.neural_network import MLPClassifier

def train_classification_models(X_train, X_test, y_train, y_test, class_names=None, tune_models=True):
    """
    Train and evaluate all 10 classification algorithms.
    """
    models = {
        'Logistic Regression': LogisticRegression(max_iter=500, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes (Gaussian)': GaussianNB(),
        'Decision Tree Classifier': DecisionTreeClassifier(max_depth=6, random_state=42),
        'Support Vector Machine (SVC)': SVC(probability=True, random_state=42),
        'Random Forest Classifier': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        'AdaBoost Classifier': AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=8, random_state=42), n_estimators=60, learning_rate=0.5, random_state=42),
        'Gradient Boosting Classifier': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42),
        'Bagging Classifier': BaggingClassifier(estimator=DecisionTreeClassifier(random_state=42), n_estimators=50, random_state=42),
        'MLP Classifier (Neural Net)': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    }
    
    results = []
    trained_estimators = {}
    predictions = {}
    probabilities = {}
    
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Predict probabilities if supported
            if hasattr(model, 'predict_proba'):
                y_prob = model.predict_proba(X_test)
            else:
                y_prob = None
                
            acc = float(accuracy_score(y_test, y_pred))
            prec = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
            rec = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
            f1 = float(f1_score(y_test, y_pred, average='weighted'))
            
            # Compute ROC-AUC (OvR)
            roc_auc = None
            if y_prob is not None:
                try:
                    if len(np.unique(y_test)) > 2:
                        roc_auc = float(roc_auc_score(y_test, y_prob, multi_class='ovr', average='weighted'))
                    else:
                        # Binary
                        roc_auc = float(roc_auc_score(y_test, y_prob[:, 1]))
                except Exception:
                    roc_auc = None
                    
            results.append({
                'Algorithm': name,
                'Accuracy': round(acc, 4),
                'Precision': round(prec, 4),
                'Recall': round(rec, 4),
                'F1-Score': round(f1, 4),
                'ROC-AUC (OvR)': round(roc_auc, 4) if roc_auc is not None else "N/A"
            })
            
            trained_estimators[name] = model
            predictions[name] = y_pred
            probabilities[name] = y_prob
        except Exception as e:
            print(f"Error training {name}: {e}")
            
    res_df = pd.DataFrame(results).sort_values(by='Accuracy', ascending=False).reset_index(drop=True)
    
    tuning_details = {}
    if tune_models:
        # Tune Random Forest
        rf_grid = GridSearchCV(
            RandomForestClassifier(random_state=42),
            {'n_estimators': [50, 100], 'max_depth': [6, 10]},
            cv=3, scoring='accuracy'
        )
        rf_grid.fit(X_train, y_train)
        rf_tuned_pred = rf_grid.best_estimator_.predict(X_test)
        tuning_details['Random Forest Classifier'] = {
            'best_params': rf_grid.best_params_,
            'before_acc': res_df.loc[res_df['Algorithm'] == 'Random Forest Classifier', 'Accuracy'].values[0] if 'Random Forest Classifier' in res_df['Algorithm'].values else 0,
            'after_acc': round(float(accuracy_score(y_test, rf_tuned_pred)), 4)
        }
        trained_estimators['Random Forest Classifier (Tuned)'] = rf_grid.best_estimator_

    return res_df, trained_estimators, predictions, probabilities, tuning_details

def plot_confusion_matrix_plotly(y_test, y_pred, class_names=None, model_name="Best Model"):
    """
    Interactive heatmap of the confusion matrix.
    """
    cm = confusion_matrix(y_test, y_pred)
    labels = [str(c) for c in (class_names if class_names is not None else sorted(np.unique(y_test)))]
    
    fig = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Predicted Class", y="Actual Class", color="Sample Count"),
        x=labels,
        y=labels,
        color_continuous_scale=[[0, "#FFF0E8"], [0.5, "#F05A78"], [1.0, "#BE3455"]],
        title=f"Confusion Matrix: {model_name}"
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFF0E8",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def plot_multiclass_roc_curves(y_test, y_prob, class_names, model_name="Best Model"):
    """
    Interactive multi-class One-vs-Rest ROC curve comparison with Coral Bloom clinical risk palette.
    """
    fig = go.Figure()
    
    risk_color_map = {
        'low risk': '#10B981',       # Mint Jade
        'mid risk': '#FFB38A',       # Warm Peach
        'high risk': '#BE3455'       # Raspberry
    }
    
    num_classes = len(class_names)
    for i, cname in enumerate(class_names):
        y_binary = (y_test == i).astype(int)
        if len(np.unique(y_binary)) > 1:
            fpr, tpr, _ = roc_curve(y_binary, y_prob[:, i])
            roc_val = auc(fpr, tpr)
            curve_color = risk_color_map.get(str(cname).lower(), '#F05A78')
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f"{str(cname).title()} (AUC = {roc_val:.3f})",
                line=dict(color=curve_color, width=2.8)
            ))
            
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        line=dict(dash='dash', color='#BE3455', width=1.5),
        name='Chance Baseline'
    ))
    
    fig.update_layout(
        title=f"One-vs-Rest (OvR) ROC Curves: {model_name}",
        xaxis_title="False Positive Rate (1 - Specificity)",
        yaxis_title="True Positive Rate (Sensitivity)",
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFF0E8",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig
