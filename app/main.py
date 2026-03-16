from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from app.config import get_settings
from app.schemas import HealthResponse
from app.routes import auth, tasks


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="Todo API",
    description="RESTful API for the Phase II Full-Stack Todo Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS - allow frontend origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global exception handler to ensure CORS headers are always sent
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return proper CORS headers."""
    print(f"Unhandled exception: {exc}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("Origin", "http://localhost:3000"),
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")
