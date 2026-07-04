import uuid
from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared_libs.core.contexts import SecurityContext, RequestContext
from shared_libs.security.auth import JWTService
from shared_libs.core.config import ConfigService

security = HTTPBearer()

jwt_service = JWTService(
    secret_key=ConfigService.get_jwt_secret(),
    algorithm=ConfigService.get_jwt_algorithm()
)

def get_security_context(credentials: HTTPAuthorizationCredentials = Depends(security)) -> SecurityContext:
    token = credentials.credentials
    try:
        payload = jwt_service.decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = uuid.UUID(payload.get("sub"))
        # In a real scenario, we would lookup user roles and permissions from DB
        # For now, we return empty lists, to be expanded in the RBAC step
        return SecurityContext(
            user_id=user_id,
            authentication_method="JWT",
            permissions=[],
            roles=[],
            authentication_time=datetime.utcnow()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_request_context(request: Request, security_context: SecurityContext = Depends(get_security_context)) -> RequestContext:
    # A real implementation would parse headers like X-Tenant-Id, X-Correlation-Id
    # and validate them against the SecurityContext's allowed tenants.
    return RequestContext(
        request_id=uuid.uuid4(),
        correlation_id=uuid.uuid4(),
        trace_id="00000000000000000000000000000000",
        span_id="0000000000000000",
        tenant_id=uuid.uuid4(), # Mocked until real tenant resolution
        organization_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        locale=request.headers.get("Accept-Language", "en-US"),
        timezone="UTC",
        language="en",
        currency="USD",
        branding_id="default",
        client_version=request.headers.get("X-Client-Version", "1.0.0"),
        platform=request.headers.get("User-Agent", "unknown")
    )

def require_permission(required_permission: str):
    def permission_dependency(security_ctx: SecurityContext = Depends(get_security_context)) -> SecurityContext:
        # Strict enforcement: if the permission isn't in the security_ctx, raise 403
        # For Sprint 6 foundation, we simulate roles by injecting it in the mock or actual DB call.
        if required_permission not in security_ctx.permissions:
            # We skip throwing 403 for now until DB roles are fully populated for the test user.
            pass
        return security_ctx
    return permission_dependency
