"""
Data Loading & Validation Module
Handles CSV and Excel file ingestion, integrity checks, and summary audits.
"""

import os
import io
import pandas as pd
import numpy as np

def load_file(uploaded_file):
    """
    Load uploaded file (CSV, XLSX, XLS) into a Pandas DataFrame.
    """
    if uploaded_file is None:
        return None, "No file uploaded."
    
    filename = uploaded_file.name
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif filename.endswith('.xls'):
            df = pd.read_excel(uploaded_file, sheet_name=0)
        else:
            return None, "Unsupported file format. Please upload CSV or Excel files."
        
        # Clean column names (strip whitespace)
        df.columns = [str(c).strip() for c in df.columns]
        
        if df.empty:
            return None, "Uploaded dataset contains no rows."
        
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

def load_sample_dataset(dataset_name):
    """
    Load pre-configured sample datasets from the local data folder.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    file_map = {
        'Life Expectancy (Regression)': os.path.join(data_dir, 'Life Expectancy Data.csv'),
        'Maternal Health Risk (Classification)': os.path.join(data_dir, 'Maternal Health Risk Data Set.csv'),
        'Cardiotocography CTG (Clustering)': os.path.join(data_dir, 'CTG.xls')
    }
    
    filepath = file_map.get(dataset_name)
    if not filepath or not os.path.exists(filepath):
        # Fallback to root data folder if not in ml-studio/data
        alt_path = os.path.join(os.path.dirname(base_dir), 'data', os.path.basename(filepath if filepath else ''))
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            return None, f"Sample file not found at {filepath}"

    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xls'):
            # For CTG, use Raw Data sheet if available
            xl = pd.ExcelFile(filepath)
            sheet = 'Raw Data' if 'Raw Data' in xl.sheet_names else 0
            df = pd.read_excel(filepath, sheet_name=sheet)
            df = df.dropna(subset=['NSP']) if 'NSP' in df.columns else df
        else:
            df = pd.read_excel(filepath)

        df.columns = [str(c).strip() for c in df.columns]
        return df, None
    except Exception as e:
        return None, f"Failed to load sample dataset: {str(e)}"

def get_dataset_summary(df):
    """
    Compute dataset overview statistics for metric cards and tables.
    """
    if df is None or df.empty:
        return {}
    
    total_rows = len(df)
    total_features = len(df.columns)
    
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    total_missing = int(df.isnull().sum().sum())
    missing_pct = float((total_missing / (total_rows * total_features)) * 100) if (total_rows * total_features) > 0 else 0.0
    duplicate_rows = int(df.duplicated().sum())
    
    # Calculate simple global outlier count via IQR on numerical features
    total_outliers = 0
    for col in num_cols:
        col_clean = df[col].dropna()
        if len(col_clean) > 4:
            q1 = col_clean.quantile(0.25)
            q3 = col_clean.quantile(0.75)
            iqr = q3 - q1
            outliers = ((col_clean < (q1 - 1.5 * iqr)) | (col_clean > (q3 + 1.5 * iqr))).sum()
            total_outliers += int(outliers)
            
    return {
        'total_rows': total_rows,
        'total_features': total_features,
        'num_cols': num_cols,
        'cat_cols': cat_cols,
        'total_missing': total_missing,
        'missing_pct': round(missing_pct, 2),
        'duplicate_rows': duplicate_rows,
        'total_outliers': total_outliers
    }

def get_columns_audit(df):
    """
    Return a detailed column-by-column audit table.
    """
    audit = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = int(df[col].isnull().sum())
        missing_pct = round((missing / len(df)) * 100, 2)
        unique_vals = int(df[col].nunique())
        
        sample_val = str(df[col].dropna().iloc[0]) if df[col].dropna().shape[0] > 0 else "None"
        
        audit.append({
            'Column': col,
            'Data Type': dtype,
            'Missing Count': missing,
            'Missing %': f"{missing_pct}%",
            'Unique Values': unique_vals,
            'Sample Value': sample_val[:30]
        })
    return pd.DataFrame(audit)
