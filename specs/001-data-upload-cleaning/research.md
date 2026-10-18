# Research: Data Upload and Cleaning

## Decision: Use a multipart FastAPI upload with pandas-backed pure cleaning functions

**Rationale**: The requested API is a file upload, so `multipart/form-data`
maps directly to the client interaction. FastAPI provides explicit request
validation and structured error responses, while pandas supplies reliable CSV
tabular operations for type conversion, normalization, and duplicate removal.
The route will pass file bytes or a file-like object to plain Python functions
and will not contain data-cleaning rules.

**Alternatives considered**:

- Accepting a JSON string containing CSV data: less natural for browser file
  uploads and adds unnecessary client-side encoding work.
- Implementing CSV handling manually with the standard library: possible for a
  tiny parser, but less clear and more error-prone for tabular normalization
  and duplicate handling.

## Decision: Normalize headers before required-column validation

**Rationale**: Trimming whitespace and comparing case-insensitively satisfies
the feature requirement while still rejecting genuinely missing required
columns. The canonical output names remain `date`, `description`, `amount`,
and `category`.

**Alternatives considered**:

- Requiring exact header spelling: simpler internally but rejects common CSV
  exports and violates the stated header tolerance.
- Fuzzy matching arbitrary header names: risks mapping the wrong source field
  and is not needed for the MVP.

## Decision: Reject invalid required values rather than silently drop rows

**Rationale**: A missing or malformed date or amount makes a transaction
  unreliable for later analysis. Returning structured row-level errors makes
  the problem actionable and avoids presenting partial data as complete.
Blank rows are the explicit exception and are excluded with a count.

**Alternatives considered**:

- Drop invalid rows and continue: hides data loss and conflicts with the
  requirement for clear validation errors.
- Coerce invalid values to defaults: creates misleading financial records.

## Decision: Keep processing stateless and return a bounded preview

**Rationale**: The MVP explicitly excludes persistence and multi-file
  management. A summary plus a small preview demonstrates readiness for later
  analysis without making response size depend on the entire uploaded file.
The clean in-memory dataset remains available only during request handling.

**Alternatives considered**:

- Persisting to SQLite: useful later, but outside MVP scope and adds lifecycle
  and cleanup concerns.
- Returning every cleaned row: unnecessary for the preview contract and can
  produce oversized responses.

## Decision: Use explicit ISO dates and deterministic category casing

**Rationale**: ISO `YYYY-MM-DD` is unambiguous and easy for downstream
  analysis. Category values will be trimmed and converted to title case;
  blank or absent categories become `Uncategorized`.

**Alternatives considered**:

- Preserve source date strings: prevents consistent analysis.
- Lowercase categories: consistent but less readable in the dashboard.
- Infer ambiguous day/month dates: risks changing the meaning of transactions.
