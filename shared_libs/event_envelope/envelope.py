import uuid
import datetime

def create_envelope(event_type, source, payload, correlation_id=None, causation_id=None, tenant_id="default"):
    """
    Creates a standard Event Envelope required by the Architecture Guidelines.
    Includes trace_id and tenant_id for distributed tracing and multi-tenant support.
    """
    return {
        "metadata": {
            "event_id": str(uuid.uuid4()),
            "trace_id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "event_type": event_type,
            "event_version": "1.0",
            "source": source,
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "causation_id": causation_id,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        },
        "payload": payload
    }
