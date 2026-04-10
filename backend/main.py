import io
import pandas as pd

import joblib
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# 1. Load the model
# It's best to do this globally so it stays in memory
model = joblib.load("../model/model.joblib")

app = FastAPI(title="Model Inference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your Svelte dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 2. Define the input schema


#GENERATE A PING ENDPOINT
@app.get("/ping")
def ping():
    x = 5
    x = x + 10
    y = x
    return {"message": "pong"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Convert input data to the format your model expects (usually a 2D array)
    contents = await file.read()                  # raw bytes
    df = pd.read_csv(io.BytesIO(contents))
            # wrap in BytesIO → pandas
    X = df[top_features]
    # 3. Perform inference
    prediction = model.predict(X)
    probability = model.predict_proba(X)
    
    # Return the result as JSON
    return {"prediction": int(prediction[0]),
            "probability": list(probability[0])
            }