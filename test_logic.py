import pytest
import pandas as pd
import numpy as np
# Assuming your file is named 'data_processor.py'
from data_processor import remove_outliers 

def test_remove_outliers_basic():
    """
    HAPPY PATH TEST:
    Check if the function removes a clearly extreme value.
    """
    # 1. Setup: Create a small fake dataset
    data = {'price': [10, 12, 11, 13, 1000]} # 1000 is a massive outlier
    df = pd.DataFrame(data)
    
    # 2. Action: Run your function
    result_df = remove_outliers(df, columns=['price'])
    
    # 3. Assert: Verify the outlier (1000) is gone
    assert 1000 not in result_df['price'].values
    assert len(result_df) == 4
    print("Happy Path Test Passed!")

def test_remove_outliers_empty():
    """
    EDGE CASE TEST:
    What happens if we pass an empty DataFrame?
    """
    df = pd.DataFrame({'price': []})
    result_df = remove_outliers(df, columns=['price'])
    
    assert result_df.empty
    print("Edge Case Test Passed!")

from data_processor import clean_data, filter_data

def test_filter_integration_casing():
    """
    TEST: Does filtering work if the raw data has weird casing?
    """
    # 1. Setup: Raw data with a Capital 'Year' and spaces
    raw_data = {'  Year  ': [2020, 2021, 2022], 'make': ['Toyota', 'Honda', 'Ford']}
    df = pd.DataFrame(raw_data)
    
    # 2. Action: Clean it first (this should fix the column name)
    df_cleaned = clean_data(df)
    
    # 3. Action: Try to filter it
    my_filters = {'year_range': (2021, 2022)}
    df_filtered = filter_data(df_cleaned, filters=my_filters)
    
    # 4. Assert: We expect 2 rows back (2021 and 2022)
    assert len(df_filtered) == 2
    print("Integration test passed!")
