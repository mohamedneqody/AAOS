# Changelog

## [v0.6.0] - 2026-07-04

### Completed Sprints
- **Sprint 1**: Foundation & Dispatcher
- **Sprint 2**: Execution Engine
- **Sprint 3**: Intelligence & Profiling
- **Sprint 4**: Decision Engine
- **Sprint 5**: Publishing & Artifacts
- **Sprint 6**: Enterprise SaaS Foundation (Authentication, JWT, RBAC, Database)

### Major Features
- Recovered Dispatcher architecture with dynamic worker payload routing.
- Recovered Decision Domain architecture with verifiable constraints.
- Integrated `argon2-cffi` backend for Enterprise-grade password hashing.
- Complete OpenAPI schema validations with rigid input bounds.
- Added strict RBAC rules and Docker service encapsulation.
- Implemented full Knowledge Graph node verification limits.
- Validated automated End-to-End Test Suite covering multi-worker parallel execution.

### Breaking Changes
- Fixed Dispatcher JSON serialization to native Pydantic schemas. 
- Removed generic `v1/` routing prefixes to harmonize backward-compatible external n8n workflows.

### Known Technical Debt
- **Risk Engine**: Fallback deterministic categorizations.
- **Confidence Engine**: Initial placeholder passes on graph confidence.
- **Publishing Domain**: Hardcoded default fallback templates.
- **Dependencies**: Temporary tenant/roles simulated in mocking functions pending DB integration.
- **AI Service**: Container fallback SA keys.

### Future Work
- **Sprint 7**: Distributed task scheduling & multi-node orchestration.
- PostgreSQL full relational normalization.
- Comprehensive UI implementation.
