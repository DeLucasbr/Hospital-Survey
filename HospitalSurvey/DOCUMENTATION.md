# Hospital Santa Clara – Satisfaction Survey System

Comprehensive documentation for the full-stack application to collect, store and analyze patient satisfaction surveys.

## 1) Overview

- Purpose: Digitize the satisfaction survey, store structured responses, and provide a management dashboard for insights.
- Stack:
  - Backend: FastAPI, SQLAlchemy (SQLite by default; MySQL-ready)
  - Frontend: Jinja2 templates (Bootstrap, Font Awesome), vanilla JS
  - Charts: Chart.js
  - Server: Uvicorn

Key features:
- Dynamic questionnaire (questions and options persisted in DB)
- Form with progress bar and anonymous option
- Survey submission with automatic satisfaction score
- Dashboard with KPIs, charts, recent responses
- “Ver” action to open the full filled form (ficha completa) in a modal

## 2) Project Structure

```
.
├── main.py                     # FastAPI app, models, endpoints
├── templates/
│   ├── base.html               # Base layout
│   ├── survey.html             # Survey page (form)
│   └── dashboard.html          # Dashboard (charts, table)
├── static/                     # Static assets (CSS/JS/img)
├── hospital_satisfaction.db    # SQLite database (local dev default)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build file
├── docker-compose.yml          # Optional: compose for DB/server
├── README.md                   # Quick start
└── DOCUMENTATION.md            # This documentation
```

## 3) Setup & Running Locally

Prerequisites:
- Python 3.11+ (project uses 3.13 in venv snapshot)

Install:
1. Create/activate venv (Windows PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app:
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

Access:
- Survey: http://localhost:8000/
- Dashboard: http://localhost:8000/dashboard

Notes:
- On first start, DB tables are created automatically and questions are seeded (see init_questions in `main.py`).

## 4) Database

ORM: SQLAlchemy

Tables:
- `surveys` (Survey)
  - id, patient_name, is_anonymous, admission_date, discharge_date, observations, created_at, completed, satisfaction_score
- `questions` (Question)
  - id, question_id (e.g., q1_1), section_title, question_text, question_type, section_order, question_order
- `question_options` (QuestionOption)
  - id, question_id (FK to questions.id), option_text, option_value (numeric), option_order
- `survey_responses` (SurveyResponse)
  - id, survey_id (FK), question_id (FK), response_value, response_score

Initialization:
- `init_questions(db)` seeds 5 sections with predefined questions and options (including numeric values for scoring).

## 5) Backend (FastAPI)

Lifecycle:
- `lifespan` hook creates tables and seeds questions at startup.

Static/Template config:
- `app.mount("/static", StaticFiles(directory="static"), name="static")`
- `templates = Jinja2Templates(directory="templates")`

Pages:
- GET `/` → `survey.html`
- GET `/dashboard` → `dashboard.html`

APIs:
- POST `/api/submit-survey`
  - Accepts form data from the survey page.
  - Extracts answers (keys like `q1_1`, `q2_1`, ...), calculates average satisfaction score from selected options.
  - Persists `Survey` + `SurveyResponse` records.
  - Response: `{ status: "success", survey_id }` or error.

- GET `/api/questions`
  - Returns all questions grouped by section with options.
  - Used by the survey page to render dynamic questions (with a built-in fallback list if API fails).

- GET `/api/dashboard-data`
  - Returns metrics for cards and charts:
    - totalSurveys, avgSatisfaction, sectionScores, monthlyTrend (sample), recentSurveys (id, patient/Anônimo, date, score)

- GET `/api/surveys/{survey_id}`
  - Returns full survey details for the "ficha completa" modal on the dashboard:
    - id, patient/isAnonymous, dates, observations, createdAt, satisfactionScore
    - sections: ordered by section/question showing question text, answer and score

## 6) Frontend – Survey (`templates/survey.html`)

Highlights:
- Patient info fields with “Anônimo” checkbox disabling name field.
- Dynamic question rendering from `/api/questions` (fallback included).
- Progress bar updates with color and encouragement messages.
- Submit button enabled only when all questions are answered.
- Submits via `fetch('/api/submit-survey', { method: 'POST', body: FormData })`.
- On success, shows a success modal with option to start a new survey (`resetForm()`).

## 7) Frontend – Dashboard (`templates/dashboard.html`)

Metrics & charts:
- Loads `/api/dashboard-data` on DOMContentLoaded.
- Cards: total surveys, average satisfaction, etc.
- Charts (Chart.js): trend line, distribution donut, section bar chart.

Recent Responses table:
- Server-rendered initial list (for quick first paint) with a “Ver” button per row.
- Client-side refresh (Refresh button) rebuilds rows from `/api/dashboard-data`.

“Ver” – Ficha completa:
- Each row uses `<button data-survey-id="..." onclick="openSurveyDetails(this)">Ver</button>`.
- `openSurveyDetails` fetches `/api/surveys/{id}` and calls `renderSurveyDetails`.
- Modal `#surveyDetailsModal` displays:
  - Paciente/Anônimo, datas, pontuação total, Observações (if any)
  - All sections with each question + answer (score is available in payload if needed)
- HTML is safely assembled with `escapeHtml` for user-entered text.

Important fixes implemented:
- Replaced fragile inline JSON for Observações with data attributes and dedicated handlers.
- Fixed a client-side templating typo that had wrapped the button HTML in backticks (breaking JS execution and charts). Now a proper `<button>` is rendered.

## 8) Running with Docker (optional)

Build & run (example):
```bash
docker build -t hospital-survey .
docker run -p 8000:8000 hospital-survey
```

Or via docker-compose:
```bash
docker compose up --build
```

Note: The project defaults to SQLite (`DATABASE_URL = "sqlite:///./hospital_satisfaction.db"`). For MySQL, adjust `DATABASE_URL` and compose services accordingly.

## 9) Security & Privacy Considerations

- Anonymous option stores `patient_name = NULL` and `is_anonymous = True`.
- No authentication is implemented (intended for internal network; consider adding admin auth for production).
- Escape and encode user-entered content when displaying (implemented for Observações and answers in modal).
- If moving to MySQL/Postgres, use separate credentials and least-privilege access.

## 10) Troubleshooting

- Charts not rendering / “Ver” not working:
  - Hard refresh (Ctrl+F5).
  - Check browser console for JS errors (Chart.js and Bootstrap must be loaded via `base.html`).
  - Ensure `/api/dashboard-data` and `/api/surveys/{id}` return 200.

- DB issues:
  - Delete `hospital_satisfaction.db` for a clean slate (dev only).
  - Verify that the app has write permissions in the project directory.

- Missing Python packages:
  - Reinstall `pip install -r requirements.txt` inside the venv.

## 11) Extensibility & Next Steps

- Add authentication/authorization for dashboard access.
- Export report (PDF/CSV) for a single survey or aggregated data.
- Add pagination/filters for recent responses.
- Add question management UI (create/update questions and options via admin).
- Internationalization (PT/EN) for UI text.

## 12) Changelog (Recent Work)

- Added Observações to dashboard recent surveys payload (server) and UI (client).
- Implemented robust modal handling with data attributes and safe rendering.
- Introduced `/api/surveys/{id}` endpoint to return full survey details.
- Updated dashboard “Ver” action to show the full filled form (ficha completa).
- Fixed client-side templating mistake that broke charts and buttons.


