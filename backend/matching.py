"""Finds past incidents that describe the same problem as an alert.

Uses TF-IDF cosine similarity: words shared by the alert and an incident count
more when they are rare across all incidents. It needs no extra packages or
model download, so it cannot fail during a live demo.
"""

import math
import re
from collections import Counter

MATCH_THRESHOLD = 0.35

STOP_WORDS = {
    "a", "after", "above", "an", "and", "at", "by", "during", "for", "from",
    "in", "is", "not", "of", "on", "or", "the", "to", "was", "when", "with",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def tfidf_vector(tokens, idf):
    counts = Counter(tokens)
    return {word: count * idf.get(word, 0.0) for word, count in counts.items()}


def cosine(left, right):
    shared = left.keys() & right.keys()
    dot = sum(left[word] * right[word] for word in shared)
    left_size = math.sqrt(sum(value * value for value in left.values()))
    right_size = math.sqrt(sum(value * value for value in right.values()))
    if not left_size or not right_size:
        return 0.0
    return dot / (left_size * right_size)


def search_past_incidents(alert_text, incidents, threshold=MATCH_THRESHOLD):
    """Returns matching incidents, best first, each with a similarity score."""
    documents = [tokenize(incident["symptom"]) for incident in incidents]
    total = len(documents)
    document_counts = Counter(word for doc in documents for word in set(doc))
    idf = {
        word: math.log((1 + total) / (1 + count)) + 1
        for word, count in document_counts.items()
    }

    alert_vector = tfidf_vector(tokenize(alert_text), idf)
    matches = []
    for incident, document in zip(incidents, documents):
        score = cosine(alert_vector, tfidf_vector(document, idf))
        if score >= threshold:
            matches.append({**incident, "score": round(score, 2)})
    return sorted(matches, key=lambda match: match["score"], reverse=True)
