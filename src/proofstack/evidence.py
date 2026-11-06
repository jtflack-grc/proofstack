import re


INSTRUCTION_PATTERNS = (
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"system\s+prompt",
    r"developer\s+message",
    r"return\s+supported",
    r"return\s+unsupported",
)


def normalize_text(value: str) -> str:
    """Collapse whitespace for stable citation comparison."""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def citation_is_grounded(cited_excerpt: str, evidence_text: str) -> bool:
    """Return True only when the cited excerpt is actually present in the evidence."""
    excerpt = normalize_text(cited_excerpt)
    evidence = normalize_text(evidence_text)
    if not excerpt or not evidence:
        return False
    return excerpt in evidence


def instruction_like_signals(evidence_text: str) -> list[str]:
    """Identify instruction-like text inside evidence for reviewer visibility."""
    text = str(evidence_text or "")
    hits = []
    for pattern in INSTRUCTION_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            hits.append(pattern)
    return hits
