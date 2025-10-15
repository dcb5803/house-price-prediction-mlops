import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import os

# Define the structure for incoming data
# Adjust these features to match your trained model's inputs!
class HouseFeatures(BaseModel):
    feature1: float # e.g., 'Median_Income'
    feature2: float # e.g., 'House_Age'
    feature3: float # e.g., 'Avg_Rooms'

# --- 1. Initialization ---
app = FastAPI(title="House Price Prediction API")
model = None

@app.on_event("startup")
async def load_model():
    """Load the trained model and preprocessor when the API starts."""
    global model
    try:
        # Assumes model.pkl is in the root or a 'model' directory
        model_path = os.path.join("model", "model.pkl")
        model = joblib.load(model_path)
        print(f"Model loaded successfully from: {model_path}")
    except FileNotFoundError:
        print("ERROR: model.pkl not found. Check the path.")
        model = None # Stop the app or handle gracefully
    except Exception as e:
        print(f"An error occurred loading the model: {e}")
        model = None

# --- 2. Health Check Endpoint ---
@app.get("/health", tags=["Status"])
def health_check():
    """Simple health check to ensure the service is running."""
    if model:
        return {"status": "ok", "model_loaded": True}
    return {"status": "error", "model_loaded": False}

# --- 3. Prediction Endpoint ---
@app.post("/predict", tags=["Prediction"])
def predict_price(features: HouseFeatures):
    if model is None:
        return {"error": "Model not loaded. Check server logs."}

    # Convert incoming data to model input format (e.g., a 2D array)
    input_data = [
        features.feature1,
        features.feature2,
        features.feature3
    ]

    # Preprocessing (if needed, e.g., scaling should happen here)
    # The saved model might handle some pre-processing, or you need to load
    # a separate 'scaler.pkl' and apply it. For simplicity, we skip it here.
    
    try:
        # Reshape for single prediction: (1, n_features)
        prediction = model.predict([input_data])[0]
        
        return {
            "predicted_price_usd": round(float(prediction), 2),
            "model_version": "1.0" # Good practice to version the model output
        }
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}

# To run locally: uvicorn app:app --reload --port 8000
