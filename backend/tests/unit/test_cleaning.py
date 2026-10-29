import pytest

from backend.app.cleaning import CANONICAL_COLUMNS, CleaningError, clean_csv


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


@pytest.mark.parametrize(
    ("csv", "code", "field"),
    [
        (b"description,amount\nCoffee,1\n", "missing_columns", "date"),
        (b"date,description,amount\nnot-a-date,Coffee,1\n", "invalid_rows", "date"),
        (b"date,description,amount\n2026-01-01,Coffee,nope\n", "invalid_rows", "amount"),
    ],
)
def test_clean_csv_reports_actionable_validation_errors(csv, code, field):
    with pytest.raises(CleaningError) as raised:
        clean_csv(csv)

    error = raised.value
    assert error.code == code
    assert error.errors[0].field == field
    if code == "invalid_rows":
        assert error.errors[0].row == 2


@pytest.mark.parametrize("csv", [b"", b"date,description,amount\n"])
def test_clean_csv_rejects_empty_or_header_only_files(csv):
    with pytest.raises(CleaningError) as raised:
        clean_csv(csv)

    assert raised.value.code in {"empty_file", "no_transactions"}
