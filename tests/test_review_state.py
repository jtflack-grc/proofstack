from proofstack.review_state import assessment_matches_case


def test_assessment_matches_current_case():
    context = {"question_id": "Q01", "evidence_id": "E01"}
    assert assessment_matches_case(context, "Q01", "E01")


def test_assessment_rejected_for_different_evidence():
    context = {"question_id": "Q01", "evidence_id": "E01"}
    assert not assessment_matches_case(context, "Q01", "E02")


def test_assessment_rejected_for_different_question():
    context = {"question_id": "Q01", "evidence_id": "E01"}
    assert not assessment_matches_case(context, "Q02", "E01")


def test_assessment_rejected_without_context():
    assert not assessment_matches_case(None, "Q01", "E01")
