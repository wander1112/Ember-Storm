"""
Regression Track Module
Implements all 10 required regression algorithms, cross-validation, tuning, and Plotly diagnostics.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# 10 Algorithms
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

def train_regression_models(X_train, X_test, y_train, y_test, tune_models=True):
    """
    Train and evaluate all 10 regression algorithms.
    """
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0, random_state=42),
        'Lasso Regression': Lasso(alpha=0.1, random_state=42),
        'ElasticNet Regression': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
        'Polynomial Regression': Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('linear', LinearRegression())
        ]),
        'Decision Tree Regressor': DecisionTreeRegressor(max_depth=8, random_state=42),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
        'Support Vector Regressor (SVR)': SVR(C=10.0, kernel='rbf'),
        'K-Nearest Neighbors Regressor': KNeighborsRegressor(n_neighbors=5)
    }
    
    results = []
    trained_estimators = {}
    predictions = {}
    
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            r2 = float(r2_score(y_test, y_pred))
            rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
            mae = float(mean_absolute_error(y_test, y_pred))
            
            results.append({
                'Model': name,
                'R2 Score': round(r2, 4),
                'RMSE': round(rmse, 4),
                'MAE': round(mae, 4),
                '5-Fold CV R2': None  # Calculated for top 2 later
            })
            trained_estimators[name] = model
            predictions[name] = y_pred
        except Exception as e:
            print(f"Error training {name}: {e}")
            
    res_df = pd.DataFrame(results).sort_values(by='R2 Score', ascending=False).reset_index(drop=True)
    
    # Run 5-fold CV on top 2 models
    top_models = res_df.head(2)['Model'].tolist()
    for top_m in top_models:
        est = trained_estimators[top_m]
        cv_scores = cross_val_score(est, X_train, y_train, cv=5, scoring='r2')
        res_df.loc[res_df['Model'] == top_m, '5-Fold CV R2'] = round(float(cv_scores.mean()), 4)
        
    tuning_details = {}
    if tune_models:
        # Tune Random Forest
        rf_grid = GridSearchCV(
            RandomForestRegressor(random_state=42),
            {'n_estimators': [50, 100], 'max_depth': [8, 12]},
            cv=3, scoring='r2'
        )
        rf_grid.fit(X_train, y_train)
        rf_tuned_pred = rf_grid.best_estimator_.predict(X_test)
        tuning_details['Random Forest Regressor'] = {
            'best_params': rf_grid.best_params_,
            'before_r2': res_df.loc[res_df['Model'] == 'Random Forest Regressor', 'R2 Score'].values[0] if 'Random Forest Regressor' in res_df['Model'].values else 0,
            'after_r2': round(float(r2_score(y_test, rf_tuned_pred)), 4)
        }
        trained_estimators['Random Forest Regressor (Tuned)'] = rf_grid.best_estimator_
        
        # Tune SVR
        svr_grid = GridSearchCV(
            SVR(),
            {'C': [1.0, 10.0], 'kernel': ['linear', 'rbf']},
            cv=3, scoring='r2'
        )
        svr_grid.fit(X_train, y_train)
        svr_tuned_pred = svr_grid.best_estimator_.predict(X_test)
        tuning_details['Support Vector Regressor (SVR)'] = {
            'best_params': svr_grid.best_params_,
            'before_r2': res_df.loc[res_df['Model'] == 'Support Vector Regressor (SVR)', 'R2 Score'].values[0] if 'Support Vector Regressor (SVR)' in res_df['Model'].values else 0,
            'after_r2': round(float(r2_score(y_test, svr_tuned_pred)), 4)
        }
        trained_estimators['Support Vector Regressor (SVR) (Tuned)'] = svr_grid.best_estimator_

    return res_df, trained_estimators, predictions, tuning_details

def plot_actual_vs_predicted(y_test, y_pred, model_name="Best Model"):
    """
    Plot actual vs predicted scatter with 45-degree parity line.
    """
    fig = px.scatter(
        x=y_test, y=y_pred,
        labels={'x': 'Actual Life Expectancy (Years)', 'y': 'Predicted Life Expectancy (Years)'},
        title=f"Actual vs. Predicted: {model_name}",
        color_discrete_sequence=['#0B6E4F'],
        opacity=0.75
    )
    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    fig.add_shape(
        type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val,
        line=dict(color="#10B981", width=2.5, dash="dash")
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F0FDF4",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def plot_residual_diagnostics(y_test, y_pred, model_name="Best Model"):
    """
    Residual scatter and residual distribution side-by-side with Emerald Oasis styling.
    """
    residuals = y_test - y_pred
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_pred, y=residuals,
        mode='markers',
        marker=dict(color='#10B981', opacity=0.75, size=7, line=dict(width=1, color='#0B6E4F')),
        name='Residuals'
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#0B6E4F", line_width=2)
    fig.update_layout(
        title=f"Residual Diagnostics: {model_name}",
        xaxis_title="Fitted / Predicted Values",
        yaxis_title="Residuals (Actual - Predicted)",
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F0FDF4",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def plot_feature_importances(model, feature_names):
    """
    Bar chart of tree-based feature importances in Emerald Oasis colors.
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_)
    else:
        return None
        
    feat_df = pd.DataFrame({
        'Feature': feature_names[:len(importances)],
        'Importance': importances
    }).sort_values(by='Importance', ascending=True)
    
    fig = px.bar(
        feat_df, x='Importance', y='Feature', orientation='h',
        title="Relative Epidemiological Feature Importances",
        color='Importance',
        color_continuous_scale=[[0, "#D9F99D"], [0.5, "#10B981"], [1.0, "#0B6E4F"]]
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F0FDF4",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig
