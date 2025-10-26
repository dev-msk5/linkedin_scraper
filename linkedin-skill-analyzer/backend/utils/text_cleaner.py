"""Simple text cleaning helpers used by the backend services.

Provides small, dependency-free utilities for lowercasing, removing
punctuation, and filtering stopwords. These are intentionally simple
helpers suitable for unit tests and early prototyping. For production
use, consider using `nltk` or `spaCy` for tokenization/normalization.
"""
from __future__ import annotations

import re
from typing import Iterable, List, Set


# A small default English stopword set. Kept intentionally compact so the
# module does not require external downloads. You can pass a larger set
# to `remove_stopwords` if desired.
DEFAULT_STOPWORDS: Set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


# Use a conservative fallback regex to strip punctuation (non-word, non-space chars).
_FALLBACK_PUNCT_RE = re.compile(r"[^\w\s]", flags=re.UNICODE)


def to_lower(text: str) -> str:
    """Return lowercased text (handles None-like inputs via str())."""
    return str(text).lower()


def remove_punctuation(text: str) -> str:
    """Remove punctuation characters from text and collapse whitespace.

    This uses a conservative fallback regex to strip any character that is
    not a word character or whitespace. It leaves numbers and underscores.
    """
    if text is None:
        return ""
    # Use the fallback regex which removes anything that's not a word character
    # or whitespace. This is simple and avoids reliance on non-portable regex
    # escapes such as \p{P} which aren't supported by Python's `re`.
    cleaned = _FALLBACK_PUNCT_RE.sub("", text)

    # Collapse multiple whitespace characters to a single space and strip
    return re.sub(r"\s+", " ", cleaned).strip()


def remove_stopwords(tokens: Iterable[str], stopwords: Set[str] | None = None) -> List[str]:
    """Filter out stopwords from a sequence of tokens.

    Args:
        tokens: Iterable of token strings (assumed to be lowercased already).
        stopwords: Optional set of stopwords. If None, uses DEFAULT_STOPWORDS.

    Returns:
        List of tokens with stopwords removed, preserving order.
    """
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS

    return [t for t in tokens if t and t not in stopwords]


def clean_text(text: str, stopwords: Set[str] | None = None) -> List[str]:
    """Full cleaning pipeline returning list of tokens.

    Steps:
      1. Lowercase
      2. Remove punctuation
      3. Split on whitespace
      4. Remove stopwords

    Returns a list of remaining tokens.
    """
    if not text:
        return []

    lower = to_lower(text)
    no_punct = remove_punctuation(lower)
    tokens = no_punct.split()
    return remove_stopwords(tokens, stopwords=stopwords)


if __name__ == "__main__":
    sample = "We're looking for a Data Scientist with experience in Python, pandas, and SQL."
    print("Original:", sample)
    print("Lower:", to_lower(sample))
    print("No punctuation:", remove_punctuation(to_lower(sample)))
    print("Clean tokens:", clean_text(sample))
