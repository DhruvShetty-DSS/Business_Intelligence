# Tasks: Data Upload and Cleaning

**Input**: Design documents from
[specs/001-data-upload-cleaning](.)

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md),
[research.md](./research.md), [data-model.md](./data-model.md),
[contracts/upload-api.md](./contracts/upload-api.md),
[quickstart.md](./quickstart.md)

**Tests**: Pytest tasks are mandatory for all data-cleaning and validation
functions. API contract tests cover the upload endpoint.

**Organization**: Tasks are grouped by user story so each story can be
implemented and tested independently after the foundational package exists.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it uses different files and has no
  dependency on incomplete work.
- **[Story]**: Maps the task to a user story (`US1`, `US2`, or `US3`).
- Every task names the concrete file or directory it changes.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the minimal Python package and test environment.

- [x] T001 Create the backend package directories and package markers in
  `backend/app/__init__.py`, `backend/tests/unit/`, and
  `backend/tests/integration/`.
- [x] T002 Create the Python dependency manifest in `backend/requirements.txt`
  with FastAPI, Uvicorn, pandas, Pydantic, pytest, and HTTPX test dependencies.
- [x] T003 [P] Add pytest configuration and test discovery settings in
  `backend/pytest.ini`.
- [x] T004 [P] Add a backend development and API startup section to
  `README.md` that links to the feature quickstart.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared typed models, cleaning result structures, and error
mapping before user-story implementation.

**Critical**: Complete this phase before implementing any user story endpoint
or cleaning behavior.

- [x] T005 Define typed transaction, validation-error, cleaning-summary, and
  upload-result models in `backend/app/schemas.py` based on
  `data-model.md` and `contracts/upload-api.md`.
- [x] T006 Define stable validation error codes, canonical output columns, and
  the bounded preview size in `backend/app/cleaning.py`.
- [x] T007 [P] Add shared test fixtures for valid CSV bytes, malformed rows,
  duplicates, blank rows, and optional categories in
  `backend/tests/conftest.py`.
- [x] T008 [P] Add typed application configuration for the upload size limit
  and preview limit in `backend/app/config.py` without introducing persistence
  or user state.

**Checkpoint**: The backend package, typed contracts, and reusable test
fixtures exist; user-story work can proceed.

---

## Phase 3: User Story 1 - Upload a Transaction CSV (Priority: P1) 🎯 MVP

**Goal**: Accept one valid CSV and return a clean-data summary with a bounded
preview.

**Independent Test**: Send a valid CSV to `POST /upload` and verify HTTP 200,
the four canonical columns, standardized transaction values, and accurate
summary counts.

### Tests for User Story 1

> Write these tests first and verify they fail before implementation.

- [x] T009 [P] [US1] Add unit tests for parsing a valid CSV, canonicalizing
  headers, and returning the four output fields in
  `backend/tests/unit/test_cleaning.py`.
- [x] T010 [P] [US1] Add API contract tests for a successful multipart upload,
  filename propagation, summary counts, and bounded preview in
  `backend/tests/integration/test_upload.py`.

### Implementation for User Story 1

- [x] T011 [US1] Implement typed CSV parsing and canonical header mapping in
  `backend/app/cleaning.py`, including UTF-8 BOM handling and extra-column
  exclusion.
- [x] T012 [US1] Implement successful clean-result construction and summary
  counts in `backend/app/cleaning.py` for valid transaction rows.
- [x] T013 [US1] Implement the FastAPI application and multipart `POST /upload`
  route in `backend/app/main.py`, delegating all cleaning work to
  `backend/app/cleaning.py`.
- [x] T014 [US1] Serialize the successful response according to
  `contracts/upload-api.md` using the typed models in
  `backend/app/schemas.py`.

**Checkpoint**: A valid CSV can be uploaded once and produces a correct,
in-memory JSON response without persistence.

---

## Phase 4: User Story 2 - Understand and Correct Invalid Input (Priority: P1)

**Goal**: Reject unusable CSV files with actionable structured errors.

**Independent Test**: Upload fixtures with missing columns, malformed dates,
non-numeric amounts, empty content, unsupported content, and oversized content;
verify the status code, error code, field, and row information.

### Tests for User Story 2

> Write these tests first and verify they fail before implementation.

- [x] T015 [P] [US2] Add unit tests for missing required columns, invalid dates,
  invalid amounts, empty files, no transaction rows, and row-level error
  metadata in `backend/tests/unit/test_cleaning.py`.
- [x] T016 [P] [US2] Add API tests for HTTP 400 invalid-file responses,
  HTTP 413 upload-limit responses, missing multipart files, and the guarantee
  that errors never return partial successful data in
  `backend/tests/integration/test_upload.py`.

### Implementation for User Story 2

- [x] T017 [US2] Implement required-column, empty-file, and unreadable-CSV
  validation in `backend/app/cleaning.py` with actionable error objects.
- [x] T018 [US2] Implement row-level date and numeric-amount validation with
  one-based CSV row numbers in `backend/app/cleaning.py`.
- [x] T019 [US2] Map cleaning validation failures and unsupported uploads to
  the documented JSON error shape and HTTP statuses in `backend/app/main.py`.
- [x] T020 [US2] Enforce the configured upload size limit before parsing and
  return HTTP 413 from `backend/app/main.py` when exceeded.

