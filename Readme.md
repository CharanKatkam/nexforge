# Project Instructions — Enterprise Django Application

These instructions are mandatory for all work in this repository. Claude must follow them
on every task unless the user explicitly overrides them for a specific request.

## 1. Technology Stack (do not deviate)

| Layer            | Technology                                              |
|------------------|---------------------------------------------------------|
| Backend          | **Python (Django) only** — no Flask, FastAPI, Node, etc.|
| API              | **Django REST Framework (DRF)**                         |
| Database         | **PostgreSQL** (use `psycopg`/`psycopg2`; never SQLite in prod) |
| Admin            | **Django Admin** (register every model)                |
| Frontend         | **HTML5, CSS3, Bootstrap, vanilla JavaScript**         |
| Version Control  | **Git**                                                |

- Do **not** introduce React/Vue/Angular, SPA frameworks, or non-Bootstrap CSS frameworks.
- Do **not** swap the database engine. All migrations target PostgreSQL.
- Prefer Django/DRF built-ins over third-party packages unless there is a clear, justified need.

## 2. Project Structure & Conventions

- Settings split by environment: `settings/base.py`, `settings/dev.py`, `settings/prod.py`.
- One Django **app per bounded domain**; keep apps small and cohesive.
- Business logic lives in `services.py` / `selectors.py`, **not** in views or serializers.
- Models: explicit `__str__`, `Meta.ordering`, `verbose_name`; use `TextChoices`/`IntegerChoices`.
- DRF: `ViewSet` + `Serializer` per resource; use routers; version the API under `/api/v1/`.
- Settings, secrets, and credentials come from **environment variables** (`django-environ` or
  `os.environ`). **Never** hardcode secrets or commit `.env` files.

## 3. Code Quality — Enterprise Standards

- **PEP 8** compliant. Format with **black**, sort imports with **isort**, lint with
  **ruff** (or flake8). Type-check public interfaces with **mypy** where practical.
- Type hints on all function signatures and model methods.
- No bare `except:`; catch specific exceptions. No `print()` — use the `logging` module.
- DRY, single-responsibility functions; keep view/serializer methods short.
- All user input validated at the serializer/form layer. Use Django ORM (parameterized) —
  never string-format SQL. Escape template output (Django autoescaping stays on).
- Security: enforce authentication/permission classes on every DRF view, use CSRF protection
  for session auth, `SECURE_*` settings in prod, and least-privilege DB roles.

## 4. Testing (required for every change)

- Write tests with `pytest` + `pytest-django` (or Django `TestCase`).
- Cover: model methods, serializers (validation), API endpoints (status + payload), permissions.
- Run the full test suite before declaring a task done; report results honestly.
- Use factories (`factory_boy`) over fixtures for test data.

## 5. Documentation — MANDATORY

Documentation is a hard requirement, not optional:

- **Docstrings** on every module, class, public method, and DRF view/serializer
  (Google or NumPy style, consistent across the repo).
- **API documentation**: keep DRF endpoints self-documenting via `drf-spectacular`
  (OpenAPI schema) or DRF's browsable API; document request/response shapes.
- **README.md** kept current: setup, env vars, how to run, how to test.
- Update **migrations** and inline comments when changing models.
- Every PR/commit message explains the *why*, not just the *what*.

## 6. Database & Migrations

- Always create migrations for model changes (`makemigrations`) and review them before applying.
- Never edit applied migrations; add a new one instead.
- `migrate` and destructive DB commands (`flush`, dropping tables) require explicit user
  confirmation — never run them autonomously.

## 7. Git Workflow

- Work on feature branches; never commit directly to `main`/`master` without being asked.
- Small, focused commits. Conventional-style messages (`feat:`, `fix:`, `docs:`, `refactor:`,
  `test:`, `chore:`).
- Commit or push **only when the user asks**. Never force-push shared branches.
- Keep `.env`, `__pycache__/`, `*.pyc`, `db.sqlite3`, and local media out of version control.

## 8. Available Tooling in This Environment

- **MCP servers** (configured in `.mcp.json`):
  - `context7` — pull up-to-date Django / DRF / Bootstrap docs on demand.
  - `postgres` — inspect schema and run read-only queries (restricted mode; set `DATABASE_URI`).
  - `git` — structured git operations.
- **gstack skills** (global): `/qa`, `/review`, `/investigate`, `/cso` (security audit),
  `/ship`, `/document-generate`, `/spec`, `/office-hours`, etc. Use `/review` and `/cso`
  before shipping, and `/document-generate` to satisfy the documentation requirement.

## 9. Security & Pre-Deployment (Django / DRF / PostgreSQL mapping)

The global security checklist (`~/.claude/CLAUDE.md`) is mandatory. Here is how each control
maps onto **this** stack — implement and verify all of it before any production deploy:

- **Secrets:** `django-environ`/`os.environ`; `SECRET_KEY`, DB creds, API keys from env only.
  `.env` is git-ignored (already in `.gitignore`). Rotate anything ever exposed.
- **Authorization / IDOR:** every DRF view sets `permission_classes`; object access is scoped via
  `get_queryset()` filtering on `request.user` (and `DjangoObjectPermissions`/`has_object_permission`
  where needed). Never return an object by `pk` alone without an ownership check.
- **Input / SQLi / XSS:** validate at the serializer layer; use the ORM (parameterized) — never
  `.raw()`/`.extra()`/string-built SQL with user input; keep Django template autoescaping on and
  avoid `mark_safe`. Validate file uploads (type/size), store in `MEDIA` outside code paths.
- **Password reset tokens:** use Django's `default_token_generator`; set `PASSWORD_RESET_TIMEOUT`
  short; tokens are single-use.
- **Rate limiting:** DRF throttling (`AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle`)
  with tighter scopes on auth/reset/signup; or `django-ratelimit`. Return `429` + `Retry-After`.
- **CORS & headers:** `django-cors-headers` with `CORS_ALLOWED_ORIGINS` (never `CORS_ALLOW_ALL_ORIGINS`
  in prod); enable `SECURE_HSTS_*`, `SECURE_SSL_REDIRECT`, `SECURE_CONTENT_TYPE_NOSNIFF`,
  `X_FRAME_OPTIONS='DENY'`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and a CSP (e.g. `django-csp`).
- **Error handling:** `DEBUG = False` in prod; custom `handler403/404/500`; structured DRF
  exception responses — no stack traces or the Django yellow debug page reaching clients.
- **DB indexes:** `db_index=True` / `Meta.indexes` on foreign keys and hot `filter`/`order_by`
  fields; check with `EXPLAIN`. Don't over-index.
- **RLS / least privilege:** primary enforcement is queryset ownership; optionally add Postgres
  RLS for defense-in-depth; run the app under a least-privilege DB role (not superuser).
- **Logging/monitoring:** Python `logging` (JSON), error tracking (e.g. Sentry), alerts on 5xx/latency.
- **Dependencies:** `pip-audit` (or `safety`) before deploy; pin versions; remove demo endpoints.
- **Rollback:** tested blue-green / canary path before relying on it.

Run `/cso` and `/security-review` (and `/review`) before shipping; treat any unchecked item as a blocker.

## 10. Definition of Done

A task is complete only when: code follows the stack + style rules above, tests are written
and passing, public interfaces are documented, migrations are generated, and the change has
been linted/formatted. State explicitly what was verified and what (if anything) was skipped.
