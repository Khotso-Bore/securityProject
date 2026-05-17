# Insider Threat Detection Backend

A FastAPI-based machine learning inference server that detects insider threats using a deep neural network with SHAP explainability.

## Overview

This backend provides REST API endpoints to:

- **Predict insider threats** from employee behavior data
- **Explain predictions** using SHAP (SHapley Additive exPlanations) values to show which features contributed to each prediction
- **Health check** the service

The system uses a pre-trained PyTorch neural network that analyzes employee activities (file access, printing, locations, etc.) to identify potential insider threats with a maliciousness confidence score and detailed feature importance breakdowns.

## Features

- **Deep Learning Model**: 3-layer neural network trained on insider threat behavioral data
- **Explainability**: SHAP DeepExplainer provides per-sample feature contribution analysis
- **Batch Processing**: Handle multiple employee records in a single CSV file upload
- **CORS Enabled**: Ready for integration with frontend applications
- **Production Ready**: Uses FastAPI for async request handling

## Prerequisites

- Python 3.8+
- The following dependencies (see requirements):
  - `fastapi` - Web framework
  - `torch` - PyTorch deep learning framework
  - `pandas` - Data handling
  - `joblib` - Model serialization
  - `shap` - Model explainability
  - `uvicorn` - ASGI server (for running the app)

## Installation

1. Install required dependencies:

```bash
pip install fastapi uvicorn torch pandas joblib shap
```

2. Ensure model files are in the correct location:
   - `../model/model_weights.pth` - Pre-trained model weights
   - `../model/scaler.joblib` - Feature scaler for preprocessing

3. Ensure training data is available:
   - `insider_threat_clean_dataset.csv` - Used for SHAP background samples

## Running the Server

Start the server with:

```bash
python -m uvicorn main:app --reload
```

Or with custom host/port:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Options:

- `--reload` - Auto-restart on code changes (development only)
- `--host 0.0.0.0` - Listen on all network interfaces
- `--port 8000` - Server port (default: 8000)

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check

**GET** `/ping`

Returns a simple health check response.

```bash
curl http://localhost:8000/ping
```

**Response:**

```json
{ "message": "pong" }
```

### 2. Predict Insider Threats

**POST** `/predict`

Upload a CSV file with employee behavior data to get threat predictions and SHAP explanations.

**Request:**

```bash
curl -X POST -F "file=@data.csv" http://localhost:8000/predict
```

**CSV Format:**
The CSV must contain these columns:

- `total_files_burned`
- `burned_from_other`
- `num_printed_pages_off_hours`
- `total_printed_pages`
- `num_unique_campus`
- `hostility_country_level`
- `entry_during_weekend`
- `num_entries`

**Response:**

```json
{
  "results": [
    {
      "row_index": 0,
      "prediction_prob": 0.85,
      "is_malicious": true,
      "feature_contributions": {
        "total_files_burned": 0.42,
        "burned_from_other": 0.28,
        "num_printed_pages_off_hours": 0.12,
        ...
      }
    }
  ]
}
```

**Response Fields:**

- `row_index`: Index of the row in the input CSV
- `prediction_prob`: Probability score (0-1) of being a threat
- `is_malicious`: Boolean flag (true if probability > 0.7)
- `feature_contributions`: SHAP values showing each feature's impact on the prediction

## Example Usage

1. **Test with sample data:**

```bash
# Using the test dataset
curl -X POST -F "file=@insider_threat_clean_dataset_test.csv" http://localhost:8000/predict
```

2. **Parse results with Python:**

```python
import requests
import json

with open('insider_threat_clean_dataset_test.csv', 'rb') as f:
    response = requests.post('http://localhost:8000/predict', files={'file': f})
    predictions = response.json()

    for result in predictions['results']:
        print(f"Row {result['row_index']}: {result['is_malicious']} (prob: {result['prediction_prob']:.2f})")
        print(f"  Top contributing features: {sorted(result['feature_contributions'].items(), key=lambda x: abs(x[1]), reverse=True)[:3]}")
```

## Model Architecture

The insider threat detection model is a 3-layer deep neural network:

- **Input Layer**: 8 features (employee behavioral data)
- **Hidden Layers**: 64 neurons with ReLU activation (2 layers)
- **Output Layer**: 1 neuron with sigmoid activation (binary classification)

## Architecture Notes

- The model is set to `eval()` mode for inference (no dropout/batch norm effects)
- Feature scaling is applied using a pre-fitted scaler
- PyTorch runs on CPU for compatibility
- SHAP uses 100 background samples from the training data

## Troubleshooting

**"No such file or directory" errors:**

- Ensure model files exist at `../model/model_weights.pth` and `../model/scaler.joblib`
- Ensure `insider_threat_clean_dataset.csv` exists in the backend directory

**CORS errors:**

- CORS is enabled for all origins (`allow_origins=["*"]`)
- Adjust as needed for production security

**Port already in use:**

```bash
python -m uvicorn main:app --port 8001
```

**Dependencies not found:**

```bash
pip install --upgrade fastapi uvicorn torch pandas joblib shap
```

## Files

- `main.py` - FastAPI application with model loading and API endpoints
- `ThreatModels.py` - PyTorch neural network model architecture
- `insider_threat_clean_dataset.csv` - Training data (used for SHAP background)
- `insider_threat_clean_dataset_test.csv` - Test data for predictions
