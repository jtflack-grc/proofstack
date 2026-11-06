import pytest

from proofstack.providers import google_vertex


class FakeResponse:
    text = '{"label":"SUPPORTED","rationale":"grounded","cited_excerpt":"MFA enrolled: 4"}'


class FakeModels:
    def __init__(self):
        self.kwargs = None

    def generate_content(self, **kwargs):
        self.kwargs = kwargs
        return FakeResponse()


class FakeClient:
    def __init__(self, **kwargs):
        self.init_kwargs = kwargs
        self.models = FakeModels()


def test_vertex_requires_project(monkeypatch):
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    monkeypatch.setenv("VERTEX_MODEL", "test-model")

    with pytest.raises(RuntimeError, match="GOOGLE_CLOUD_PROJECT"):
        google_vertex.GoogleVertexProvider()


def test_vertex_requires_model(monkeypatch):
    monkeypatch.setenv("GCP_PROJECT_ID", "proofstack-test")
    monkeypatch.delenv("VERTEX_MODEL", raising=False)

    with pytest.raises(RuntimeError, match="VERTEX_MODEL"):
        google_vertex.GoogleVertexProvider()


def test_vertex_uses_adc_project_location_and_model(monkeypatch):
    created = {}

    def fake_client(**kwargs):
        created["client"] = FakeClient(**kwargs)
        return created["client"]

    monkeypatch.setenv("GCP_PROJECT_ID", "proofstack-test")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "global")
    monkeypatch.setenv("VERTEX_MODEL", "test-model")
    monkeypatch.setattr(google_vertex.genai, "Client", fake_client)

    provider = google_vertex.GoogleVertexProvider()
    raw = provider.assess(
        {"question": "MFA?", "claim": "All privileged accounts use MFA."},
        {"title": "Export", "artifact_type": "system_export"},
        "MFA enrolled: 4",
    )

    assert '"label":"SUPPORTED"' in raw
    assert created["client"].init_kwargs == {
        "vertexai": True,
        "project": "proofstack-test",
        "location": "global",
    }
    assert created["client"].models.kwargs["model"] == "test-model"


def test_vertex_empty_response_is_rejected(monkeypatch):
    class EmptyModels:
        def generate_content(self, **kwargs):
            return type("Response", (), {"text": ""})()

    class EmptyClient:
        models = EmptyModels()

    monkeypatch.setenv("GCP_PROJECT_ID", "proofstack-test")
    monkeypatch.setenv("VERTEX_MODEL", "test-model")
    monkeypatch.setattr(
        google_vertex.genai,
        "Client",
        lambda **kwargs: EmptyClient(),
    )

    provider = google_vertex.GoogleVertexProvider()
    with pytest.raises(RuntimeError, match="empty text response"):
        provider.assess(
            {"question": "MFA?", "claim": "All privileged accounts use MFA."},
            {"title": "Export", "artifact_type": "system_export"},
            "MFA enrolled: 4",
        )
