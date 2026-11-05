def assessment_matches_case(context, question_id: str, evidence_id: str) -> bool:
    """Return True only when an assessment belongs to the selected review case."""
    if not isinstance(context, dict):
        return False
    return (
        context.get("question_id") == question_id
        and context.get("evidence_id") == evidence_id
    )
