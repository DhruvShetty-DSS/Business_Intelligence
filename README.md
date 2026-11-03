# Business_Intelligence

## Business Intelligence Tool

A data-driven Business Intelligence tool that transforms raw business data into meaningful insights through interactive dashboards, visualizations, and analytics. It helps users explore trends, identify patterns, monitor key performance indicators (KPIs), and support data-driven decision-making.

## Workflow




Data Upload
     ↓
Data Preprocessing
     ↓
Data Analysis & KPI Calculation
     ↓
Interactive Dashboard
     ↓
AI-Powered Insights & Anomaly Detection
     ↓
Predictive Analytics & Forecasting
     ↓
Business Recommendations

## Status

Feature 001 (data upload and cleaning) is in progress:

- Setup: done
- Foundational: done
- Phase 3 — upload endpoint: done

Planned MVP features:

- [ ] 001 Data upload and cleaning (in progress)
- [ ] 002 Analysis and KPIs
- [ ] 003 Forecast and suggestions
- [ ] 004 React dashboard

## Tech stack

| Technology | Used for |
|---|---|
| FastAPI | Defines the backend API and `POST /upload` endpoint |
| Uvicorn | Runs the FastAPI application server |
| pandas | Parses and cleans uploaded CSV data |
| Pydantic | Defines typed upload response and validation models |
| python-multipart | Parses multipart file uploads |
| pytest | Runs the backend test suite |
| HTTPX | Provides the HTTP client used by API tests |
| scikit-learn | **Planned** for future forecasting and machine-learning features |
| React | **Planned** for the dashboard frontend |
| Recharts | **Planned** for dashboard charts |

## Project structure

```text
backend/   FastAPI application, CSV cleaning code, requirements, and tests
specs/     Feature specifications, plans, contracts, and task tracking
.specify/  GitHub Spec Kit configuration, workflows, templates, and constitution
.github/   Spec Kit agents and skills used during development
```

## Getting started

From the project root, create and activate the backend virtual environment:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd ..
```

Run the tests from the project root:

```powershell
python -m pytest
```

Start the server from the project root:

```powershell
uvicorn backend.app.main:app --reload
```

Open the interactive API documentation at
<http://127.0.0.1:8000/docs>.

## API

### `POST /upload`

Uploads one CSV file using the multipart form field `file`. The CSV must
contain these required columns:

- `date`
- `description`
- `amount`

The `category` column is optional. A successful response includes the cleaned
canonical columns, row counts, and a bounded preview:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/upload" `
  -F "file=@sample-transactions.csv"
```

Sample success response:

```json
{
  "status": "success",
  "filename": "transactions.csv",
  "summary": {
    "input_rows": 2,
    "blank_rows_removed": 0,
    "duplicates_removed": 0,
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
    },
    {
      "date": "2026-01-03",
      "description": "Salary",
      "amount": 1000.0,
      "category": "Income"
    }
  ]
}
```

## Development approach

The project uses GitHub Spec Kit to guide development through a constitution,
specification, plan, tasks, and implementation workflow. Planning documents
for each feature live in [specs/](specs/).
