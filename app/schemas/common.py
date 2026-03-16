from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: str
    detail: str
    code: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
