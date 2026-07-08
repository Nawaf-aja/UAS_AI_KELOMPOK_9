import argparse
import csv
import json
import os
import pickle
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.request import urlopen

import numpy as np

from src.evaluate import classification_report, confusion_matrix_rows
from src.models import MultinomialNaiveBayes, SoftmaxLogisticRegression
from src.preprocessing import preprocess_many
from src.vectorizer import SimpleTfidfVectorizer


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "complaints.csv.zip"
PROCESSED_DATA_PATH = ROOT / "data" / "processed_banking_complaints.csv"
MODEL_PATH = ROOT / "models" / "complaint_topic_model.pkl"
METRICS_PATH = ROOT / "reports" / "metrics.json"
CONFUSION_PATH = ROOT / "reports" / "confusion_matrix.csv"
MAX_ROWS_PER_LABEL = 350
MAX_SCAN_ROWS = 2000000
TARGET_LABELS = {
    "account_closure",
    "account_management",
    "card_dispute",
    "credit_reporting",
    "fees_interest",
    "fraud_scam",
    "loan_mortgage",
    "payment_transfer",
}


def read_simple_dataset(path: Path) -> Tuple[List[str], np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return [row["text"] for row in rows], np.array([row["label"] for row in rows])


def read_api_dataset(api_url: str) -> Tuple[List[str], np.ndarray]:
    with urlopen(api_url, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    rows = payload.get("data", payload if isinstance(payload, list) else [])
    if not rows:
        raise ValueError("Dataset API tidak mengembalikan data. Pastikan endpoint /complaints benar.")

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_DATA_PATH.open("w", encoding="utf-8", newline="") as file:
        fieldnames = ["text", "label", "source_product", "source_sub_product", "source_issue", "source_sub_issue"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})

    return [row["text"] for row in rows], np.array([row["label"] for row in rows])


def read_cfpb_zip_dataset(path: Path) -> Tuple[List[str], np.ndarray]:
    buckets: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    with zipfile.ZipFile(path) as archive:
        csv_name = archive.namelist()[0]
        with archive.open(csv_name) as raw_file:
            text_file = (line.decode("utf-8", errors="replace") for line in raw_file)
            reader = csv.DictReader(text_file)

            for row_number, row in enumerate(reader, start=1):
                narrative = (row.get("Consumer complaint narrative") or "").strip()
                issue = (row.get("Issue") or "").strip()
                sub_issue = (row.get("Sub-issue") or "").strip()
                product = (row.get("Product") or "").strip()
                sub_product = (row.get("Sub-product") or "").strip()
                if not narrative or not issue or len(narrative.split()) < 15:
                    continue
                label = map_cfpb_category(product, sub_product, issue, sub_issue, narrative)
                if not label:
                    continue
                if len(buckets[label]) < MAX_ROWS_PER_LABEL:
                    buckets[label].append(
                        {
                            "text": narrative,
                            "label": label,
                            "source_product": product,
                            "source_sub_product": sub_product,
                            "source_issue": issue,
                            "source_sub_issue": sub_issue,
                        }
                    )
                if all(len(buckets[label]) >= MAX_ROWS_PER_LABEL for label in TARGET_LABELS):
                    break
                if row_number >= MAX_SCAN_ROWS:
                    break

    selected = []
    for label in sorted(buckets):
        selected.extend(buckets[label][:MAX_ROWS_PER_LABEL])

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_DATA_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "label", "source_product", "source_sub_product", "source_issue", "source_sub_issue"],
        )
        writer.writeheader()
        writer.writerows(selected)

    return [row["text"] for row in selected], np.array([row["label"] for row in selected])


