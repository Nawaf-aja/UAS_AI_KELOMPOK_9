import re
from typing import Iterable, List

STOPWORDS = {
    "ada", "agar", "akan", "aku", "anda", "atau", "bagai", "bagi", "bahwa",
    "bank", "baru", "belum", "bisa", "dan", "dari", "dengan", "di", "ini",
    "itu", "jika", "karena", "ke", "lagi", "lebih", "maka", "masih", "mau",
    "maupun", "melalui", "meminta", "menjadi", "mereka", "meskipun", "namun",
    "pada", "padahal", "saya", "sejak", "sebagai", "setelah", "sudah",
    "supaya", "tanpa", "tapi", "telah", "terlalu", "tetap", "tidak", "untuk",
    "yang",
    "a", "about", "after", "all", "also", "am", "an", "and", "any", "are",
    "as", "at", "be", "been", "being", "but", "by", "can", "could", "did",
    "do", "does", "doing", "for", "from", "had", "has", "have", "having",
    "he", "her", "him", "his", "how", "i", "if", "in", "into", "is", "it",
    "its", "me", "my", "no", "not", "of", "on", "or", "our", "she", "so",
    "than", "that", "the", "their", "them", "then", "there", "these", "they",
    "this", "those", "to", "up", "was", "we", "were", "what", "when",
    "where", "which", "who", "why", "will", "with", "would", "you", "your",
}

SUFFIXES = ("kan", "nya", "lah", "kah", "an", "i")
PREFIXES = ("meng", "meny", "men", "mem", "me", "ber", "ter", "di", "ke", "se", "pe")


def _fallback_stem(token: str) -> str:
    """Small Indonesian stemmer fallback when PySastrawi is unavailable."""
    original = token
    for prefix in PREFIXES:
        if token.startswith(prefix) and len(token) - len(prefix) >= 4:
            token = token[len(prefix):]
            break
    for suffix in SUFFIXES:
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            token = token[: -len(suffix)]
            break
    return token or original


try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

    _STEMMER = StemmerFactory().create_stemmer()

    def stem_token(token: str) -> str:
        return _STEMMER.stem(token)

except Exception:

    def stem_token(token: str) -> str:
        return _fallback_stem(token)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str, use_stemming: bool = True) -> List[str]:
    tokens = normalize_text(text).split()
    tokens = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
    if use_stemming:
        tokens = [stem_token(token) for token in tokens]
    return tokens


def preprocess_text(text: str, use_stemming: bool = True) -> str:
    return " ".join(tokenize(text, use_stemming=use_stemming))


def preprocess_many(texts: Iterable[str], use_stemming: bool = True) -> List[str]:
    return [preprocess_text(text, use_stemming=use_stemming) for text in texts]
