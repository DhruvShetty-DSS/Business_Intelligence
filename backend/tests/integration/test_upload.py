from fastapi.testclient import TestClient

from backend.app.main import app


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
