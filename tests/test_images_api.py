import io, base64
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app

client = TestClient(app)
TEST_IMAGE = Path("tests/data/sample.jpg")


def test_upload_image(client):
    with TEST_IMAGE.open("rb") as f:
        response = client.post(
            "/api/v1/images/",
            files={"file": ("sample.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200
    body = response.json()
    assert "id" in body


def test_filter_stack(client):
    # upload first
    with TEST_IMAGE.open("rb") as f:
        resp = client.post("/", files={"file": ("sample.jpg", f, "image/jpeg")})
    image_id = resp.json()["id"]

    # apply filters
    response = client.post(f"/{image_id}/filter-stack")
    assert response.status_code == 200
    data = response.json()

    assert "toaster" in data  # one of your filters

    # decode one filter image and check properties
    img_bytes = io.BytesIO(base64.b64decode(data["toaster"]))
    img = Image.open(img_bytes)
    assert img.format == "JPEG"
    assert img.width > 0
    assert img.height > 0


def test_scale_image(client):
    # upload
    with TEST_IMAGE.open("rb") as f:
        resp = client.post("/", files={"file": ("sample.jpg", f, "image/jpeg")})
    image_id = resp.json()["id"]

    # scale
    response = client.post(f"/{image_id}/scale", json={"factor": 0.5})
    assert response.status_code == 200
    # Depending on your implementation this might return JSON or image
