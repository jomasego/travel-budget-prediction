import pytest
import pandas as pd
import joblib
import os

# Define paths relative to the test file location
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(os.path.dirname(TEST_DIR), 'src') # src/ is one level up from tests/
ARTIFACTS_DIR = os.path.join(SRC_DIR, 'artifacts')
PREPROCESSOR_FILENAME = os.path.join(ARTIFACTS_DIR, 'preprocessor.joblib')

# Define expected features based on app.py (must match exactly)
EXPECTED_FEATURES = [
    '# Adults',
    '# Children & Babies',
    'Trip Duration Category',
    'Country',
    'Theme Parks',
    'Hidden Gems',
    'Cultural Attractions',
    'Beach or Pools',
    'Sunset Spots',
    'Nature Getaway'
]

# Expected number of features AFTER preprocessing (based on training output)
EXPECTED_OUTPUT_FEATURES = 79

@pytest.fixture(scope="module")
def preprocessor():
    """Loads the preprocessor artifact once per module."""
    if not os.path.exists(PREPROCESSOR_FILENAME):
        pytest.fail(f"Preprocessor artifact not found at {PREPROCESSOR_FILENAME}. Run training first.")
    try:
        return joblib.load(PREPROCESSOR_FILENAME)
    except Exception as e:
        pytest.fail(f"Failed to load preprocessor: {e}")

def test_preprocessor_output_shape(preprocessor):
    """Tests if the preprocessor outputs the correct number of features."""
    # Create sample input data (one row)
    # Use plausible values matching the expected types
    sample_data = {
        '# Adults': [2],
        '# Children & Babies': [1],
        'Trip Duration Category': ['Short'], # Example category
        'Country': ['Spain'],          # Example category
        'Theme Parks': [1],            # Boolean as 1/0
        'Hidden Gems': [0],
        'Cultural Attractions': [1],
        'Beach or Pools': [1],
        'Sunset Spots': [0],
        'Nature Getaway': [0]
    }
    sample_df = pd.DataFrame(sample_data, columns=EXPECTED_FEATURES) # Ensure correct column order

    # Transform the sample data
    try:
        processed_data = preprocessor.transform(sample_df)
    except Exception as e:
        pytest.fail(f"Preprocessor transformation failed: {e}")

    # Assert the number of columns (features)
    assert processed_data.shape[1] == EXPECTED_OUTPUT_FEATURES, \
        f"Expected {EXPECTED_OUTPUT_FEATURES} features after preprocessing, but got {processed_data.shape[1]}"
