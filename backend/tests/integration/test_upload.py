from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config import settings


def test_upload_returns_success_filename_counts_and_bounded_preview(
    valid_csv_bytes,
):
    client = TestClient(app)

    response = client.post(
        "/upload",
        files={"file": ("transactions.csv", valid_csv_bytes, "text/csv")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["filename"] == "transactions.csv"
    assert body["columns"] == ["date", "description", "amount", "category"]
    assert body["summary"] == {
        "input_rows": 2,
        "blank_rows_removed": 0,
        "duplicates_removed": 0,
        "output_rows": 2,
        "preview_rows": 2,
    }
    assert len(body["preview"]) == body["summary"]["preview_rows"]


def test_upload_returns_structured_invalid_row_errors(malformed_rows_csv_bytes):
    response = TestClient(app).post(
        "/upload",
        files={"file": ("invalid.csv", malformed_rows_csv_bytes, "text/csv")},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["code"] == "invalid_rows"
    assert body["errors"][0]["field"] == "date"
    assert body["errors"][0]["row"] == 2
    assert "preview" not in body


def test_upload_rejects_missing_file_and_non_csv():
    client = TestClient(app)

    missing = client.post("/upload")
    unsupported = client.post(
        "/upload", files={"file": ("transactions.txt", b"not csv", "text/plain")}
    )

    assert missing.status_code == 400
    assert missing.json()["code"] == "unsupported_file"
    assert unsupported.status_code == 400
    assert unsupported.json()["code"] == "unsupported_file"


def test_upload_returns_413_when_file_exceeds_limit(valid_csv_bytes):
    original_limit = settings.upload_size_limit
    settings.upload_size_limit = len(valid_csv_bytes) - 1
    try:
        response = TestClient(app).post(
            "/upload",
            files={"file": ("transactions.csv", valid_csv_bytes, "text/csv")},
        )
    finally:
        settings.upload_size_limit = original_limit

    assert response.status_code == 413
    assert response.json()["code"] == "upload_too_large"
