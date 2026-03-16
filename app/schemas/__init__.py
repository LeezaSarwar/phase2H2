# from app.schemas.common import ErrorResponse, HealthResponse
# from app.schemas.task import TaskCreate, TaskUpdate, TaskComplete, TaskResponse, TaskListResponse
# from app.schemas.auth import AuthRequest, UserResponse, AuthResponse

# # __all__ = [
#     "ErrorResponse",
#     "HealthResponse",
#     "TaskCreate",
#     "TaskUpdate",
#     "TaskComplete",
#     "TaskResponse",
#     "TaskListResponse",
#     "AuthRequest",
#     "UserResponse",
#     "AuthResponse",
# # ]




# new
from app.schemas.common import ErrorResponse, HealthResponse
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskComplete,
    TaskResponse,
    TaskListResponse,
)
from app.schemas.auth import (
    AuthRequest,
    AuthResponse,
    UserResponse,
    SessionResponse,
)

__all__ = [
    "AuthRequest",
    "AuthResponse",
    "UserResponse",
    "SessionResponse",
    "ErrorResponse",
    "HealthResponse",
    "TaskCreate",
    "TaskUpdate",
    "TaskComplete",
    "TaskResponse",
    "TaskListResponse",
]


