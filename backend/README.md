# Tarot Backend

FastAPI-based backend for Tarot Reading MVP.

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM (async)
- **PostgreSQL** - Primary database
- **Redis** - Cache and sessions
- **OpenAI/Anthropic** - LLM integration
- **Stripe** - Payment processing
- **pytest** - Testing

## Setup

### 1. Install dependencies

```bash
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pytest
```

## Code Style

```bash
ruff check .
ruff format .
```

## Type Checking

```bash
mypy app/
```
