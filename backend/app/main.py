"""FastAPI transport for the in-memory CSV cleaning service."""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from .cleaning import CleaningError, ERROR_CODES, clean_csv
from .config import settings
from .schemas import UploadErrorResponse

app = FastAPI(title="Business Intelligence Data Upload")


@app.post("/upload")
async def upload(file: UploadFile | None = File(default=None)):
    """Accept one CSV and return its cleaned summary and bounded preview."""
    if file is None:
        payload = UploadErrorResponse(
            code=ERROR_CODES["UNSUPPORTED_FILE"],
            message="Upload one CSV file using the 'file' field.",
        )
        return JSONResponse(status_code=400, content=payload.model_dump())
    if not file.filename or not file.filename.lower().endswith(".csv"):
        payload = UploadErrorResponse(
            code=ERROR_CODES["UNSUPPORTED_FILE"],
            message="Only CSV files are supported. Upload a .csv file and retry.",
        )
        return JSONResponse(status_code=400, content=payload.model_dump())
    contents = await file.read()
    if len(contents) > settings.upload_size_limit:
        payload = UploadErrorResponse(
            code="upload_too_large",
            message=f"Upload exceeds the {settings.upload_size_limit}-byte limit.",
        )
        return JSONResponse(status_code=413, content=payload.model_dump())
    try:
        result = clean_csv(contents, file.filename)
    except CleaningError as exc:
        payload = UploadErrorResponse(
            code=exc.code, message=str(exc), errors=exc.errors
        )
        return JSONResponse(status_code=400, content=payload.model_dump())
    return result.model_dump()
