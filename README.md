# GenAI Eval Engine

A FastAPI-based evaluation service for scoring LLM outputs. The system accepts a prompt and a model response, stores the run, evaluates it asynchronously with Gemini through LangChain, and exposes a React dashboard for submitting, reviewing, editing, and deleting evaluation runs.

## What It Does

- Registers and authenticates users with JWT bearer tokens.
- Stores evaluation runs in PostgreSQL with per-user ownership.
- Scores model outputs on overall score, correctness, completeness, clarity, and reasoning.
- Runs scoring jobs asynchronously with Celery and Redis.
- Caches repeated prompt/output scoring results in Redis.
- Supports golden runs and expected scores for regression checks.
- Ships with a Vite React dashboard and an Nginx reverse proxy for Docker Compose.

## Architecture

```text
React dashboard
      |
      v
Nginx reverse proxy
      |
      v
FastAPI API  <---->  PostgreSQL
      |
      v
Redis broker/cache  <---->  Celery worker
                           |
                           v
                    Gemini scorer via LangChain
```

Main backend layers:

```text
app/
  api/routes/       HTTP endpoints
  models/           SQLAlchemy database models
  schemas/          Pydantic request/response schemas
  repositories/     Database access functions
  services/         Evaluation and scoring logic
  middleware/       Logging and rate limiting
  utils/            Auth, password, cache, and error helpers
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Auth: JWT with `python-jose`, password hashing with Passlib/bcrypt
- Jobs/cache: Celery and Redis
- Database: PostgreSQL
- LLM scoring: LangChain + `langchain-google-genai`
- Frontend: React + Vite
- Deployment/dev orchestration: Docker Compose, Nginx
- Tests: Pytest

## Repository Layout

```text
.
├── app/                         FastAPI application
├── alembic/                     Database migrations
├── frontend/eval-dashboard/     React dashboard
├── nginx/nginx.conf             Reverse proxy config
├── tests/                       Backend tests
├── docker-compose.yml           Local service stack
├── Dockerfile                   Backend/worker image
├── entrypoint.sh                Runs migrations then starts API
├── requirements.txt             Python dependencies
└── eval_engine_architecture_v3.svg
```

## Environment Variables

Create a `.env` for local backend runs or use `.env.docker` with Docker Compose. Start from `.env.example`, then fill in real values.

```env
APP_NAME=GenAI Eval Engine
SECRET_KEY=change-this-to-a-long-random-secret
DEBUG=False
DATABASE_URL=postgresql://eval_user:eval_pass@localhost:5433/eval_db
GOOGLE_API_KEY=your-google-api-key
HUGGINGFACEHUB_API_KEY=your-huggingface-key
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=eval-engine
REDIS_URL=redis://localhost:6379/0
```

For Docker Compose, the API container talks to Postgres and Redis by service name, so `.env.docker` should use values like:

```env
DATABASE_URL=postgresql://eval_user:eval_pass@db:5432/eval_db
REDIS_URL=redis://redis:6379/0
```

## Run With Docker Compose

Docker Compose is the easiest way to start the backend stack.

```bash
docker compose up --build
```

Services:

- PostgreSQL: host port `5433`, container port `5432`
- Redis: host port `6379`
- API: internal port `8000`
- Nginx: host port `80`, proxying to the API
- Celery worker: background evaluation jobs

The backend entrypoint runs Alembic migrations automatically before starting Uvicorn.

Useful URLs:

- API health: `http://localhost/health`
- Readiness check: `http://localhost/ready`
- API docs: `http://localhost/docs`
- Versioned API base: `http://localhost/api/v1`

## Run Backend Locally Without Docker

Start PostgreSQL and Redis first, then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with real values, then run migrations and start the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Start a Celery worker in another terminal:

```bash
celery -A app.celery_app worker --loglevel=info
```

The direct local backend URL is `http://localhost:8000`.

## Run The Frontend

```bash
cd frontend/eval-dashboard
npm install
npm run dev
```

The dashboard API client currently uses:

```js
const BASE_URL = 'http://localhost/api/v1'
```

That works with the Docker Compose Nginx service on port `80`. If you run the backend directly with Uvicorn on port `8000`, update `frontend/eval-dashboard/src/services/api.js` to:

```js
const BASE_URL = 'http://localhost:8000/api/v1'
```

Frontend checks:

```bash
npm run lint
npm run build
```

