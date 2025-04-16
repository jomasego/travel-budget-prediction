import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Define paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) # Project root is one level up from src/

# --- Configuration ---
DATA_FILE = os.path.join(PROJECT_ROOT, 'data', '17-mar-25-extraction.csv') # Data is in ../data/
TARGET_VARIABLES = ['Hotel Budget in EUR', 'Food Budget in EUR', 'Activity Budget in EUR'] # New multi-target
ARTIFACTS_DIR = os.path.join(SCRIPT_DIR, 'artifacts') # Save artifacts inside src/
MODEL_FILENAME = os.path.join(ARTIFACTS_DIR, 'model.joblib') # Renamed for clarity
PREPROCESSOR_FILENAME = os.path.join(ARTIFACTS_DIR, 'preprocessor.joblib') # New preprocessor artifact
FEATURES = [
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
CATEGORICAL_FEATURES = ['Trip Duration Category', 'Country']
NUMERICAL_FEATURES = [
    '# Adults',
    '# Children & Babies',
    'Theme Parks',
    'Hidden Gems',
    'Cultural Attractions',
    'Beach or Pools',
    'Sunset Spots',
    'Nature Getaway'
]

# Create output directory if it doesn't exist
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# --- Load Data ---
def load_data(file_path):
    """Loads data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        print(f"Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# --- Preprocessing & Training ---
def train_model(df):
    """Preprocesses data and trains a linear regression model."""
    if df is None:
        return

    # 1. Select relevant columns + Drop rows with missing target(s)
    all_cols = FEATURES + TARGET_VARIABLES
    df = df[all_cols].copy()
    df.dropna(subset=TARGET_VARIABLES, inplace=True) # Drop rows if ANY target is missing

    # 2. Handle missing features (simple imputation: fillna with 0 for numeric, 'Missing' for categorical)
    #    Note: More sophisticated imputation might be needed for real-world scenarios.
    for col in NUMERICAL_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') # Ensure numeric types
            df[col].fillna(0, inplace=True)
        else:
            print(f"Warning: Numerical feature '{col}' not found in data.")

    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            df[col].fillna('Missing', inplace=True)
            df[col] = df[col].astype(str) # Ensure string type for encoder
        else:
            print(f"Warning: Categorical feature '{col}' not found in data.")

    # Check if target became non-numeric or has issues
    for target in TARGET_VARIABLES:
        df[target] = pd.to_numeric(df[target], errors='coerce')
    df.dropna(subset=TARGET_VARIABLES, inplace=True) # Drop rows where any target became NaN

    if df.empty:
        print("Error: No data remaining after cleaning. Check input data and feature/target names.")
        return

    print(f"Shape after cleaning: {df.shape}")

    X = df[FEATURES]
    y = df[TARGET_VARIABLES] # Use list of targets

    # 3. Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Define preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', NUMERICAL_FEATURES), # Pass through numerical features as is (for now)
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES)], # sparse=False for dense array
        remainder='drop') # Drop columns not specified

    # 5. Define the model
    model = LinearRegression()

    # 6. Fit the preprocessor and transform the data
    # Fit on training data ONLY
    print("\nFitting preprocessor...")
    X_train_processed = preprocessor.fit_transform(X_train)
    print("Transforming training & test data...")
    # Transform both train and test data
    X_test_processed = preprocessor.transform(X_test)
    print(f"Shape after preprocessing (train): {X_train_processed.shape}")
    print(f"Shape after preprocessing (test): {X_test_processed.shape}")

    # Get feature names after one-hot encoding (important for debugging/understanding)
    # Note: This assumes 'passthrough' keeps original names and OneHotEncoder generates names
    try:
        ohe_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(CATEGORICAL_FEATURES)
        processed_feature_names = NUMERICAL_FEATURES + list(ohe_feature_names)
        print(f"Number of features after preprocessing: {len(processed_feature_names)}")
        # print("Feature names:", processed_feature_names) # Uncomment to see all feature names
    except Exception as e:
        print(f"Could not get feature names after OHE: {e}")
        processed_feature_names = None

    # 7. Train the model on the PROCESSED data
    print("\nTraining model...")
    model.fit(X_train_processed, y_train)
    print("Model training complete.")

    # 8. Evaluate the model using PROCESSED test data
    y_pred = model.predict(X_test_processed)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n--- Model Evaluation (Combined Targets) ---")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R-squared (R2): {r2:.2f}")

    # Optional: Print metrics per target
    print("\n--- Metrics Per Target ---")
    for i, target_name in enumerate(TARGET_VARIABLES):
        mse_target = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
        r2_target = r2_score(y_test.iloc[:, i], y_pred[:, i])
        print(f"  {target_name}:")
        print(f"    MSE: {mse_target:.2f}")
        print(f"    R2: {r2_target:.2f}")

    # 9. Save the trained model AND the fitted preprocessor
    joblib.dump(model, MODEL_FILENAME)
    joblib.dump(preprocessor, PREPROCESSOR_FILENAME)
    print(f"\nModel saved to {MODEL_FILENAME}")
    print(f"Preprocessor saved to {PREPROCESSOR_FILENAME}")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting model training process...")
    travel_data = load_data(DATA_FILE)
    train_model(travel_data)
