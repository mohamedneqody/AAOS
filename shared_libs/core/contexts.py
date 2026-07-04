from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class RequestContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    request_id: UUID
    correlation_id: UUID
    trace_id: str
    span_id: str
    
    tenant_id: UUID
    organization_id: UUID
    workspace_id: UUID
    project_id: UUID
    
    locale: str
    timezone: str
    language: str
    currency: str
    branding_id: str
    
    client_version: str
    platform: str

class SecurityContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id: UUID
    authentication_method: str
    session_id: Optional[UUID] = None
    api_key_id: Optional[UUID] = None
    
    permissions: List[str]
    roles: List[str]
    
    authentication_time: datetime
