import time
from sqlalchemy.orm import Session
from database.models import AuditLog
from shared_libs.core.contexts import RequestContext, SecurityContext

class AuditService:
    @staticmethod
    def log(
        db: Session,
        request_ctx: RequestContext,
        security_ctx: SecurityContext,
        action: str,
        status: str,
        target_id: str = None,
        target_type: str = None,
        duration_ms: int = None
    ):
        """
        Synchronously log an audit event to the database.
        In Sprints 7+, this will be migrated to the Transactional Outbox pattern.
        """
        audit_entry = AuditLog(
            tenant_id=request_ctx.tenant_id,
            organization_id=request_ctx.organization_id,
            workspace_id=request_ctx.workspace_id,
            action=action,
            target_id=target_id,
            target_type=target_type,
            actor_id=security_ctx.user_id,
            status=status,
            correlation_id=request_ctx.correlation_id,
            ip_address=None, # Extract from request later if needed
            user_agent=request_ctx.platform,
            duration_ms=duration_ms,
            authentication_method=security_ctx.authentication_method
        )
        
        db.add(audit_entry)
        db.commit()
