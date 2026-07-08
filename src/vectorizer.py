import math
from collections import Counter
from typing import Dict, Iterable, List

import numpy as np


class SimpleTfidfVectorizer:
    def __init__(self, max_features: int = 1500, min_df: int = 1):
        self.max_features = max_features
        self.min_df = min_df
        self.vocabulary_: Dict[str, int] = {}
        self.idf_: np.ndarray | None = None

    def fit(self, documents: Iterable[str]):
        docs = list(documents)
        df = Counter()
        term_counts = Counter()

        for doc in docs:
            tokens = doc.split()
            term_counts.update(tokens)
            df.update(set(tokens))

        terms = [
            term for term, count in term_counts.most_common()
            if df[term] >= self.min_df
        ][: self.max_features]
        self.vocabulary_ = {term: idx for idx, term in enumerate(terms)}

        n_docs = len(docs)
        idf = []
        for term in terms:
            idf.append(math.log((1 + n_docs) / (1 + df[term])) + 1)
        self.idf_ = np.array(idf, dtype=float)
        return self

    def transform(self, documents: Iterable[str]) -> np.ndarray:
        if self.idf_ is None:
            raise ValueError("Vectorizer has not been fitted.")

        docs = list(documents)
        matrix = np.zeros((len(docs), len(self.vocabulary_)), dtype=float)
        for row, doc in enumerate(docs):
            counts = Counter(doc.split())
            if not counts:
                continue
            total = sum(counts.values())
            for term, count in counts.items():
                col = self.vocabulary_.get(term)
                if col is not None:
                    matrix[row, col] = (count / total) * self.idf_[col]

        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return matrix / norms

    def fit_transform(self, documents: Iterable[str]) -> np.ndarray:
        return self.fit(documents).transform(documents)

    def top_terms(self, limit: int = 30) -> List[str]:
        ordered = sorted(self.vocabulary_.items(), key=lambda item: item[1])
        return [term for term, _ in ordered[:limit]]
