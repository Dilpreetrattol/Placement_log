# PlacementLog

A self-hosted tracker for campus placement season — log companies, applications,
and interview rounds, then see where your time is actually going on a dashboard.

Built to replace the usual scattered spreadsheet with something that has real
relationships between the data (a company has applications, an application has
rounds), enforces its own consistency (deleting a company cleans up everything
under it), and turns the raw log into a few insights (status funnel, topics that
keep coming up across interviews, how you're rated round-over-round).

## Features

- **Companies** — tier, CTC range, CGPA cutoff, bond, on/off-campus mode. Full CRUD.
- **Applications** — one per company, with a status that moves through the actual
  pipeline (`Applied → Shortlisted → OA → OA Result → TR1 → TR2 → HR → Offer/Reject`).
- **Rounds** — per-application interview rounds with a date, a 1–5 performance
  rating, free-text topics asked (rendered as chips), and an outcome.
- **Dashboard** — Chart.js visualizations built from live SQLAlchemy aggregate
  queries: applications by status, applications by company tier, round outcomes
  (pass/fail/pending), average rating by round type, and the most frequently
  asked interview topics across every round logged.
- **CSV export** — one click to a spreadsheet-friendly dump for anything the
  dashboard doesn't cover.
- **Season countdown** — home page counts down to (or up from) a placement
  season start date set via `.env`, not hardcoded.

## Tech stack

- **Backend:** Flask (blueprints per resource), Flask-SQLAlchemy
- **Database:** SQLite for local dev, swaps to Postgres in production via
  `DATABASE_URL` (deploys as-is to Render/Railway/etc.)
- **Frontend:** server-rendered Jinja templates, hand-written CSS (no framework),
  Chart.js for the dashboard
- **Testing:** pytest, 19 tests covering models, all CRUD routes, and the
  dashboard/export views, run against an in-memory SQLite DB

## Project structure

```
app/
  models.py            Company, Application, Round + relationships/cascades
  config.py             Development / Production / Testing configs
  routes/
    main.py             Home page + dashboard aggregate queries
    companies.py         Company CRUD
    applications.py       Application CRUD
    rounds.py            Round CRUD
    export.py            CSV export
  templates/             Jinja templates, one folder per resource
  static/
    css/style.css        All styling
    js/charts.js          Chart.js rendering helpers used by dashboard.html
tests/                   pytest suite (fixtures in conftest.py)
```

## Running it locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
cp .env.example .env          # then fill in SECRET_KEY etc. (Windows: copy .env.example .env)

python run.py                 # http://localhost:5000
```

On first run, `create_app()` creates the SQLite tables automatically — no
migration step needed for local dev.

### Configuration

Set via `.env` (see `app/config.py`):

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session signing key |
| `DATABASE_URL` | Postgres URL in production; ignored in dev (SQLite) |
| `PLACEMENT_SEASON_START` | `YYYY-MM-DD` — drives the home page countdown |

### Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Design notes

A few decisions worth knowing if this comes up in an interview:

- **Cascading deletes are model-level**, not just UI confirmation dialogs —
  `Company.applications` and `Application.rounds` are declared with
  `cascade='all, delete-orphan'`, so removing a company can never leave
  orphaned applications/rounds in the database.
- **The dashboard does its aggregation in SQL**, not in Python — status/tier
  breakdowns use `func.count()` with `group_by()` at the query layer rather
  than pulling every row and counting in a loop (topic frequency is the one
  exception, since topics live as a comma-separated string on `Round` rather
  than their own table — a normalization the data model would benefit from,
  see below).
- **Add and Edit share one template** per resource (`form.html`) instead of
  duplicating markup — the route decides whether it's inserting or updating.

## Possible next steps

- Normalize `Round.topics_asked` into a `Topic` model with a many-to-many
  join, instead of a comma-separated string.
- Auth, if this ever needs to track more than one person's applications.
- Migrations (Alembic/Flask-Migrate) once the schema needs to change without
  wiping local data.
