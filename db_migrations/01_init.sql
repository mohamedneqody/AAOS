-- Core Infrastructure Schema (Phase 1)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Task Tracking (Orchestrator)
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID,
    type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'NEW',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- State Management
CREATE TABLE IF NOT EXISTS task_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    current_state VARCHAR(50) NOT NULL,
    previous_state VARCHAR(50),
    next_state VARCHAR(50),
    retry_count INTEGER DEFAULT 0,
    execution_time_ms INTEGER,
    owner VARCHAR(255),
    correlation_id UUID,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Cost Control
CREATE TABLE IF NOT EXISTS costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    resource_type VARCHAR(100) NOT NULL,
    api_cost NUMERIC(10, 6) DEFAULT 0,
    compute_cost NUMERIC(10, 6) DEFAULT 0,
    total_cost NUMERIC(10, 6) GENERATED ALWAYS AS (api_cost + compute_cost) STORED,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Event Bus / Queue (PostgreSQL SKIP LOCKED approach)
CREATE TABLE IF NOT EXISTS event_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    queue_name VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'QUEUED',
    locked_at TIMESTAMP WITH TIME ZONE,
    locked_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_event_queue_status ON event_queue(queue_name, status);
