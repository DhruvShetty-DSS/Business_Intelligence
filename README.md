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



## Tech Stack

### Frontend
| Tech | Purpose |
|---|---|
| **React** | UI framework — builds the dashboard interface |
| **Recharts** | Charting library — renders income/expense trends, category breakdowns |
| **Axios** (or fetch) | Handles HTTP requests to the backend API |
| **shadcn/ui or Mantine** *(optional)* | Pre-built UI components (buttons, cards, upload widgets) for a polished look without custom CSS |

## Backend
| Tech | Purpose |
|---|---|
| **Python** | Core backend language |
| **FastAPI** | Web framework — exposes analysis/prediction logic as REST API endpoints |
| **Uvicorn** | ASGI server that runs the FastAPI app |
| **Pydantic** | Data validation for API request/response models (comes bundled with FastAPI) |

### Data & machine learning
| Tech | Purpose |
|---|---|
| **pandas** | Data cleaning, transformation, and aggregation |
| **NumPy** | Numerical operations underlying pandas/sklearn |
| **scikit-learn** | Simple ML models (e.g. linear regression for forecasting) |
| **Prophet** *(optional alt. to sklearn)* | Time-series forecasting, purpose-built for trend/seasonality prediction |

### Storage
| Tech | Purpose |
|---|---|
| **SQLite** *(optional)* | Lightweight database to persist uploaded datasets between sessions |

### Dev tools
| Tech | Purpose |
|---|---|
| **Git/GitHub** | Version control |
| **npm** | Frontend package management |
| **pip / venv** | Backend package management and environment isolation |

## Backend development

Create and activate a virtual environment, then install the backend
dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Run the backend tests from the repository root:

```powershell
python -m pytest backend\tests
```

Start the API after the application entry point is implemented:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The current MVP backend plan and upload validation scenarios are documented in
[specs/001-data-upload-cleaning/quickstart.md](specs/001-data-upload-cleaning/quickstart.md).