def map_cfpb_category(product: str, sub_product: str, issue: str, sub_issue: str, narrative: str) -> str | None:
    metadata = " ".join([product, sub_product, issue, sub_issue]).lower()
    if "fraud" in metadata or "scam" in metadata or "identity theft" in metadata:
        return "fraud_scam"
    if "closing" in metadata or "closed" in metadata or "close" in metadata:
        return "account_closure"
    if "credit reporting" in metadata or "incorrect information" in metadata or "report" in metadata:
        return "credit_reporting"
    if "mortgage" in metadata or "loan" in metadata or "lender" in metadata or "servicer" in metadata:
        return "loan_mortgage"
    if "credit card" in metadata or "debit card" in metadata or "prepaid card" in metadata or "purchase shown" in metadata:
        return "card_dispute"
    if "money transfer" in metadata or "payment" in metadata or "transfer" in metadata or "deposit" in metadata or "withdrawal" in metadata:
        return "payment_transfer"
    if "fee" in metadata or "interest" in metadata or "overdraft" in metadata or "charged" in metadata:
        return "fees_interest"
    if "checking" in metadata or "savings" in metadata or "account" in metadata or "managing an account" in metadata:
        return "account_management"
    return None


def read_dataset(path: Path) -> Tuple[List[str], np.ndarray]:
    api_url = os.getenv("DATA_API_URL", "").strip()
    if api_url:
        return read_api_dataset(api_url)
    if PROCESSED_DATA_PATH.exists():
        return read_simple_dataset(PROCESSED_DATA_PATH)
    if path.suffix == ".zip":
        return read_cfpb_zip_dataset(path)
    return read_simple_dataset(path)


def stratified_split(labels: np.ndarray, test_ratio: float = 0.125, seed: int = 42):
    rng = np.random.default_rng(seed)
    train_indices: List[int] = []
    test_indices: List[int] = []
    for label in sorted(set(labels)):
        indices = np.where(labels == label)[0]
        rng.shuffle(indices)
        test_size = max(1, int(round(len(indices) * test_ratio)))
        test_indices.extend(indices[:test_size].tolist())
        train_indices.extend(indices[test_size:].tolist())
    rng.shuffle(train_indices)
    rng.shuffle(test_indices)
    return np.array(train_indices), np.array(test_indices)


def train_and_evaluate() -> Dict:
    texts, labels = read_dataset(DATA_PATH)
    processed = np.array(preprocess_many(texts))
    train_idx, test_idx = stratified_split(labels)

    vectorizer = SimpleTfidfVectorizer(max_features=1200, min_df=1)
    x_train = vectorizer.fit_transform(processed[train_idx])
    x_test = vectorizer.transform(processed[test_idx])
    y_train = labels[train_idx]
    y_test = labels[test_idx]

    models = {
        "naive_bayes": MultinomialNaiveBayes(alpha=1.0),
        "logistic_regression": SoftmaxLogisticRegression(
            learning_rate=0.45,
            epochs=1000,
            reg_strength=0.001,
        ),
    }

    metrics = {
        "dataset": {
            "source_file": str(DATA_PATH.name),
            "source_api": os.getenv("DATA_API_URL", "").strip() or None,
            "processed_file": str(PROCESSED_DATA_PATH.relative_to(ROOT)),
            "dataset_strategy": "CFPB narratives mapped into balanced banking complaint categories",
            "total_rows": len(texts),
            "train_rows": len(train_idx),
            "test_rows": len(test_idx),
            "labels": sorted(set(labels)),
        },
        "models": {},
    }

    best_name = ""
    best_score = -1.0
    fitted_models = {}
    predictions = {}

    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        report = classification_report(y_test, pred)
        metrics["models"][name] = report
        fitted_models[name] = model
        predictions[name] = pred
        if report["macro_f1"] > best_score:
            best_name = name
            best_score = report["macro_f1"]

    bundle = {
        "vectorizer": vectorizer,
        "models": fitted_models,
        "best_model": best_name,
        "labels": sorted(set(labels)),
        "preprocessing": "case folding, cleaning, stopword removal, optional Sastrawi/fallback stemming",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORTS = METRICS_PATH.parent
    REPORTS.mkdir(parents=True, exist_ok=True)

    with MODEL_PATH.open("wb") as file:
        pickle.dump(bundle, file)

    metrics["best_model"] = best_name
    with METRICS_PATH.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

    rows = confusion_matrix_rows(y_test, predictions[best_name])
    with CONFUSION_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true", help="Print metrics after training")
    args = parser.parse_args()
    metrics = train_and_evaluate()
    if args.print:
        print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
