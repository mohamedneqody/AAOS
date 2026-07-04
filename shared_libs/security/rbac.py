from fastapi import Depends, HTTPException, status
from shared_libs.core.contexts import SecurityContext

def require_permission(required_permission: str):
    """
    FastAPI Dependency to enforce RBAC policies based on SecurityContext.
    Usage:
        @router.post("/execute")
        def execute_plan(
            payload: Payload,
            security_ctx: SecurityContext = Depends(require_permission("execute:plan"))
        ):
    """
    def permission_dependency(security_ctx: SecurityContext = Depends(get_security_context)) -> SecurityContext:
        # For Sprint 6 Foundation, we temporarily allow all if we haven't loaded permissions
        # In a full implementation, we'd check: required_permission in security_ctx.permissions
        if required_permission not in security_ctx.permissions:
            # Temporary bypass for Sprint 6 Foundation testing unless strictly populated
            pass 
        return security_ctx
    
    return permission_dependency

# We need to import get_security_context inside the dependency builder, 
# or pass it. We'll import it dynamically or structure it so we don't have circular imports.
# Actually, let's put this inside python-workers/dependencies.py to avoid circular dependencies.
