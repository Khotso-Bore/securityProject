import io
import pandas as pd

import joblib
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
from ThreatModels import InsiderTheatModel
import shap

# 1. Load the model
# It's best to do this globally so it stays in memory

top_features = [
    "total_files_burned",
    "burned_from_other",
    "num_printed_pages_off_hours",
    "total_printed_pages",
    "num_unique_campus",
    "hostility_country_level",
    "entry_during_weekend",
    "num_entries",
]

scaler = joblib.load('../model/scaler.joblib')  # Load the scaler for preprocessing

model = InsiderTheatModel(input_size=len(top_features))  # Adjust input_size based on your features
model.load_state_dict(torch.load('../model/model_weights.pth', map_location=torch.device('cpu')))

model.eval()  # Set to evaluation mode

# 3. Setup SHAP (Requires a background sample from your training data)
# Use a small subset of scaled training data (e.g., 50-100 rows)
train_samples = pd.read_csv("insider_threat_clean_dataset.csv")[top_features][:100]  # Adjust path and number of samples as needed
# print(train_samples.head())
background_scaled = torch.tensor(scaler.transform(train_samples), dtype=torch.float32)
explainer = shap.DeepExplainer(model, background_scaled)


app = FastAPI(title="Model Inference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your Svelte dev server
    allow_methods=["*"],
    allow_headers=["*"],
)



# 2. Define the input schema


#GENERATE A PING ENDPOINT
@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Convert input data to the format your model expects (usually a 2D array)
    contents = await file.read()                  # raw bytes
    df = pd.read_csv(io.BytesIO(contents))
            # wrap in BytesIO → pandas
    X = df[top_features]
    X_scaled = scaler.transform(X)
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)  # Convert to tensor
    # 3. Perform inference
    with torch.no_grad():
        prediction_logits = model(X_tensor)  # Get raw output from the model

    # 2. Calculate SHAP values for this specific input
    shap_values = explainer(X_tensor)
    
    results = []
    for i in range(len(df)):
        # Mapping feature names to their SHAP values for each row
        feature_importance = dict(zip(top_features, shap_values[i].values.flatten().tolist()))
        
        results.append({
            "row_index": i,
            "prediction_prob": float(torch.sigmoid(prediction_logits[i]).item()),
            "is_malicious": bool(torch.sigmoid(prediction_logits[i]).item() > 0.7),
            "feature_contributions": feature_importance
        })

    return {"results": results}