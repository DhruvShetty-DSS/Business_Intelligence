<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles: I. Typed and Tested Python -> I. Typed, Tested Python Analysis;
  II. Simple, Explainable Machine Learning -> II. Simple and Explainable Models;
  III. Prediction Limitations -> III. Visible Prediction Limitations;
  IV. Single-Page React Dashboard -> V. Single-Page React Dashboard;
  V. Simplicity Over Cleverness -> I, II, and VI
- Added principles: IV. API-Independent Backend Logic; VI. Incremental MVP Delivery
- Added sections: Technical Constraints; Development Workflow
- Removed sections: none
- Templates requiring updates: .specify/templates/plan-template.md (updated);
  .specify/templates/tasks-template.md (updated); .specify/templates/spec-template.md
  (no update required)
- Follow-up TODOs: none
-->

# Business Intelligence Constitution

## Core Principles

### I. Typed, Tested Python Analysis
All Python code MUST use appropriate type hints. Data cleaning and analysis
functions MUST have pytest coverage, and new or changed behavior MUST include
tests before it is considered complete. This keeps the analytical foundation
safe to change and makes the student project reproducible.

### II. Simple and Explainable Models
The project MUST prefer simple, explainable machine-learning models over
complex models when both satisfy the requirement. Features, assumptions,
training data, and evaluation results MUST be understandable to contributors
and users. More complex modeling requires a documented, measurable benefit.

### III. Visible Prediction Limitations
Every prediction shown to a user MUST include a nearby note describing its
limitations, relevant assumptions, uncertainty where available, and the
conditions under which it may fail. The interface MUST NOT present predictions
as guarantees.

### IV. API-Independent Backend Logic
Data cleaning, analysis, and prediction behavior MUST live in plain Python
functions independent of FastAPI routes, request objects, and response
serialization. The API layer MUST adapt validated inputs and outputs rather
than contain analytical logic. This separation keeps core behavior directly
testable and reusable.

### V. Single-Page React Dashboard
The UI MUST be a single-page React dashboard. It MUST provide explicit
loading and error states for asynchronous work, and it MUST present analysis
results, predictions, and their limitations within the dashboard experience.

### VI. Incremental Minimal MVP
Development MUST proceed in small, testable increments. The MVP MUST contain
only the smallest scope that demonstrates the core finance-analysis workflow.
New abstractions, dependencies, and features MUST be justified by a concrete
requirement or validated user need.

## Technical Constraints

- The backend MUST use Python with FastAPI, pandas, and scikit-learn as
  appropriate to the feature, while keeping analytical functions independent
  of the API layer.
- Python data-cleaning and analysis functions MUST be typed and tested with
  pytest.
- Model outputs MUST expose limitations in the React dashboard alongside the
  corresponding prediction.
- Frontend work MUST preserve the single-page React dashboard architecture
  and its loading and error states.

## Development Workflow

- Each increment MUST have a clear, independently testable outcome.
- Reviews MUST verify type hints, pytest coverage for affected data-cleaning
  and analysis functions, model explainability, prediction limitation
  disclosures, API-independent backend logic, and UI loading/error states
  where applicable.
- Changes MUST be validated with the smallest relevant pytest, type-checking,
  and frontend build or test commands before broader validation.
- Any complexity that cannot be avoided MUST be documented with the concrete
  requirement or measurable benefit that justifies it.

## Governance

This constitution is the governing quality standard for the project. All
feature specifications, plans, implementations, and reviews MUST comply with
these principles. Amendments MUST update this document, record the rationale,
increment the semantic version, and review affected templates and guidance.
The ratification date remains the original adoption date; the last-amended
date changes whenever the constitution changes. If a conflict exists, the
simplest compliant interpretation takes precedence until the constitution is
amended.

**Version**: 1.1.0 | **Ratified**: 2026-10-16 | **Last Amended**: 2026-10-18
