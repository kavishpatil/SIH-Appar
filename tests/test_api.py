import os
import tempfile

# Use a throw-away SQLite DB so tests never touch real data.
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "test.db")

from fastapi.testclient import TestClient  # noqa: E402
from backend.app.main import app  # noqa: E402


def test_health_endpoint():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "healthy"
        assert body["service"] == "aicte-apaar-backend"


def test_swagger_docs_available():
    with TestClient(app) as client:
        assert client.get("/docs").status_code == 200


def test_openapi_lists_api_routes():
    with TestClient(app) as client:
        paths = client.get("/openapi.json").json()["paths"]
        assert any(p.startswith("/api/v1") for p in paths)
