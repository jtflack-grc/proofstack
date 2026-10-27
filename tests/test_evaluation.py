from proofstack.evaluation import classification_metrics

def test_perfect_metrics():
    gold = ["SUPPORTED","UNSUPPORTED","SUPPORTED","UNSUPPORTED"]
    m = classification_metrics(gold, gold)
    assert m["accuracy"] == 1.0
    assert m["macro_f1"] == 1.0
