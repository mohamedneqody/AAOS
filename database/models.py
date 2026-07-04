from sqlalchemy import Column, String, Integer, JSON, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import UUID
import datetime
import uuid

Base = declarative_base()

class TenantScopedEntity:
    """Base mixin for all SaaS multi-tenant tables."""
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    organization_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    workspace_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)

class User(Base, TenantScopedEntity):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Organization(Base, TenantScopedEntity):
    __tablename__ = 'organizations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

class Workspace(Base, TenantScopedEntity):
    __tablename__ = 'workspaces'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

class Project(Base, TenantScopedEntity):
    __tablename__ = 'projects'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

class Role(Base, TenantScopedEntity):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

class Permission(Base, TenantScopedEntity):
    __tablename__ = 'permissions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

class ApiKey(Base, TenantScopedEntity):
    __tablename__ = 'api_keys'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_revoked = Column(Boolean, default=False)

class AuditLog(Base, TenantScopedEntity):
    __tablename__ = 'audit_logs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String, nullable=False, index=True)
    target_id = Column(String, nullable=True)
    target_type = Column(String, nullable=True)
    actor_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, nullable=False)
    correlation_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    authentication_method = Column(String, nullable=True)

# Legacy Models preserved for backward compatibility
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True)
    type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TaskState(Base):
    __tablename__ = 'task_states'
    id = Column(String, primary_key=True)
    task_id = Column(String)
    state = Column(String)
    updated_at = Column(DateTime)

class Cost(Base):
    __tablename__ = 'costs'
    id = Column(String, primary_key=True)
    task_id = Column(String)
    amount = Column(Float)
