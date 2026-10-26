"""CSV parsing and deterministic transaction cleaning."""

from io import BytesIO
from typing import Final

import pandas as pd

from .schemas import CleaningSummary, Transaction, UploadResult, ValidationError

CANONICAL_COLUMNS: Final[tuple[str, ...]] = (
    "date",
    "description",
    "amount",
    "category",
)
REQUIRED_COLUMNS: Final[tuple[str, ...]] = ("date", "description", "amount")
PREVIEW_LIMIT: Final[int] = 100

ERROR_CODES: Final[dict[str, str]] = {
    "UNSUPPORTED_FILE": "unsupported_file",
    "EMPTY_FILE": "empty_file",
    "UNREADABLE_CSV": "unreadable_csv",
    "MISSING_COLUMNS": "missing_columns",
    "INVALID_ROWS": "invalid_rows",
    "INVALID_DATE": "invalid_date",
    "INVALID_AMOUNT": "invalid_amount",
    "NO_TRANSACTIONS": "no_transactions",
}


class CleaningError(ValueError):
    """A request cannot be converted into a reliable clean dataset."""

    def __init__(
        self, code: str, message: str, errors: list[ValidationError] | None = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.errors = errors or []


def _error(code: str, message: str, field: str | None = None, row: int | None = None):
    return ValidationError(code=code, message=message, field=field, row=row)


def _canonicalize_headers(frame: pd.DataFrame) -> pd.DataFrame:
    mapping: dict[str, str] = {}
    for column in frame.columns:
        normalized = str(column).strip().lstrip("\ufeff").lower()
        if normalized in CANONICAL_COLUMNS and normalized not in mapping:
            mapping[normalized] = column

    missing = [column for column in REQUIRED_COLUMNS if column not in mapping]
    if missing:
        raise CleaningError(
            ERROR_CODES["MISSING_COLUMNS"],
            f"Missing required columns: {', '.join(missing)}.",
            [
                _error(
                    ERROR_CODES["MISSING_COLUMNS"],
                    "Required column is missing.",
                    missing_column,
                )
                for missing_column in missing
            ],
        )

    selected = {canonical: mapping[canonical] for canonical in mapping}
    result = frame[[source for source in selected.values()]].rename(
        columns={source: canonical for canonical, source in selected.items()}
    )
    if "category" not in result:
        result["category"] = ""
    return result.loc[:, list(CANONICAL_COLUMNS)]


def clean_csv(csv_bytes: bytes, filename: str = "upload.csv") -> UploadResult:
    """Parse, normalize, deduplicate, and summarize one CSV upload."""
    if not csv_bytes:
        raise CleaningError(ERROR_CODES["EMPTY_FILE"], "The uploaded CSV is empty.")
    try:
        frame = pd.read_csv(
            BytesIO(csv_bytes),
            dtype=str,
            encoding="utf-8-sig",
            keep_default_na=False,
            skip_blank_lines=False,
        )
    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        ValueError,
    ) as exc:
        raise CleaningError(
            ERROR_CODES["UNREADABLE_CSV"], "The uploaded file is not a readable CSV."
        ) from exc

    input_rows = len(frame)
    frame = _canonicalize_headers(frame)
    blank_mask = frame.apply(lambda row: all(not str(value).strip() for value in row), axis=1)
    blank_rows_removed = int(blank_mask.sum())
    frame = frame.loc[~blank_mask].copy()
    if frame.empty:
        raise CleaningError(
            ERROR_CODES["NO_TRANSACTIONS"], "The CSV contains no transactions."
        )

    frame["date"] = pd.to_datetime(frame["date"].str.strip(), errors="coerce").dt.strftime(
        "%Y-%m-%d"
    )
    frame["description"] = frame["description"].map(
        lambda value: str(value).strip() or "Unknown description"
    )
    frame["amount"] = pd.to_numeric(frame["amount"].str.strip(), errors="coerce")
    frame["category"] = frame["category"].map(
        lambda value: str(value).strip().title() or "Uncategorized"
    )

    errors: list[ValidationError] = []
    for index, row in frame.iterrows():
        csv_row = int(index) + 2
        if pd.isna(row["date"]):
            errors.append(_error(ERROR_CODES["INVALID_DATE"], "Date must be valid.", "date", csv_row))
        if pd.isna(row["amount"]):
            errors.append(
                _error(ERROR_CODES["INVALID_AMOUNT"], "Amount must be numeric.", "amount", csv_row)
            )
    if errors:
        raise CleaningError(ERROR_CODES["INVALID_ROWS"], "Some transactions contain invalid values.", errors)

    before_dedup = len(frame)
    frame = frame.drop_duplicates(ignore_index=True)
    transactions = [
        Transaction(
            date=row["date"],
            description=row["description"],
            amount=float(row["amount"]),
            category=row["category"],
        )
        for row in frame.to_dict(orient="records")
    ]
    summary = CleaningSummary(
        input_rows=input_rows,
        blank_rows_removed=blank_rows_removed,
        duplicates_removed=before_dedup - len(transactions),
        output_rows=len(transactions),
        preview_rows=min(len(transactions), PREVIEW_LIMIT),
    )
    return UploadResult(
        filename=filename,
        summary=summary,
        columns=list(CANONICAL_COLUMNS),
        preview=transactions[:PREVIEW_LIMIT],
    )
