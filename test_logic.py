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
