# no-scrum

Monorepo with a **Next.js** frontend and a **FastAPI** backend (async SQLAlchemy + Postgres).

```
no-scrum/
├── frontend/    Next.js 16 (App Router, TypeScript, Tailwind, Turbopack)
└── backend/     FastAPI + async SQLAlchemy + Postgres (Docker)
```

## Prerequisites

- **Docker** + Docker Compose (for the backend + Postgres)
- **Node.js 20+** and **npm** (for the frontend)
- **uv** (only if running the backend outside Docker) — install with `brew install uv` or [docs](https://docs.astral.sh/uv/)

## Quick start

Open two terminals.

### 1. Backend + Postgres

```sh
cd backend
docker compose up
```

- API: <http://localhost:8000>
- Interactive docs: <http://localhost:8000/docs>
- Postgres: `localhost:5432` (user: `postgres`, pass: `postgres`, db: `app`)

Add `--build` the first time, or after changing dependencies / the Dockerfile:

```sh
docker compose up --build
```

### 2. Frontend

```sh
cd frontend
npm install         # first time only
npm run dev
```

- App: <http://localhost:3000>

## Running the backend without Docker

Postgres still needs to be reachable on `localhost:5432`. Then:

```sh
cd backend
uv sync                            # install deps into .venv
cd app
uv run fastapi dev --port 8000     # dev with hot reload
```

## Backend conventions

- Dependency management: **`uv`** only — never `pip`. Lockfile is `backend/uv.lock`.
- **No `__init__.py`** files inside `backend/app/`; the project uses PEP 420 namespace packages.
- All imports inside `backend/app/` use **bare** paths (no `app.` prefix), e.g. `from api.v1.router import api_router`. The package root is `backend/app/`, not `backend/`.

Add a dependency:

```sh
cd backend
uv add <pkg>          # runtime
uv add --dev <pkg>    # dev only
```


## Stopping things

```sh
# In the terminal running compose: Ctrl+C
# To remove containers (data in the postgres_data volume is kept):
cd backend && docker compose down

# To also wipe the database:
cd backend && docker compose down -v
```
