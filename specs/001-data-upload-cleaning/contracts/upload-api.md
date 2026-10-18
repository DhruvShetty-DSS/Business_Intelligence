# Upload API Contract

## `POST /upload`

Accepts one CSV file using `multipart/form-data`.

### Request

- Content type: `multipart/form-data`
- Form field: `file`
- File type: CSV only
- Maximum size: implementation-configured upload limit; exceeding it is an
  explicit client error

### Success response

- Status: `200 OK`
- Content type: `application/json`

```json
{
  "status": "success",
  "filename": "transactions.csv",
  "summary": {
    "input_rows": 4,
    "blank_rows_removed": 1,
    "duplicates_removed": 1,
    "output_rows": 2,
    "preview_rows": 2
  },
  "columns": ["date", "description", "amount", "category"],
  "preview": [
    {
      "date": "2026-01-02",
      "description": "Coffee",
      "amount": -4.5,
      "category": "Food"
    }
  ]
}
```

The preview is bounded and may contain fewer rows than `output_rows`.

### Error response

- Status: `400 Bad Request` for invalid file content, missing columns, invalid
  row values, empty CSVs, or unsupported file content
- Status: `413 Request Entity Too Large` when the upload exceeds the configured
  size limit
- Content type: `application/json`

```json
{
  "status": "error",
  "code": "invalid_rows",
  "message": "Some transactions contain invalid values.",
  "errors": [
    {
      "code": "invalid_amount",
      "message": "Amount must be numeric.",
      "field": "amount",
      "row": 3
    }
  ]
}
```

Error responses MUST NOT return a partial dataset as successful output.
Additional error codes may include `unsupported_file`, `empty_file`,
`missing_columns`, `invalid_date`, `unreadable_csv`, and `no_transactions`.
