from backend.app.cleaning import CANONICAL_COLUMNS, clean_csv


def test_clean_csv_canonicalizes_headers_and_returns_four_fields():
    csv = (
        b"\xef\xbb\xbf DATE , Description , AMOUNT , CATEGORY , ignored\n"
        b"2026-01-02, Coffee ,-4.50, food ,unused\n"
    )

    result = clean_csv(csv)

    assert result.columns == list(CANONICAL_COLUMNS)
    assert result.summary.input_rows == 1
    assert result.summary.output_rows == 1
    assert [transaction.model_dump() for transaction in result.preview] == [
        {
            "date": "2026-01-02",
            "description": "Coffee",
            "amount": -4.5,
            "category": "Food",
        }
    ]