**Checkpoint**: Invalid uploads fail explicitly, explain what to fix, and
cannot be mistaken for a clean dataset.

---

## Phase 5: User Story 3 - Review Normalized Transaction Data (Priority: P2)

**Goal**: Normalize dates, missing values, categories, blank rows, and exact
duplicates consistently for downstream analysis.

**Independent Test**: Upload a fixture containing mixed valid date formats,
blank descriptions/categories, inconsistent category casing, blank rows, and
duplicates; verify the cleaned preview and all summary counts.

### Tests for User Story 3

> Write these tests first and verify they fail before implementation.

- [ ] T021 [P] [US3] Add unit tests for ISO date normalization, description and
  category defaults, category casing/whitespace normalization, blank-row
  removal, and exact duplicate removal in
  `backend/tests/unit/test_cleaning.py`.
- [ ] T022 [P] [US3] Add an integration test for the complete normalization
  summary and preview through `POST /upload` in
  `backend/tests/integration/test_upload.py`.

### Implementation for User Story 3

- [ ] T023 [US3] Implement unambiguous date parsing and `YYYY-MM-DD`
  formatting in `backend/app/cleaning.py` without guessing ambiguous dates.
- [ ] T024 [US3] Implement trimmed descriptions with the `Unknown description`
  default and optional/blank categories with the `Uncategorized` default in
  `backend/app/cleaning.py`.
- [ ] T025 [US3] Implement deterministic title-case category normalization and
  normalized exact duplicate removal in `backend/app/cleaning.py`.
- [ ] T026 [US3] Track blank rows, duplicate rows, input rows, output rows,
  and preview rows accurately in `backend/app/cleaning.py`.

**Checkpoint**: The returned dataset contains only standardized fields and
consistent values, with transparent cleaning counts.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete MVP and keep the implementation aligned with
the project constitution and quickstart.

- [ ] T027 [P] Add type-checking configuration and resolve type diagnostics for
  `backend/app/cleaning.py`, `backend/app/main.py`, and
  `backend/app/schemas.py`.
- [ ] T028 [P] Add malformed encoding, UTF-8 BOM, extra-column, and upload-size
  regression fixtures in `backend/tests/unit/test_cleaning.py` and
  `backend/tests/integration/test_upload.py`.
- [ ] T029 Run the full backend pytest suite and verify coverage of every
  cleaning requirement with `python -m pytest backend/tests`.
- [ ] T030 Run the API manually against the scenarios in
  `specs/001-data-upload-cleaning/quickstart.md` and correct any contract
  mismatch in `backend/app/main.py` or `backend/app/schemas.py`.
- [ ] T031 Confirm no files are persisted between requests and document any
  remaining frontend handoff notes in `specs/001-data-upload-cleaning/plan.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; T001-T004 can begin immediately.
- **Foundational (Phase 2)**: Depends on Phase 1; T005-T008 establish shared
  contracts and fixtures.
- **User Story 1 (Phase 3)**: Depends on T005-T008 and is the MVP slice.
- **User Story 2 (Phase 4)**: Depends on the shared package and can extend the
  US1 cleaning and route implementation.
- **User Story 3 (Phase 5)**: Depends on the shared package and can extend the
  US1 cleaning pipeline; it should be completed before final validation.
- **Polish (Phase 6)**: Depends on all selected user-story work.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependency on another story.
- **US2 (P1)**: Starts after Foundational; shares the US1 endpoint and
  cleaning pipeline but remains independently testable through invalid fixtures.
- **US3 (P2)**: Starts after Foundational; shares the cleaning pipeline and
  independently verifies normalization behavior.

### Within Each User Story

- Tests MUST be written and shown failing before implementation.
- Pure cleaning behavior MUST be implemented before route integration.
- Typed schemas MUST be updated before response serialization changes.
- Each story MUST pass its independent test criteria before the next story is
  considered complete.

### Parallel Opportunities

- T003, T004, T007, and T008 can run in parallel after directory creation.
- T009 and T010 can run in parallel because they target separate test scopes.
- T015 and T016 can run in parallel.
- T021 and T022 can run in parallel.
- T027 and T028 can run in parallel after all story implementation is complete.
- US2 and US3 test design can proceed in parallel after foundational contracts,
  though implementation changes to the shared cleaning module should be
  sequenced to avoid conflicts.

## Parallel Example: User Story 1

```text
Task T009: Add pure cleaning unit tests in backend/tests/unit/test_cleaning.py
Task T010: Add endpoint contract tests in backend/tests/integration/test_upload.py
```

## Parallel Example: User Story 2

```text
Task T015: Add validation unit tests in backend/tests/unit/test_cleaning.py
Task T016: Add HTTP error contract tests in backend/tests/integration/test_upload.py
```

## Parallel Example: User Story 3

```text
Task T021: Add normalization unit tests in backend/tests/unit/test_cleaning.py
Task T022: Add end-to-end normalization test in backend/tests/integration/test_upload.py
```

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Setup and Foundational phases.
2. Implement the valid CSV path and successful `POST /upload` contract.
3. Run the independent US1 unit and integration tests.
4. Demonstrate one valid upload before expanding scope.

### Incremental Delivery

1. Add US2 invalid-input handling and verify every error is actionable.
2. Add US3 normalization and transparent cleaning counts.
3. Run the complete pytest suite and quickstart scenarios.
4. Defer React dashboard work to its own feature while preserving this API
   contract for the later client.
