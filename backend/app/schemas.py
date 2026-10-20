"""Typed request-independent models for upload and cleaning results."""

from pydantic import BaseModel, ConfigDict, Field


class Transaction(BaseModel):
    """A canonical cleaned transaction."""

    model_config = ConfigDict(extra="forbid")

    date: str
    description: str
    amount: float
    category: str


class ValidationError(BaseModel):
    """An actionable validation issue."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    field: str | None = None
    row: int | None = Field(default=None, ge=1)


class CleaningSummary(BaseModel):
    """Counts describing one cleaning attempt."""

    model_config = ConfigDict(extra="forbid")

    input_rows: int = Field(ge=0)
    blank_rows_removed: int = Field(ge=0)
    duplicates_removed: int = Field(ge=0)
    output_rows: int = Field(ge=0)
    preview_rows: int = Field(ge=0)


class UploadResult(BaseModel):
    """Successful upload response."""

    model_config = ConfigDict(extra="forbid")

    status: str = "success"
    filename: str
    summary: CleaningSummary
    columns: list[str]
    preview: list[Transaction]


class UploadErrorResponse(BaseModel):
    """Structured error response for an unsuccessful upload."""

    model_config = ConfigDict(extra="forbid")

    status: str = "error"
    code: str
    message: str
    errors: list[ValidationError] = Field(default_factory=list)
