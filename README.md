# 🌍 Travel Budget Predictor 💰

## What's this all about?

Ever wondered how much that dream trip might cost? 🤔 This project helps predict travel budgets (Hotel 🏨, Food 🍔, Activities 🎭) based on your trip plans! It uses a nifty machine learning model served up with a Flask API and packaged neatly in Docker 🐳.

## Project Folder Layout 📁

Here's how things are organized:

```
. 
├── data/                 # Your training data goes here (like 17-mar-25-extraction.csv)
│   └── .placeholder
├── src/                  # All the important code lives here!
│   ├── artifacts/        # The brains of the operation: saved model & preprocessor
│   │   ├── model.joblib
│   │   └── preprocessor.joblib
│   ├── static/           # Pretty things for the web UI (CSS, JS)
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/        # The HTML structure for the web UI
│   │   └── index.html
│   ├── app.py            # The Flask app that runs the show (API & UI)
│   └── train_model.py    # Script to teach the model 🧠
├── tests/                # Making sure things work (Pytest tests)
│   └── test_preprocessing.py
├── .gitignore          # Tells Git what to ignore (like secret virtual envs!)
├── Dockerfile            # Instructions for Docker to build the image
├── requirements.txt      # List of Python packages needed
└── README.md             # You are here! 📍
```

## Get Started! 🚀

**1. Stuff You Need:**
   - Python 3.8+ 🐍
   - pip (Python's package installer)
   - Docker Desktop (Gotta have the whale!)
   - Git (For version control magic ✨)

**2. Grab the Code (if you haven't):**
   ```bash
   git clone https://github.com/jomasego/travel-budget-prediction.git
   cd travel-budget-prediction
   ```

**3. Virtual Environment & Packages:**
   (It's like a sandbox for your Python stuff!)
   ```bash
   # Create the sandbox
   python -m venv .venv
   
   # Jump into the sandbox (Windows PowerShell)
   .\.venv\Scripts\Activate.ps1
   # Or (Git Bash / Linux / macOS)
   # source .venv/bin/activate 
   
   # Install the goodies
   pip install -r requirements.txt
   ```

**4. Add Your Data:**
   - Make sure your training data CSV (e.g., `17-mar-25-extraction.csv`) is chilling inside the `data/` folder.

**5. Train the Model:**
   - Time to make the magic happen! This creates the `.joblib` files in `src/artifacts/`.
   ```bash
   python src/train_model.py
   ```
   *(This might take a moment, grab a coffee! ☕)*

**6. Run Tests (Good idea! ✅):**
   ```bash
   pytest
   ```

**7. Run Locally (The Simple Way):**
   ```bash
   # Make sure your sandbox (.venv) is active!
   flask run --port=5001
   ```
   - Open your browser to 👉 [http://localhost:5001](http://localhost:5001)

**8. Run with Docker (The Cool Way 😎):**
   ```bash
   # Build the Docker image (might take a bit the first time)
   docker build -t travel-predictor .
   
   # Run the container!
   docker run -p 5001:5001 travel-predictor
   ```
   - Open your browser to 👉 [http://localhost:5001](http://localhost:5001)

## Talk to the API 🗣️

Want to get predictions programmatically? No problem!

- **URL:** `/predict`
- **Method:** `POST`
- **Data:** Send JSON
- **Example (`curl` command):**
  ```bash
  curl -X POST http://localhost:5001/predict -H "Content-Type: application/json" -d '{
    "# Adults": 2,
    "# Children & Babies": 0,
    "Trip Duration Category": "Short",
    "Country": "Spain",
    "Theme Parks": 1,
    "Hidden Gems": 0,
    "Cultural Attractions": 1,
    "Beach or Pools": 1,
    "Sunset Spots": 1,
    "Nature Getaway": 0
  }'
  ```
- **What you get back (Example):**
  ```json
  {
    "predicted_budgets": {
      "Activity Budget in EUR": 120.00,
      "Food Budget in EUR": 200.00,
      "Hotel Budget in EUR": 450.99
    }
  }
  ```
  *(Disclaimer: Numbers are just examples! Your mileage may vary.)*

## Quick Notes & Caveats 📝

- The data cleaning is pretty basic. Could be fancier! ✨
- We're using a simple Linear Regression model. Others might be better! 🤷
- Not much feature engineering went into this.
- Hyperparameters weren't really tuned. It's more of a starting point! 🌱
