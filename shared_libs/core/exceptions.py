class AAOSException(Exception):
    """Base exception for all AAOS errors."""
    pass

class LLMException(AAOSException):
    """Base exception for all LLM-related errors."""
    pass

class LLMValidationException(LLMException):
    """Raised when the LLM output fails Pydantic validation."""
    pass

class LLMAuthenticationException(LLMException):
    """Raised when LLM authentication fails."""
    pass

class LLMTransportException(LLMException):
    """Raised when network transport to LLM fails."""
    pass
