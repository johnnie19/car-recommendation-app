import pandas as pd
import numpy as np

def load_data(file_path):
    """Load and preprocess the car dataset"""
    try:
        df = pd.read_csv(file_path)
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

    # 3. Fill missing values
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # 4. Clean text columns
    for col in categorical_cols:
        df[col] = df[col].str.strip()

    return df


def filter_data(df, filters=None):
    """Apply filters to the dataset"""
    if df is None or filters is None:
        return df
    
    filtered_df = df.copy()
    
    # Apply price filter if available
    if 'price_range' in filters and 'price' in df.columns:
        min_price, max_price = filters['price_range']
        filtered_df = filtered_df[(filtered_df['price'] >= min_price) & 
                                 (filtered_df['price'] <= max_price)]
    
    # Apply make filter if available
    if 'makes' in filters and len(filters['makes']) > 0 and 'make' in df.columns:
        filtered_df = filtered_df[filtered_df['make'].isin(filters['makes'])]
    
    # Apply body type filter if available
    if 'body_types' in filters and len(filters['body_types']) > 0 and 'vehicle size class' in df.columns:
        filtered_df = filtered_df[filtered_df['vehicle size class'].isin(filters['body_types'])]
    
    return filtered_df