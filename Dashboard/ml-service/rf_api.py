
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json
import time

app = Flask(__name__)

# Core logic removed for IP protection.
# Feature engineering and model details have been abstracted.

MODEL_PATH = "artifacts/rf_model.joblib"
METADATA_PATH = "artifacts/model_metadata.json"

rf_model = joblib.load(MODEL_PATH)
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

FEATURE_COLUMNS = metadata["feature_columns"]
PREDICTION_MAPPING = {0: "class_0", 1: "class_1"}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "Classifier"})


@app.route("/predict", methods=["POST"])
def predict():
    request_start = time.perf_counter()
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Support either a single record dict OR list of records
    if isinstance(payload, dict):
        records = [payload]
    elif isinstance(payload, list):
        records = payload
    else:
        return jsonify({"error": "Payload must be a JSON object or list of objects"}), 400

    input_df = pd.DataFrame(records)

    missing_cols = [col for col in FEATURE_COLUMNS if col not in input_df.columns]
    if missing_cols:
        return jsonify({
            "error": "Missing required feature columns",
            "missing_columns": missing_cols,
            "required_columns": FEATURE_COLUMNS
        }), 400

    input_df = input_df[FEATURE_COLUMNS]

    pred_codes = rf_model.predict(input_df).astype(int)
    pred_labels = [PREDICTION_MAPPING[int(code)] for code in pred_codes]

    if hasattr(rf_model, "predict_proba"):
        pred_proba = rf_model.predict_proba(input_df)
        probabilities = [
            {"prob_class_0": float(p[0]), "prob_class_1": float(p[1])}
            for p in pred_proba
        ]
    else:
        probabilities = [None] * len(pred_codes)

    response = []
    for i in range(len(pred_codes)):
        response.append({
            "prediction_code": int(pred_codes[i]),
            "prediction_label": pred_labels[i],
            "probabilities": probabilities[i]
        })

    processing_ms = (time.perf_counter() - request_start) * 1000.0
    return jsonify({
        "predictions": response,
        "processing_ms": round(processing_ms, 3)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
