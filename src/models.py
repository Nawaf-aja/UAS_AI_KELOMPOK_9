from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np


def softmax(scores: np.ndarray) -> np.ndarray:
    scores = scores - np.max(scores, axis=1, keepdims=True)
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)


@dataclass
class PredictionResult:
    labels: List[str]
    probabilities: np.ndarray


class MultinomialNaiveBayes:
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.classes_: np.ndarray | None = None
        self.class_log_prior_: np.ndarray | None = None
        self.feature_log_prob_: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = x.shape[1]
        feature_count = np.zeros((n_classes, n_features), dtype=float)
        class_count = np.zeros(n_classes, dtype=float)

        for idx, label in enumerate(self.classes_):
            rows = x[y == label]
            class_count[idx] = rows.shape[0]
            feature_count[idx, :] = rows.sum(axis=0)

        smoothed = feature_count + self.alpha
        smoothed_sum = smoothed.sum(axis=1, keepdims=True)
        self.feature_log_prob_ = np.log(smoothed / smoothed_sum)
        self.class_log_prior_ = np.log(class_count / class_count.sum())
        return self

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        if self.classes_ is None or self.class_log_prior_ is None or self.feature_log_prob_ is None:
            raise ValueError("Model has not been fitted.")
        scores = x @ self.feature_log_prob_.T + self.class_log_prior_
        return softmax(scores)

    def predict(self, x: np.ndarray) -> np.ndarray:
        probabilities = self.predict_proba(x)
        return self.classes_[np.argmax(probabilities, axis=1)]


class SoftmaxLogisticRegression:
    def __init__(self, learning_rate: float = 0.4, epochs: int = 900, reg_strength: float = 0.001):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.reg_strength = reg_strength
        self.classes_: np.ndarray | None = None
        self.weights_: np.ndarray | None = None
        self.bias_: np.ndarray | None = None
        self.class_to_index_: Dict[str, int] = {}

    def fit(self, x: np.ndarray, y: np.ndarray):
        self.classes_ = np.unique(y)
        self.class_to_index_ = {label: idx for idx, label in enumerate(self.classes_)}
        y_idx = np.array([self.class_to_index_[label] for label in y])
        n_samples, n_features = x.shape
        n_classes = len(self.classes_)

        y_one_hot = np.zeros((n_samples, n_classes), dtype=float)
        y_one_hot[np.arange(n_samples), y_idx] = 1

        rng = np.random.default_rng(42)
        self.weights_ = rng.normal(0, 0.01, size=(n_features, n_classes))
        self.bias_ = np.zeros(n_classes, dtype=float)

        for _ in range(self.epochs):
            scores = x @ self.weights_ + self.bias_
            probabilities = softmax(scores)
            error = probabilities - y_one_hot
            grad_w = (x.T @ error) / n_samples + self.reg_strength * self.weights_
            grad_b = error.mean(axis=0)
            self.weights_ -= self.learning_rate * grad_w
            self.bias_ -= self.learning_rate * grad_b

        return self

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        if self.classes_ is None or self.weights_ is None or self.bias_ is None:
            raise ValueError("Model has not been fitted.")
        return softmax(x @ self.weights_ + self.bias_)

    def predict(self, x: np.ndarray) -> np.ndarray:
        probabilities = self.predict_proba(x)
        return self.classes_[np.argmax(probabilities, axis=1)]
