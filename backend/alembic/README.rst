# Alembic Migration Scripts

This directory contains Alembic migration scripts.

## Creating a new migration

```bash
alembic revision --autogenerate -m "description of changes"
```

## Applying migrations

```bash
alembic upgrade head
```

## Rolling back migrations

```bash
alembic downgrade -1
```

## Viewing migration history

```bash
alembic history
```

## Current migration version

```bash
alembic current
```
