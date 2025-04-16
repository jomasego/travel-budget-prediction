from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__) # Serve files from the static folder

# Define paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuration ---
ARTIFACTS_DIR = os.path.join(SCRIPT_DIR, 'artifacts') # Artifacts dir inside src/
MODEL_FILENAME = os.path.join(ARTIFACTS_DIR, 'model.joblib') # Path to model file
PREPROCESSOR_FILENAME = os.path.join(ARTIFACTS_DIR, 'preprocessor.joblib') # Path to preprocessor file

# Update expected features to match the preprocessor's input
EXPECTED_FEATURES = [
    '# Adults',
    '# Children & Babies',
    'Trip Duration Category',
    # 'Food Budget in EUR', # Removed
    'Country',
    'Theme Parks',
    'Hidden Gems',
    'Cultural Attractions',
    'Beach or Pools',
    'Sunset Spots',
    'Nature Getaway'
]
# Define target names for structuring the output
TARGET_NAMES = ['Hotel Budget in EUR', 'Food Budget in EUR', 'Activity Budget in EUR']

# --- Load Model & Preprocessor ---
def load_artifacts(model_path, preprocessor_path):
    """Loads the trained model and preprocessor."""
    try:
        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)
        print(f"Model loaded from {model_path}")
        print(f"Preprocessor loaded from {preprocessor_path}")
        return model, preprocessor
    except FileNotFoundError:
        print(f"Error: Artifact file not found at {model_path} or {preprocessor_path}. Please run the training script first.")
        return None, None
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        return None, None

# Load artifacts at app startup
model, preprocessor = load_artifacts(MODEL_FILENAME, PREPROCESSOR_FILENAME)

# --- API Endpoints ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Receives feature data in JSON, predicts budget, returns prediction."""
    # Check if model and preprocessor loaded successfully
    if not model or not preprocessor:
         return jsonify({"error": "Model or preprocessor not loaded. Check server logs."}), 500

    try:
        data = request.get_json(force=True)
        print(f"Received data: {data}")

        # Validate input - check if all expected features are present
        missing_features = [f for f in EXPECTED_FEATURES if f not in data]
        if missing_features:
            return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400

        # Prepare input data for the model pipeline (needs to be a DataFrame)
        # Ensure the order matches the training data
        input_df = pd.DataFrame([data]) 
        input_df = input_df[EXPECTED_FEATURES] # Ensure correct column order

        # Convert numeric columns explicitly to avoid potential type issues
        # Note: More robust type checking/conversion might be needed in production
        # Update numeric columns list
        numeric_cols = [
            '# Adults',
            '# Children & Babies',
            # 'Food Budget in EUR', # Removed
            'Theme Parks',
            'Hidden Gems',
            'Cultural Attractions',
            'Beach or Pools',
            'Sunset Spots',
            'Nature Getaway'
        ]
        for col in numeric_cols:
            # Handle boolean features that might come as strings ('true'/'false') or numbers (1/0)
            if col in ['Theme Parks', 'Hidden Gems', 'Cultural Attractions', 'Beach or Pools', 'Sunset Spots', 'Nature Getaway']:
                # Convert common string representations of boolean to 0/1
                if isinstance(input_df[col].iloc[0], str):
                    input_df[col] = input_df[col].str.lower().map({'true': 1, '1': 1, 'yes': 1, 'false': 0, '0': 0, 'no': 0}).fillna(0)
                else:
                    # Assume numeric or boolean input, convert to int 0/1
                    input_df[col] = input_df[col].astype(bool).astype(int)
            else:
                # Handle regular numeric columns
                 input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

        # Handle potential NaNs from coercion (though ideally input is clean)
        if input_df.isnull().any().any():
             return jsonify({"error": "Invalid numeric input detected."}), 400

        # Preprocess the input data using the loaded preprocessor
        print(f"Input shape before preprocessing: {input_df.shape}")
        input_processed = preprocessor.transform(input_df)
        print(f"Input shape after preprocessing: {input_processed.shape}")

        # Make prediction using the loaded model on the PROCESSED data
        prediction = model.predict(input_processed)

        # Structure the output with target names
        predicted_budgets = dict(zip(TARGET_NAMES, prediction[0]))

        print(f"Prediction: {predicted_budgets}")
        # Return all predictions
        return jsonify({"predicted_budgets": predicted_budgets})

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500

# --- Run App ---
if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on the network (needed for Docker)
    # Use a port like 5000 (default Flask port)
    port = int(os.environ.get('PORT', 5001)) # Use 5001 to avoid potential conflicts
    app.run(host='0.0.0.0', port=port, debug=True) # Enable debug for development
