import jwt
from datetime import datetime, timedelta
from typing import Optional

from app.config import get_settings

settings = get_settings()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.better_auth_secret, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token, settings.better_auth_secret, algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user_id from a JWT token."""
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None


# ✅ Add this to fix your import
def decode_access_token(token: str) -> Optional[dict]:
    """Alias for verify_token (for backward compatibility)."""
    return verify_token(token)
#
# 
# 
# 
# old
# import jwt
# from datetime import datetime, timedelta
# from typing import Optional

# from app.config import get_settings


# settings = get_settings()

# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_DAYS = 7


# def create_access_token(user_id: str, email: str) -> str:
#     """Create a JWT access token."""
#     expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
#     payload = {
#         "sub": user_id,
#         "email": email,
#         "exp": expire,
#         "iat": datetime.utcnow(),
#     }
#     return jwt.encode(payload, settings.better_auth_secret, algorithm=ALGORITHM)


# def verify_token(token: str) -> Optional[dict]:
#     """Verify and decode a JWT token."""
#     try:
#         payload = jwt.decode(
#             token, settings.better_auth_secret, algorithms=[ALGORITHM]
#         )
#         return payload
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None


# def get_user_id_from_token(token: str) -> Optional[str]:
#     """Extract user_id from a JWT token."""
#     payload = verify_token(token)
#     if payload:
#         return payload.get("sub")
#     return None
