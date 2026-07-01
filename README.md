# no-scrum

Monorepo with a **Next.js** frontend and a **FastAPI** backend (async SQLAlchemy + Postgres).

```
no-scrum/
├── frontend/    Next.js 16 (App Router, TypeScript, Tailwind, Turbopack)
└── backend/     FastAPI + async SQLAlchemy + Postgres
```

## Prerequisites

- **Docker** + Docker Compose
- **Node.js 20+** and **npm** (for the frontend)
- **uv** — only needed for Workflow B below. Install with `brew install uv` or see the [docs](https://docs.astral.sh/uv/)

## Two backend workflows

Both use the same `backend/docker-compose.yml` and the same named volume (`backend_postgres_data`), so the database is shared between them — switch freely without losing data.

| | Postgres | Backend |
|---|---|---|
| **A — full Docker** | container | container, hot reload via mounted volume |
| **B — DB only** | container | runs on your machine via `fastapi dev` |

Use **A** for a one-command "just run it" setup. Use **B** when you want to attach a debugger, avoid rebuilding the image after every dependency change, or just prefer running Python locally.

### Workflow A — everything in Docker

```sh
cd backend
docker compose --profile full up --build
```

- API: <http://localhost:8000>
- Interactive docs: <http://localhost:8000/docs>
- Postgres: `localhost:5433` (user `postgres`, pass `postgres`, db `app`)

`--build` is only needed the first time, or after changing dependencies / the Dockerfile — afterwards plain `docker compose --profile full up` is enough. On startup the backend container runs `alembic upgrade head` automatically, then starts `fastapi dev` with `app/` mounted for hot reload.

### Workflow B — Postgres in Docker, backend on your machine

```sh
cd backend
docker compose up          # starts only postgres-noscrum (no --profile needed)
```

```sh
cd backend
uv sync                          # first time, or after pulling dependency changes
cd app
uv run fastapi dev --port 8000   # hot reload
```

- API: <http://localhost:8000>
- Postgres: `localhost:5433`

Migrations are **not** applied automatically in this workflow — see [Alembic migrations](#alembic-migrations).

## Frontend

Same in either workflow:

```sh
cd frontend
npm install      # first time only
npm run dev
```

- App: <http://localhost:3000>

## Alembic migrations

`alembic.ini` lives in `backend/` — run all `alembic` commands from there.

### Create a migration

After changing a model in `backend/app/models/`:

```sh
cd backend
uv run alembic revision --autogenerate -m "describe the change"
```

Open the generated file in `app/migrations/versions/` and check it before applying — autogenerate can miss things (renames look like a drop + add, some constraint changes aren't detected).

For a hand-written migration (data backfills, etc.) drop `--autogenerate`:

```sh
uv run alembic revision -m "describe the change"
```

### Apply / inspect / roll back

```sh
cd backend
uv run alembic upgrade head      # apply all pending migrations
uv run alembic downgrade -1      # roll back the most recent one
uv run alembic history           # show applied vs. pending revisions
```

These need Postgres reachable on `localhost:5433` — i.e. at least `docker compose up` (Workflow B's postgres container) running.

In **Workflow A** this happens automatically when the backend container starts, so you only need to run these by hand in **Workflow B**.

## Backend conventions

- Dependency management: **`uv`** only — never `pip`. Lockfile is `backend/uv.lock`.
- **No `__init__.py`** files inside `backend/app/`; the project uses PEP 420 namespace packages.
- All imports inside `backend/app/` use **bare** paths (no `app.` prefix), e.g. `from api.v1.router import api_router`. The package root is `backend/app/`, not `backend/`.

```sh
cd backend
uv add <pkg>          # runtime dependency
uv add --dev <pkg>    # dev-only dependency
```

## Stopping / resetting

```sh
# Ctrl+C in the compose terminal, then remove containers (use the same
# --profile flag you started with, so both services are torn down):
cd backend && docker compose --profile full down   # Workflow A
cd backend && docker compose down                  # Workflow B

# Add -v to also wipe the database volume:
cd backend && docker compose --profile full down -v
```
