
import pandas as pd
import numpy as np

def load_data(file_path):
    """Load and preprocess the car dataset"""
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Loaded dataset with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def clean_data(df):
    """Clean and prepare the dataset for analysis."""
    if df is None:
        return None

    # 1. Lowercase column names
    df.columns = [col.lower().strip() for col in df.columns]

    # 2. Drop garbage columns
    cols_to_drop = [col for col in df.columns if 'unnamed' in col or df[col].isnull().mean() > 0.90]
    df.drop(columns=cols_to_drop, inplace=True)

    # 3. Convert mixed-type columns to proper dtypes
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass

    # 4. Remove misaligned rows (numeric columns with alphabetic strings)
    df = remove_misaligned_rows(df)

    # 5. Fill missing values
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # 6. Clean text columns
    for col in categorical_cols:
        df[col] = df[col].astype(str).str.strip()

    # 7. Remove outliers
    df = remove_outliers(df, columns=numeric_cols)

    return df

def remove_outliers(df, columns=None, method='iqr', threshold=1.5):
    """Remove outliers from specified numeric columns using IQR method."""
    if columns is None:
        columns = df.select_dtypes(include=['float64', 'int64']).columns

    for col in columns:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df

def remove_misaligned_rows(df):
    """Remove rows where numeric columns contain alphabetic characters (likely misaligned)"""
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    to_drop = pd.Series(False, index=df.index)

    for col in numeric_cols:
        mask = df[col].astype(str).str.contains('[a-zA-Z]', na=False)
        to_drop |= mask

    df = df[~to_drop]
    return df

def filter_data(df, filters=None):
    """Apply filters to the dataset"""
    if df is None or filters is None:
        return df
    
    filtered_df = df.copy()
    
    if 'year_range' in filters and 'year' in df.columns:
        min_year, max_year = filters['year_range']
        filtered_df = filtered_df[(filtered_df['year'] >= min_year) & 
                                 (filtered_df['year'] <= max_year)]
    
    if 'makes' in filters and len(filters['makes']) > 0 and 'make' in df.columns:
        filtered_df = filtered_df[filtered_df['make'].isin(filters['makes'])]

    if 'body_types' in filters and len(filters['body_types']) > 0 and 'vehicle size class' in df.columns:
        filtered_df = filtered_df[filtered_df['vehicle size class'].isin(filters['body_types'])]

    return filtered_df
