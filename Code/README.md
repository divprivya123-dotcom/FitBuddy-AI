# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web application that uses Google Gemini to create a personalized seven-day workout plan and a practical nutrition or recovery tip. Users can submit feedback and receive a revised plan while the original plan remains stored.

## Features

- User profile form with goal and intensity validation
- Gemini-generated workout and nutrition guidance
- Feedback-based plan updates
- SQLite persistence with SQLAlchemy
- Responsive Jinja2 pages and an admin user list
- Friendly handling for invalid input, missing keys, and AI failures

## Technologies

Python, FastAPI, Uvicorn, Google Gemini API, SQLAlchemy, SQLite, Jinja2, HTML/CSS, python-multipart, python-dotenv.

## Structure

```text
app/                 Application code and database layer
templates/           Jinja2 pages
static/style.css     Responsive UI styles
docs/                GitHub Pages preview and supporting documents
Phase wise docs/     Phase-by-phase submission documents
.env                 Local Gemini key (never commit this file)
requirements.txt     Python dependencies
```

## SmartBridge Phase-Wise Development

The project is maintained and submitted through eight phases. The detailed material for each phase is stored in [`Phase wise docs/`](Phase%20wise%20docs/), while supporting project documentation remains in [`docs/`](docs/).

```text
Phase wise docs/
├── Phase 01/  Brainstorming & Ideation
├── Phase 02/  Requirement Analysis
├── Phase 03/  Project Design
├── Phase 04/  Project Planning
├── Phase 05/  Project Development
├── Phase 06/  Project Testing
├── Phase 07/  Project Documentation
└── Phase 08/  Project Demonstration
```

### Phase Documents

1. [Brainstorming & Ideation](Phase%20wise%20docs/Phase%2001/README.md)
2. [Requirement Analysis](Phase%20wise%20docs/Phase%2002/README.md)
3. [Project Design](Phase%20wise%20docs/Phase%2003/README.md)
4. [Project Planning](Phase%20wise%20docs/Phase%2004/README.md)
5. [Project Development](Phase%20wise%20docs/Phase%2005/README.md)
6. [Project Testing](Phase%20wise%20docs/Phase%2006/README.md)
7. [Project Documentation](Phase%20wise%20docs/Phase%2007/README.md)
8. [Project Demonstration](Phase%20wise%20docs/Phase%2008/README.md)

## Setup on Windows PowerShell

```powershell
python -m venv fitbuddy-env
.\fitbuddy-env\Scripts\Activate.ps1
pip install -r requirements.txt
```

Add your key to `.env`:

```text
GOOGLE_API_KEY=your_real_gemini_api_key
```

Run the application:

```powershell
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000/) and API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Routes

- `GET /` home form
- `POST /generate-workout` generate and save a plan
- `POST /submit-feedback` revise a plan with Gemini
- `GET /view-all-users` view stored users and plans

The SQLite database is created automatically as `fitbuddy.db`. It is ignored by Git along with `.env`.

## GitHub

Create a repository, then run `git init`, `git add .`, `git commit -m "Initial FitBuddy application"`, add your GitHub remote, and push. Verify `.env` is ignored before pushing.

## GitHub Pages preview

The GitHub Actions workflow publishes a static preview from `docs/` when changes are pushed to `main` or `master`. In the repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**. The preview does not run FastAPI, Gemini requests, feedback updates, or SQLite storage; those features require the app server.

## Deploy the full app on Vercel

GitHub Pages only hosts the static preview. To publish the working FastAPI app, import this repository as a Vercel project and connect it to GitHub. Vercel detects the FastAPI entry point in `app/main.py` and automatically deploys pushes to the production branch.

Before deploying, add these environment variables in the Vercel project settings:

- `GOOGLE_API_KEY`: your Gemini API key
- `DATABASE_URL`: a PostgreSQL connection URL from a managed provider such as Neon; use its pooled URL when available

Vercel's function filesystem is temporary and cannot provide durable SQLite storage. Local development continues to use `fitbuddy.db`; Vercel requires `DATABASE_URL` so generated plans, feedback, and user records persist in PostgreSQL. Do not commit either secret to the repository.
