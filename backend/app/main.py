"""FastAPI transport for the in-memory CSV cleaning service."""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from .cleaning import CleaningError, clean_csv
from .schemas import UploadErrorResponse

app = FastAPI(title="Business Intelligence Data Upload")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Accept one CSV and return its cleaned summary and bounded preview."""
    try:
        result = clean_csv(await file.read(), file.filename or "upload.csv")
    except CleaningError as exc:
        payload = UploadErrorResponse(
            code=exc.code, message=str(exc), errors=exc.errors
        )
        return JSONResponse(status_code=400, content=payload.model_dump())
    return result.model_dump()
