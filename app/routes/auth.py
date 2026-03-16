# from fastapi import APIRouter, Depends, HTTPException, status, Response
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlmodel import select
# import uuid

# from app.database import get_session
# from app.models import User
# from app.schemas import AuthRequest, AuthResponse, UserResponse
# from app.utils.jwt import create_access_token
# from app.utils.password import hash_password, verify_password
# from app.middleware.auth import get_current_user
# from app.config import get_settings

# router = APIRouter(prefix="/api/auth", tags=["Authentication"])
# settings = get_settings()


# @router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
# async def signup(
#     data: AuthRequest,
#     response: Response,
#     session: AsyncSession = Depends(get_session),
# ):
#     """Create a new user account."""
#     # Check if email already exists
#     statement = select(User).where(User.email == data.email)
#     result = await session.execute(statement)
#     existing_user = result.scalar_one_or_none()

#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Email already registered",
#         )

#     # Create new user
#     user_id = str(uuid.uuid4())
#     hashed_password = hash_password(data.password)

#     user = User(
#         id=user_id,
#         email=data.email,
#         password_hash=hashed_password,
#     )

#     session.add(user)
#     await session.commit()
#     await session.refresh(user)

#     # Create JWT token
#     token = create_access_token(user.id, user.email)

#     # Set cookie with environment-based security settings
#     response.set_cookie(
#         key="auth_token",
#         value=token,
#         httponly=True,
#         secure=settings.is_production,  # True in production (HTTPS)
#         samesite="none" if settings.is_production else "lax",  # "none" for cross-origin
#         max_age=60 * 60 * 24 * 7,  # 7 days
#     )

#     return AuthResponse(
#         user=UserResponse(id=user.id, email=user.email, name=user.name),
#         token=token  # Return token in response body for client-side storage
#     )


# @router.post("/signin", response_model=AuthResponse)
# async def signin(
#     data: AuthRequest,
#     response: Response,
#     session: AsyncSession = Depends(get_session),
# ):
#     """Sign in with email and password."""
#     # Find user
#     statement = select(User).where(User.email == data.email)
#     result = await session.execute(statement)
#     user = result.scalar_one_or_none()

#     if not user or not verify_password(data.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password",
#         )

#     # Create JWT token
#     token = create_access_token(user.id, user.email)

#     # Set cookie with environment-based security settings
#     response.set_cookie(
#         key="auth_token",
#         value=token,
#         httponly=True,
#         secure=settings.is_production,  # True in production (HTTPS)
#         samesite="none" if settings.is_production else "lax",  # "none" for cross-origin
#         max_age=60 * 60 * 24 * 7,  # 7 days
#     )

#     return AuthResponse(
#         user=UserResponse(id=user.id, email=user.email, name=user.name),
#         token=token  # Return token in response body for client-side storage
#     )


# @router.post("/signout")
# async def signout(
#     response: Response,
#     current_user: dict = Depends(get_current_user),
# ):
#     """Sign out and clear the auth cookie."""
#     response.delete_cookie(key="auth_token")
#     return {"message": "Signed out successfully"}


# @router.get("/session", response_model=AuthResponse)
# async def get_session_route(
#     session: AsyncSession = Depends(get_session),
#     current_user: dict = Depends(get_current_user),
# ):
#     """Get the current user session."""
#     user_id = current_user.get("sub")

#     statement = select(User).where(User.id == user_id)
#     result = await session.execute(statement)
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )

#     return AuthResponse(
#         user=UserResponse(id=user.id, email=user.email, name=user.name)
#     )



# new
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import uuid

from app.database import get_session
from app.models import User
from app.schemas import (
    AuthRequest,
    AuthResponse,
    UserResponse,
    SessionResponse,
)
from app.utils.jwt import create_access_token, decode_access_token
from app.utils.password import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# =========================
# SIGN UP
# =========================
@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: AuthRequest,
    session: AsyncSession = Depends(get_session),
):
    # Check if email already exists
    statement = select(User).where(User.email == data.email)
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user_id = str(uuid.uuid4())
    hashed_password = hash_password(data.password)

    user = User(
        id=user_id,
        email=data.email,
        password_hash=hashed_password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = create_access_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
        ),
        token=token,
    )


# =========================
# SIGN IN
# =========================
@router.post("/signin", response_model=AuthResponse)
async def signin(
    data: AuthRequest,
    session: AsyncSession = Depends(get_session),
):
    statement = select(User).where(User.email == data.email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
        ),
        token=token,
    )


# =========================
# SESSION (JWT HEADER)
# =========================
@router.get("/session", response_model=SessionResponse)
async def get_session_route(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format",
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return SessionResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
        )
    )


# =========================
# SIGN OUT (CLIENT SIDE)
# =========================
@router.post("/signout")
async def signout():
    """
    JWT-based logout is handled on the client
    by removing the token from storage.
    """
    return {"message": "Signed out successfully"}
