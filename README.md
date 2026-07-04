# Autonomous Content Business (ACB) - Enterprise Edition

Welcome to the AI Business Operating System. 

## Architecture Philosophy
This system is strictly designed with the principle: **"n8n is for Orchestration only."**
- **n8n**: Executes DAGs, coordinates events, triggers workers.
- **Python**: Executes ALL deterministic logic (Data, Pandas, API Calls, Revenue Math, Validation).
- **Gemini 2.5 Pro**: Used exclusively for high-level Strategic Planning, Goal Generation, and Risk Assessment.
- **Gemini 3.5 Flash**: Used exclusively for high-volume content generation, copywriting, and formatting.

## Core Capabilities (Phase 4 MVP)
- `StrategyCapability`: Utilizes a Trend Change Detector to determine if Gemini Pro needs to be called.
- `PlanningCapability`: Translates strategies into task queues.
- `RevenueValidationCapability`: Enforces a strict profit policy (APPROVED/NEEDS_REVIEW/REJECTED).
- `ProductionCapability`: Generates platform-specific copy using Flash.
- `QualityGateCapability`: 5 stages of checking resulting in INFO, WARNING, ERROR, FATAL severities.
- `TelegramPublisherCapability`: Pushes directly to Telegram API.
- `KPIEngineCapability`: Calculates ROI, CTR, EPC, Conversion Rate, and Cost Per Asset.

## System Components
1. **Event Bus & Queues**: Powered by PostgreSQL `SKIP LOCKED` for massive scale and concurrency. Contains `q_dead_letter`.
2. **State Manager**: Keeps strict track of `Current`, `Previous`, `Next`, and `Owner` states with Correlation IDs for distributed tracing.
3. **Model Router**: Reads `routing.yaml` to securely dispatch AI tasks without hardcoded logic.
4. **Cost Engine**: Dynamically calculates token usage per model and records execution compute time.

## CI/CD and Tests
See `.github/workflows/ci.yml` and `db_migrations/alembic`. Code is enforced via Ruff and Black.

## Running the E2E Demo
Run `python e2e_demo.py` to trace the entire Business Flow locally without booting up n8n.
