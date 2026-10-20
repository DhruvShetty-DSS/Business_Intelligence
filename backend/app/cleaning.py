"""Shared cleaning constants and validation vocabulary.

The transformation functions are implemented in the user-story phases.  This
module owns the contract values they will share.
"""

from typing import Final

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

