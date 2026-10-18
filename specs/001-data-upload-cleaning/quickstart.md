# Quickstart: Data Upload and Cleaning

## Prerequisites

- Python 3.11 or newer
- A virtual environment with the backend dependencies installed
- A CSV file with `date`, `description`, and `amount` headers; `category` is
  optional

## Run the API

From the repository root:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The service is available at `http://127.0.0.1:8000`.

## Run tests

```powershell
python -m pytest backend/tests
```

The test suite must cover required-column validation, malformed dates and
amounts, missing-value defaults, category normalization, blank-row handling,
duplicate removal, and the `POST /upload` success and error contracts.

## Validate a successful upload

```powershell
curl.exe -X POST "http://127.0.0.1:8000/upload" `
  -F "file=@sample-transactions.csv"
```

Expected result:

- HTTP 200
- `status` is `success`
- `columns` contains `date`, `description`, `amount`, and `category`
- `summary` reports input, removed, and output row counts
- `preview` contains standardized dates and normalized values

## Validate an invalid upload

Upload a CSV missing `amount` or containing a non-numeric amount:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/upload" `
  -F "file=@invalid-transactions.csv"
```

Expected result:

- HTTP 400
- `status` is `error`
- `errors` identifies the affected column and row when applicable
- No partial dataset is returned as a successful result

The cleaned dataset is not persisted after the request.
