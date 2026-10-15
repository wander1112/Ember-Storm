"""
Preprocessing & Pipeline Module
Imputation, duplicate removal, encoding, scaling, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def handle_duplicates(df):
    """
    Remove duplicate rows.
    """
    dup_count = int(df.duplicated().sum())
    df_clean = df.drop_duplicates().reset_index(drop=True)
    return df_clean, dup_count

def impute_missing_values(df, strategy_num='median', strategy_cat='most_frequent', fill_value=None):
    """
    Apply imputation to numerical and categorical features.
    """
    df_imp = df.copy()
    
    num_cols = df_imp.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df_imp.select_dtypes(exclude=[np.number]).columns.tolist()
    
    if strategy_num == 'drop':
        df_imp = df_imp.dropna(subset=num_cols).reset_index(drop=True)
    elif num_cols:
        if strategy_num in ['mean', 'median', 'most_frequent']:
            imputer_num = SimpleImputer(strategy=strategy_num)
            df_imp[num_cols] = imputer_num.fit_transform(df_imp[num_cols])
        elif strategy_num == 'constant' and fill_value is not None:
            df_imp[num_cols] = df_imp[num_cols].fillna(fill_value)
            
    if strategy_cat == 'drop':
        df_imp = df_imp.dropna(subset=cat_cols).reset_index(drop=True)
    elif cat_cols:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df_imp[cat_cols] = imputer_cat.fit_transform(df_imp[cat_cols])
        
    return df_imp

def engineer_features(df, preset_type='none', custom_formula=None):
    """
    Add domain-engineered features with justification.
    """
    df_feat = df.copy()
    justification = ""
    
    if preset_type == 'map' and 'SystolicBP' in df.columns and 'DiastolicBP' in df.columns:
        # Mean Arterial Pressure
        df_feat['MAP'] = (df_feat['SystolicBP'] + 2 * df_feat['DiastolicBP']) / 3.0
        justification = "Engineered Feature: `MAP` (Mean Arterial Pressure) = (SystolicBP + 2*DiastolicBP)/3. Captures systemic vascular perfusion pressure better than systolic or diastolic pressure individually."
    elif preset_type == 'immunization' and all(c in df.columns for c in ['Hepatitis B', 'Polio', 'Diphtheria']):
        df_feat['Immunization_Index'] = (df_feat['Hepatitis B'] + df_feat['Polio'] + df_feat['Diphtheria']) / 3.0
        justification = "Engineered Feature: `Immunization_Index` composite average of HepB, Polio, and Diphtheria vaccination rates to reduce collinearity while retaining public health signal."
    elif preset_type == 'custom' and custom_formula:
        # Evaluate simple arithmetic custom column: e.g. col1 / col2
        try:
            # Safe evaluation for pandas column operations
            new_col, expr = custom_formula.split('=', 1)
            new_col = new_col.strip()
            df_feat[new_col] = df_feat.eval(expr.strip())
            justification = f"Custom Engineered Feature: `{new_col}` created via expression `{expr.strip()}`."
        except Exception as e:
            return df, f"Custom formula error: {str(e)}"
            
    return df_feat, justification

def build_preprocessor_pipeline(num_cols, cat_cols, scaler_type='standard'):
    """
    Construct a scikit-learn ColumnTransformer for leakage-free modeling.
    """
    scaler = StandardScaler() if scaler_type == 'standard' else MinMaxScaler()
    
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', scaler)
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    transformers = []
    if num_cols:
        transformers.append(('num', num_transformer, num_cols))
    if cat_cols:
        transformers.append(('cat', cat_transformer, cat_cols))
        
    return ColumnTransformer(transformers=transformers, remainder='drop')
