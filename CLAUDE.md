# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
source venv/bin/activate
python app.py          # starts on http://localhost:5001
```

Port 5001 is hardcoded in `app.py` (`app.run(debug=True, port=5001)`) because 5000 is occupied on this machine.

## Running tests

```bash
source venv/bin/activate
pytest                 # all tests
pytest tests/test_foo.py::test_name   # single test
```

Framework: `pytest` + `pytest-flask`. No tests exist yet — the project is under active development.

## Architecture

**`app.py`** — single-file Flask application. All routes live here. Many routes currently return placeholder strings and will be implemented in later steps.

**`database/db.py`** — not yet implemented. Will expose three functions: `get_db()` (SQLite connection with row_factory and foreign keys), `init_db()` (CREATE TABLE IF NOT EXISTS), `seed_db()` (sample data). The database package is imported via `database/__init__.py`.

**`templates/`** — Jinja2 templates. All pages extend `base.html`, which provides the navbar, footer, and block slots: `{% block title %}`, `{% block head %}` (for page-specific CSS/meta), `{% block content %}`, `{% block scripts %}` (for page-specific JS).

**`static/css/style.css`** — global styles and all CSS custom properties. Always use these variables; never hardcode colors or fonts:
- Colors: `--ink`, `--ink-soft`, `--ink-muted`, `--ink-faint`, `--paper`, `--paper-card`, `--accent`, `--accent-light`, `--danger`, `--border`, `--border-soft`
- Typography: `--font-display` (DM Serif Display), `--font-body` (DM Sans)
- Radii: `--radius-sm`, `--radius-md`, `--radius-lg`

**`static/css/landing.css`** — landing-page-only styles (hero section, mock dashboard, video modal). Loaded via `{% block head %}` in `landing.html` only.

**`static/js/main.js`** — global JS placeholder. Page-specific JS goes in `{% block scripts %}` inline in the relevant template (see the YouTube modal in `landing.html` for the pattern).
