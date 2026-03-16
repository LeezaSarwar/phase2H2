from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional

from app.utils.jwt import verify_token


security = HTTPBearer(auto_error=False)


async def get_current_user(request: Request) -> dict:
    """
    Dependency to extract and verify JWT from cookies or Authorization header.
    Returns the decoded token payload.
    """
    token = None

    # Try to get token from cookie first
    token = request.cookies.get("auth_token")

    # Fall back to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload


def verify_user_access(token_user_id: str, path_user_id: str) -> None:
    """
    Verify that the user_id in the path matches the user_id in the token.
    Raises HTTPException if they don't match.
    """
    if token_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch",
        )
