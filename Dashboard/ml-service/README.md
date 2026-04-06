# ML Service - Classification API

This folder contains the ML microservice for the analytical pipeline.
It hosts a Flask API that serves predictions using a trained classifier model.

## Folder Structure

ml-service/
├── rf_api.py                  # Flask API
├── artifacts/
│   ├── rf_model.joblib        # Trained classifier model
│   └── model_metadata.json    # Metadata (features, labels)
├── requirements.txt
└── Dockerfile

## API Endpoints

### Health Check
- GET /health
- Response:
```json
{
  "status": "ok",
  "model": "Classifier"
}
```

### Predict
- POST /predict
- Accepts JSON payload (single record or list of records)
- Expected format: 12 numeric features (feat_0 through feat_11)
- Example response:
```json
{
  "predictions": [
    {
      "prediction_code": 0,
      "prediction_label": "class_0",
      "probabilities": {
        "prob_class_0": 0.9,
        "prob_class_1": 0.1
      }
    }
  ],
  "processing_ms": 12.345
}
```

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python rf_api.py
```

3. Service will start on http://0.0.0.0:5000

## Running with Docker

```bash
docker build -t ml-classifier .
docker run -p 5000:5000 ml-classifier
```

## Notes
- Ensure artifacts/ contains rf_model.joblib and model_metadata.json.
- The API automatically uses the features specified in model_metadata.json.
- Core logic removed for IP protection.
