import io
import pandas as pd

import joblib
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
from ThreatModels import InsiderTheatModel
import shap


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

scaler = joblib.load('../model/scaler.joblib') 

model = InsiderTheatModel(input_size=len(top_features))

model.load_state_dict(torch.load('../model/model_weights.pth', map_location=torch.device('cpu')))

model.eval()

# 3. Setup SHAP (Requires a background sample from your training data)
# Use a small subset of scaled training data (e.g., 50-100 rows)
train_samples = pd.read_csv("insider_threat_clean_dataset.csv")[top_features][:100]

background_scaled = torch.tensor(scaler.transform(train_samples), dtype=torch.float32)
explainer = shap.DeepExplainer(model, background_scaled)


app = FastAPI(title="Model Inference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
  
    contents = await file.read()                 
    df = pd.read_csv(io.BytesIO(contents))
    
    X = df[top_features]
    X_scaled = scaler.transform(X)
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)  

    with torch.no_grad():
        prediction_logits = model(X_tensor)

    # 2. Calculate SHAP values for this specific input
    shap_values = explainer(X_tensor)
    
    results = []
    for i in range(len(df)):
        # Mapping feature names to their SHAP values for each row
        feature_importance = dict(zip(top_features, shap_values[i].values.flatten().tolist()))
        
        prob = float(torch.sigmoid(prediction_logits[i]).item())
        results.append({
            "row_index": i,
            "prediction_prob": prob,
            "is_malicious": bool(prob > 0.5),
            "feature_contributions": feature_importance
        })

    return {"results": results}