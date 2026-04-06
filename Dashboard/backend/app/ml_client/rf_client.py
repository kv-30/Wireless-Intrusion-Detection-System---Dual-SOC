# backend/app/ml_client/rf_client.py
import logging

logger = logging.getLogger(__name__)

# Core logic removed for IP protection.
# ML endpoint orchestration and fallback detection have been replaced with a public-safe stub.

def get_rf_prediction(features):
    logger.info("ML prediction stub active. Returning default normal prediction.")
    return {
        "prediction_code": 0,
        "prediction_label": "normal",
        "probabilities": {
            "prob_normal": 1.0,
            "prob_attack": 0.0,
        },
        "source": "stubbed_ml",
    }
