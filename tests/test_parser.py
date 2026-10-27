from proofstack.parser import parse_model_output

def test_json_supported():
    r = parse_model_output('{"label":"SUPPORTED","rationale":"x","cited_excerpt":"y"}')
    assert r.label == "SUPPORTED"
    assert r.parse_status == "json"

def test_ambiguous_is_unparseable():
    r = parse_model_output("SUPPORTED or UNSUPPORTED")
    assert r.label == "UNPARSEABLE"
