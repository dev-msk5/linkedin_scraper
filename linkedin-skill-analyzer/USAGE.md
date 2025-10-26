## LinkedIn Skill Analyzer — Quick usage

This document explains the quickest ways to run the project locally and how
to use the frontend and API. It's intentionally compact so you can copy
commands and begin testing quickly.

### What this project provides
- A small Flask backend that serves an API (`/api/skills`) and static frontend files.
- A tiny frontend (in `frontend/`) that calls the API and renders skill frequencies.
- Utilities in `backend/services/` to load sample job data and extract skills.

---

## Quick start (single command, cross-platform)
From the `linkedin-skill-analyzer` folder run:

```powershell
python run.py
```

What this does:
- Creates a `.venv` in the project root if it doesn't exist.
- Installs requirements into the venv if they're not present.
- Runs the backend (which also serves the frontend) at: `http://127.0.0.1:5000`.

Open your browser to `http://127.0.0.1:5000` to view the frontend UI.

### Options
- `python run.py --no-venv` — run using the current Python environment (no venv actions).
- `python run.py --reinstall` — force reinstall requirements into the venv.

---

## Alternative: PowerShell helper (Windows)
If you prefer a PowerShell helper, use `run-dev.ps1` from the project root:

```powershell
.\run-dev.ps1
```

Note: `run-dev.ps1` calls the venv's Python directly and does not require activating
`Activate.ps1`, so it avoids PowerShell execution policy prompts.

---

## Using the frontend with Live Server (optional)
If you want hot-reload for frontend-only changes, you can use the VS Code Live Server
extension. By default the frontend fetches the API at `/api/skills`, so if Live Server
serves the frontend from a different origin you can either:

- Keep the backend running at `http://127.0.0.1:5000` (the backend has CORS enabled).
- Edit `frontend/script.js` to use the full backend URL: `http://127.0.0.1:5000/api/skills`.

Or, run the backend and open the site at `http://127.0.0.1:5000` (recommended for simplicity).

---

## API
- GET `/api/skills?role=<role>` — returns JSON with `role`, `job_count`, and `skills` frequency map.

Example response:

```json
{
  "role": "data scientist",
  "job_count": 1,
  "skills": { "python": 1, "pandas": 1 }
}
```

---

## Frontend usage
1. Open `http://127.0.0.1:5000`.
2. Enter a job title (e.g. `data scientist`) and click Search.
3. Results show matched job count and a list/bar visualization of skills.

---

## Troubleshooting
- "Execution policy" error running `.ps1`: use the Python runner `python run.py` or the one-time bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
```

- If `python run.py` fails because packages are missing, run:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m backend.main
```

- If the frontend fetch fails with CORS: make sure the backend is running and CORS is enabled (it is by default).

---

## Development notes
- Backend app: `backend/main.py` (also serves `frontend/` static files).
- API blueprint: `backend/routes/api.py` — connects services to `/api/skills`.
- Services: `backend/services/job_fetcher.py`, `backend/services/skill_extractor.py`.
- Utilities: `backend/utils/text_cleaner.py` — basic text normalization.

If you want this document expanded (deployment instructions, Docker, tests, etc.),
I can update the file with those sections — tell me which you'd like next.