## API Overview

Health:

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Basic liveness check |
| `GET` | `/ready` | Checks database and Redis connectivity |

Auth:

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Create a user |
| `POST` | `/api/v1/auth/login` | Return a JWT bearer token |
| `POST` | `/api/v1/auth/logout` | Blacklist the current token in Redis |
| `GET` | `/api/v1/auth/me` | Return the current authenticated user |

Runs:

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/runs/` | Create a pending evaluation run |
| `GET` | `/api/v1/runs/` | List runs owned by the current user |
| `GET` | `/api/v1/runs/{run_id}` | Fetch one owned run |
| `PATCH` | `/api/v1/runs/{run_id}` | Update an owned run and invalidate cached score |
| `DELETE` | `/api/v1/runs/{run_id}` | Delete an owned run |
| `POST` | `/api/v1/runs/{run_id}/evaluate` | Queue the run for async evaluation |

All `/api/v1/runs/*` routes require an `Authorization: Bearer <token>` header.

## Example API Flow

Register:

```bash
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'
```

Login:

```bash
TOKEN=$(curl -s -X POST http://localhost/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

Create a run:

```bash
curl -X POST http://localhost/api/v1/runs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "experiment_id": 1,
    "prompt": "What is retrieval augmented generation?",
    "model_output": "RAG combines retrieval with generation to answer using external context.",
    "model_name": "example-model"
  }'
```

Queue evaluation:

```bash
curl -X POST http://localhost/api/v1/runs/1/evaluate \
  -H "Authorization: Bearer $TOKEN"
```

List runs:

```bash
curl http://localhost/api/v1/runs/ \
  -H "Authorization: Bearer $TOKEN"
```

## Evaluation Behavior

When a run is evaluated:

1. The Celery worker loads the run from PostgreSQL.
2. `EvalService` builds a Redis cache key from the prompt and model output.
3. If a cached score exists, the worker reuses it.
4. Otherwise, `ScorerService` sends the prompt/output pair to Gemini.
5. The scorer expects structured output with:
   - `score`
   - `reasoning`
   - `correctness`
   - `completeness`
   - `clarity`
6. The run is updated with the score fields and marked `completed`.

The worker retries failed evaluations up to three times. Cached scores expire after one hour.

## Regression Runs

The `runs` table includes:

- `is_golden`: marks a run as part of the regression set.
- `expected_score`: expected minimum score reference.

`app.tasks.run_regression` finds golden runs and queues them for evaluation. The worker logs a regression warning when a completed score is more than `0.1` below the expected score.

Note: the current Celery beat schedule should be reviewed before relying on nightly regression automation, because the schedule entry points at `evaluate_run_task`, which expects a `run_id`. For nightly golden-run sweeps, schedule `app.tasks.run_regression` instead.

## Database Migrations

Run all migrations:

```bash
alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Check current migration state:

```bash
alembic current
alembic history
```

## Tests

Run the backend test suite:

```bash
pytest
```

The tests cover repository ownership behavior and evaluation service updates with fake scorer/Redis implementations, so they do not need live LLM calls.

There is also a manual LangSmith trace helper in `tests/test_langsmith.py`:

```bash
python tests/test_langsmith.py
```

That manual path requires real LangChain/LangSmith and Google API credentials.

## Operational Notes

- JWT access tokens expire after 30 minutes.
- Logout stores the current token in Redis until it expires.
- Rate limiting is Redis-backed and allows up to 1000 requests per client IP per minute.
- Request logging emits JSON logs and adds an `X-Request-ID` response header.
- CORS currently allows `http://localhost:5173`.
- The API returns structured error bodies for validation, not-found, and readiness failures.

## Troubleshooting

If the API fails on startup, check:

- `.env` or `.env.docker` contains every required variable from `.env.example`.
- `DATABASE_URL` points to `localhost:5433` for host-local development and `db:5432` inside Docker Compose.
- `REDIS_URL` points to `localhost:6379` locally and `redis:6379` inside Docker Compose.
- Alembic migrations have been applied.
- `GOOGLE_API_KEY` is valid before triggering real evaluations.

If the dashboard cannot reach the API:

- Use `http://localhost/api/v1` when Docker Compose and Nginx are running.
- Use `http://localhost:8000/api/v1` when the backend is running directly with Uvicorn.
- Confirm CORS still includes the Vite origin, `http://localhost:5173`.

