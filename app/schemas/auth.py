# from pydantic import BaseModel, EmailStr, Field
# from typing import Optional


# class AuthRequest(BaseModel):
#     """Request schema for authentication."""

#     email: EmailStr
#     password: str = Field(..., min_length=8)


# class UserResponse(BaseModel):
#     """Response schema for user data."""

#     id: str
#     email: str
#     name: Optional[str] = None


# class AuthResponse(BaseModel):
#     """Response schema for authentication."""

#     user: UserResponse
#     token: str  # JWT token for client-side storage

# new
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None


class AuthResponse(BaseModel):
    user: UserResponse
    token: str


class SessionResponse(BaseModel):
    user: UserResponse


