# Travel Budget Prediction Pipeline

## Project Goal

This project aims to predict travel budgets (Hotel, Food, Activity) based on various trip features using a machine learning model served via a Flask API and packaged in a Docker container.

## Project Structure

```
. 
├── data/                 # Contains the training data (e.g., 17-mar-25-extraction.csv)
│   └── .placeholder
├── src/                  # Source code
│   ├── artifacts/        # Saved model and preprocessor artifacts
│   │   ├── model.joblib
│   │   └── preprocessor.joblib
│   ├── static/           # CSS and JavaScript for the web UI
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/        # HTML template for the web UI
│   │   └── index.html
│   ├── app.py            # Flask application (API and UI serving)
│   └── train_model.py    # Script to preprocess data and train the model
├── tests/                # Pytest tests
│   └── test_preprocessing.py
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── Dockerfile            # Instructions to build the Docker image
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Setup and Usage

**1. Prerequisites:**
   - Python 3.8+
   - pip
   - Docker Desktop (or Docker Engine)
   - Git

**2. Clone the Repository (if applicable):**
   ```bash
   git clone https://github.com/jomasego/travel-budget-prediction.git
   cd travel-budget-prediction
   ```

**3. Set up Virtual Environment & Install Dependencies:**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows PowerShell)
   .\.venv\Scripts\Activate.ps1
   # Or Activate (Git Bash / Linux / macOS)
   # source .venv/bin/activate 
   
   # Install requirements
   pip install -r requirements.txt
   ```

**4. Place Data:**
   - Ensure your training data CSV file (e.g., `17-mar-25-extraction.csv`) is placed inside the `data/` directory.

**5. Train the Model:**
   - Run the training script to generate the model and preprocessor artifacts in `src/artifacts/`:
   ```bash
   python src/train_model.py
   ```

**6. Run Tests (Optional):**
   ```bash
   pytest
   ```

**7. Run Locally via Flask:**
   ```bash
   # Make sure the virtual environment is active
   flask run --port=5001
   ```
   - Access the web UI at [http://localhost:5001](http://localhost:5001)

**8. Build and Run via Docker:**
   ```bash
   # Build the Docker image
   docker build -t travel-predictor .
   
   # Run the container
   docker run -p 5001:5001 travel-predictor
   ```
   - Access the web UI at [http://localhost:5001](http://localhost:5001)

## API Endpoint

- **URL:** `/predict`
- **Method:** `POST`
- **Data Format:** JSON
- **Example Request (`curl`):**
  ```bash
  curl -X POST http://localhost:5001/predict -H "Content-Type: application/json" -d '{
    "# Adults": 2,
    "# Children & Babies": 1,
    "Trip Duration Category": "Medium",
    "Country": "France",
    "Theme Parks": 0,
    "Hidden Gems": 1,
    "Cultural Attractions": 1,
    "Beach or Pools": 0,
    "Sunset Spots": 1,
    "Nature Getaway": 0
  }'
  ```
- **Example Response:**
  ```json
  {
    "predicted_budgets": {
      "Activity Budget in EUR": 150.75,
      "Food Budget in EUR": 250.50,
      "Hotel Budget in EUR": 500.25
    }
  }
  ```
  *(Note: Actual budget values are examples)*

## Notes/Limitations

- Preprocessing is basic (median/missing fill, OneHotEncoding). More advanced techniques could improve performance.
- Model used is Linear Regression; other models might yield better results.
- Minimal feature engineering performed.
- No extensive hyperparameter tuning was done.
