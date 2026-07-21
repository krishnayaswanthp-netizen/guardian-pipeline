# Guardian Pipeline

## Project Overview

Guardian Pipeline is the planned evolution of the existing AI Resume Screening project into an event-driven hiring workflow foundation.

This repository currently contains only the project structure and placeholders for future backend, frontend, worker, relay, database, and AI modules.

## Folder Structure

```text
backend/
  ai/
  api/
  config/
  database/
  logs/
  models/
  relay/
  schemas/
  services/
  uploads/
  utils/
  worker/
frontend/
docs/
  architecture/
  images/
demo/
  resumes/
  screenshots/
scripts/
tests/
docker/
```

## High-Level Architecture

The future system will separate API routing, service orchestration, persistence models, schema validation, asynchronous workers, outbox relay processing, and AI screening logic.

## Setup

TODO: Add environment setup instructions after implementation begins.

## Demo

TODO: Add demo instructions and screenshots after implementation begins.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Celery
- Redis
- Docker
- LangChain

## Development Roadmap

- Define backend API contracts.
- Add database models and migrations.
- Integrate resume upload handling.
- Connect the screening chain.
- Add worker-based background processing.
- Implement outbox relay processing.
- Build frontend workflows.
- Add automated tests.

## How to Run

TODO: Add setup and run instructions after implementation begins.

## Future Improvements

- Authentication and authorization.
- Observability and structured logging.
- Admin review dashboard.
- Queue monitoring.
- Deployment automation.
