# Business Intelligence Constitution

## Core Principles

### I. Typed and Tested Python
All Python code must use appropriate type annotations and be covered by pytest tests. Changes must preserve type safety and include tests for new or changed behavior.

### II. Simple, Explainable Machine Learning
ML models must remain simple and explainable. Model choices, features, and evaluation criteria must be understandable to project contributors and stakeholders.

### III. Prediction Limitations
Every prediction must clearly show its limitations, including relevant uncertainty, assumptions, known failure modes, and the scope of data or conditions for which it is valid.

### IV. Single-Page React Dashboard
The user interface must be implemented as a single-page React dashboard. User-facing data, model outputs, and limitations should be presented consistently within that dashboard experience.

### V. Simplicity Over Cleverness
Prefer the simplest design that satisfies the requirement. Avoid unnecessary abstraction, indirection, dependencies, and optimization; complexity must be justified by a concrete need.

## Technical Constraints

- Python is the backend and analysis language and must remain typed and pytest-tested.
- ML implementations must favor transparent baselines and interpretable techniques before more complex alternatives.
- Prediction views must expose limitations alongside results rather than hiding them in separate documentation.
- Frontend work must preserve the single-page React dashboard architecture.

## Development Workflow

- New or changed Python behavior requires corresponding pytest coverage.
- Reviews must verify type annotations, test coverage, model explainability, and prediction limitation disclosures where applicable.
- Changes should be validated with the smallest relevant type-checking, test, and build commands before broader validation.
- Any complexity that cannot be avoided must be documented in the implementation or review rationale.

## Governance

This constitution is the governing quality standard for the project. All feature specifications, plans, implementations, and reviews must comply with these principles. Amendments require updating this document, recording the rationale, and reviewing affected specifications and implementation guidance. If a conflict exists, the simplest compliant interpretation takes precedence until the constitution is amended.

**Version**: 1.0.0 | **Ratified**: 2026-10-16 | **Last Amended**: 2026-10-16
