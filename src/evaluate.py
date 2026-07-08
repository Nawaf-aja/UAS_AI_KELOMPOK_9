from collections import defaultdict
from typing import Dict, List

import numpy as np


def classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    labels = sorted(set(y_true) | set(y_pred))
    rows: Dict[str, Dict[str, float]] = {}
    precisions: List[float] = []
    recalls: List[float] = []
    f1s: List[float] = []

    for label in labels:
        tp = int(((y_true == label) & (y_pred == label)).sum())
        fp = int(((y_true != label) & (y_pred == label)).sum())
        fn = int(((y_true == label) & (y_pred != label)).sum())
        support = int((y_true == label).sum())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "support": support,
        }
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    accuracy = float((y_true == y_pred).mean()) if len(y_true) else 0.0
    return {
        "accuracy": round(accuracy, 4),
        "macro_precision": round(sum(precisions) / len(precisions), 4),
        "macro_recall": round(sum(recalls) / len(recalls), 4),
        "macro_f1": round(sum(f1s) / len(f1s), 4),
        "per_class": rows,
    }


def confusion_matrix_rows(y_true: np.ndarray, y_pred: np.ndarray) -> List[Dict[str, int | str]]:
    labels = sorted(set(y_true) | set(y_pred))
    counts = defaultdict(int)
    for actual, predicted in zip(y_true, y_pred):
        counts[(actual, predicted)] += 1

    rows: List[Dict[str, int | str]] = []
    for actual in labels:
        row: Dict[str, int | str] = {"actual": actual}
        for predicted in labels:
            row[predicted] = counts[(actual, predicted)]
        rows.append(row)
    return rows
