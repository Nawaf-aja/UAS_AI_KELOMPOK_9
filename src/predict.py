import json
import pickle
from pathlib import Path
from typing import Dict

import numpy as np

from src.preprocessing import preprocess_text
from src.recommendations import get_recommendation

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "complaint_topic_model.pkl"


def load_bundle(path: Path = MODEL_PATH) -> Dict:
    if not path.exists():
        from src.train import train_and_evaluate

        train_and_evaluate()
    with path.open("rb") as file:
        return pickle.load(file)


def predict_topic(text: str, model_name: str | None = None) -> Dict:
    if not text or not text.strip():
        return {
            "status": 400,
            "error": "Teks keluhan tidak boleh kosong.",
        }

    bundle = load_bundle()
    selected_model = model_name or bundle["best_model"]
    if selected_model not in bundle["models"]:
        return {
            "status": 400,
            "error": f"Model '{selected_model}' tidak tersedia.",
            "available_models": sorted(bundle["models"].keys()),
        }

    processed = preprocess_text(text)
    x = bundle["vectorizer"].transform([processed])
    model = bundle["models"][selected_model]
    probabilities = model.predict_proba(x)[0]
    order = np.argsort(probabilities)[::-1]
    labels = list(model.classes_)
    top_predictions = [
        {
            "label": labels[idx],
            "confidence": round(float(probabilities[idx]), 4),
        }
        for idx in order[:3]
    ]
    prediction = top_predictions[0]["label"]
    confidence = top_predictions[0]["confidence"]
    return {
        "status": 200,
        "model": selected_model,
        "input": text,
        "processed_text": processed,
        "prediction": prediction,
        "confidence": confidence,
        "top_predictions": top_predictions,
        "recommendation": get_recommendation(prediction, confidence),
    }


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Complaint text to classify")
    parser.add_argument("--model", choices=["naive_bayes", "logistic_regression"], default=None)
    args = parser.parse_args()
    print(json.dumps(predict_topic(args.text, args.model), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
