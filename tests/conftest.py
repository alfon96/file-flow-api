import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.router import images


@pytest.fixture(autouse=True)
def patch_upload_dir(tmp_path, monkeypatch):
    """Automatically redirect UPLOAD_DIR to a temp folder for all tests."""
    monkeypatch.setattr(images, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(images, "UPLOAD_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)
