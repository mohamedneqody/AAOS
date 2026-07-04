# AAOS Cloud - Architecture Baseline

**Status:** PRODUCTION FROZEN
**Sprints Covered:** Sprint 1 - Sprint 5

## System Overview
AAOS (Autonomous Agency Operating System) is an enterprise SaaS platform engineered to autonomously plan, execute, verify, decide, and publish business intelligence. The architecture relies heavily on domain-driven design principles, mapping each major lifecycle phase to a distinct, highly decoupled domain.

## Domain Boundaries
1. **Planning Domain:** Defines the overarching logic, graph structures, and expected outcomes.
2. **Execution Domain:** Handles generic worker invocations, API communication, and payload collection.
3. **Intelligence Domain:** Curates, validates, and evaluates execution payloads to produce high-confidence Insight Packages. Features a hallucination verifier and confidence scoring engine.
4. **Decision Domain:** Analyzes verified insights against business logic to synthesize Priority Scores, Risk/Opportunity Assessments, and structural Business Actions.
5. **Publishing Domain:** Consumes the Decision Package to procedurally render Dashboards, Executive Summaries, Presentations, PDFs, and Notifications via localized White Label branding.

## Contracts
All inter-domain communication is regulated by strongly-typed Pydantic Models located in `shared_libs/core/contracts/`. 
- Every schema operates with `ConfigDict(extra="forbid")`.
- Missing fields result in hard HTTP 422 errors.
- Default values are minimized to prevent implicit state.

## Runtime Pipeline
- **Orchestration layer:** Workflows are managed via `n8n`.
- **Worker layer:** API services are hosted by highly concurrent FastAPI python workers.
- **Compute layer:** AI capabilities are driven by Vertex AI Gemini models.

## Traceability
End-to-end traceability is the cornerstone of AAOS.
- **Root Anchor:** The `planning_id` (originally derived from the Planning Execution Graph) acts as the immutable identifier linking the entire pipeline.
- **Chain of Custody:** The `planning_id` is propagated from the `ExecutionResult`, through the `InsightPackage`, to the `DecisionPackage`, and finally into the `PublishingPackage`. 
- **Artifact Isolation:** Downstream artifacts (e.g., Knowledge Graphs, Decision Graphs) possess their own distinct `uuid4` identities but maintain relation to the overarching `planning_id`.

## Validation Strategy
- Real-time cryptographic validation via SHA-256 checksums to prove payload determinism.
- Strict rejection of all dummy IDs, hardcoded placeholders (`"TBD_PLAN"`, `"UNKNOWN"`), or synthetically generated traceability identifiers.
- Hallucination rejection logic guarantees execution evidence definitively supports the insight.

## Coding Rules
- Do NOT use `print()` for production traces; use the structured auditing pipeline.
- Do NOT bypass `shared_libs`. All data objects MUST serialize through contracts.
- Do NOT modify contracts unless absolutely required and backward compatibility is meticulously verified.

## Extension Rules
- If a new Domain is added, it must consume the Output Package of the previous domain without modifying the historical data.
- New pipelines MUST utilize `renderer_registry` or `template_registry` patterns (as seen in Publishing) to preserve the Open/Closed Principle.

## Enterprise Constraints
- All interfaces must account for Tenant Isolation (Branding, Localization).
- Security over Convenience.

## Future Sprint Rules
- Sprints 1 through 5 are completely **Architecture Frozen**. Modifying these modules is strictly prohibited without formal C-Level Chief Software Architect approval through a verified Production Bug Gate.
- Sprint 6 (Optimization & Analytics) must treat the outputs of Sprints 1-5 as immutable events.
