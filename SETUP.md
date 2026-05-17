# Insider Threat Detection System - Setup & Running Guide

This guide provides step-by-step instructions to set up and run both the backend API and frontend web application for the Insider Threat Detection system.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Services](#running-the-services)
6. [Verification & Testing](#verification--testing)
7. [Ports & Access](#ports--access)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Insider Threat Detection system consists of two services:

- **Backend**: FastAPI-based REST API that performs threat predictions and provides SHAP-based explainability
- **Frontend**: Svelte/SvelteKit web application for uploading CSV datasets and viewing threat analysis results

Both services must run simultaneously for the full application to function.

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8 or higher** — [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher** — [Download Node.js](https://nodejs.org/)
- **npm** — Usually installed with Node.js; verify with `npm --version`
- **Git** (optional, for cloning the repository)

### Verify Installation

```bash
python --version
node --version
npm --version
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create a Python Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- `fastapi` — Web framework for the REST API
- `uvicorn` — ASGI server to run the FastAPI app
- `torch` — PyTorch deep learning framework for the neural network
- `pandas` — Data manipulation and CSV handling
- `joblib` — Serialized model and scaler loading
- `shap` — Model explainability library

### Step 4: Verify Model Files

Ensure the following files exist in the `model/` directory (relative to the project root):

```
model/
├── model_weights.pth      ✓ Pre-trained model weights
├── scaler.joblib          ✓ Feature scaler for preprocessing
└── insider_threat_clean_dataset.csv  (used for SHAP background)
```

If these files are missing, the backend will fail to start.

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

From the project root (or a new terminal):

```bash
cd frontend
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

This will install all packages defined in `package.json`, including:

- Svelte 5.51.0
- SvelteKit 2.50.2
- Vite 7.3.1
- Tailwind CSS 4.1.18
- TypeScript 5.9.3

### Step 3: Verify Installation

```bash
npm run build
```

This will build the frontend to ensure all dependencies are correctly installed. The `build/` folder will be created.

---

## Running the Services

You **must run both services simultaneously** in separate terminal windows/tabs.

### Terminal 1: Start the Backend

From the `backend/` directory:

```bash
# If using a virtual environment, activate it first (Windows)
venv\Scripts\activate

# Then start the API server
python -m uvicorn main:app --reload
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

The `--reload` flag enables hot-reloading for development. Remove it for production.

### Terminal 2: Start the Frontend

From the `frontend/` directory:

```bash
npm run dev
```

**Expected output:**

```
VITE v7.3.1 ready in 100 ms

➜  Local:   http://localhost:5173/
```

### Services are Ready!

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000

---

## Verification & Testing

### 1. Check Backend Health

Open a browser or use `curl`:

```bash
curl http://127.0.0.1:8000/ping
```

**Expected response:**

```json
{ "message": "pong" }
```

### 2. Access Frontend

Open a browser and navigate to:

```
http://localhost:5173
```

You should see the Insider Threat Detection upload interface.
