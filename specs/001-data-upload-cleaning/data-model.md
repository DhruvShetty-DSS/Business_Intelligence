# Data Model: Data Upload and Cleaning

## Transaction

The canonical cleaned financial record.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `date` | string | yes | Unambiguous input; output format `YYYY-MM-DD` |
| `description` | string | yes | Trimmed; blank values become `Unknown description` |
| `amount` | number | yes | Numeric; sign is preserved |
| `category` | string | yes | Trimmed title case; blank/absent becomes `Uncategorized` |

## ValidationError

An actionable issue that prevents a reliable clean dataset.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `code` | string | yes | Stable machine-readable error category |
| `message` | string | yes | Human-readable remediation guidance |
| `field` | string or null | no | Source field when applicable |
| `row` | integer or null | no | One-based CSV data row when applicable |

## CleaningSummary

Counts and status for the upload attempt.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `input_rows` | integer | yes | Rows read after header parsing |
| `blank_rows_removed` | integer | yes | Fully blank rows excluded |
| `duplicates_removed` | integer | yes | Exact duplicates removed after normalization |
| `output_rows` | integer | yes | Number of returned clean transactions |
| `preview_rows` | integer | yes | Number of rows included in the response preview |

## UploadResult

Successful response containing the summary and preview.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `status` | string | yes | `success` |
| `filename` | string | yes | Original filename for user feedback |
| `summary` | CleaningSummary | yes | Counts for this request |
| `columns` | list[string] | yes | Exactly the four canonical fields |
| `preview` | list[Transaction] | yes | Bounded clean-data preview |

## State transitions

`received` -> `validated` -> `cleaned` -> `returned`

Any unsupported file, unreadable CSV, missing required column, or invalid
required value transitions the request to `rejected` and returns an error.
There is no persisted dataset state.
