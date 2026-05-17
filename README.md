---
title: Todo API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false.
---

# Todo API Backend

FastAPI backend for the Todo application


## API Endpoints

### Health Check
- `GET /health` - Check API health status

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Tasks
- `GET /tasks` - List all tasks (requires auth)
- `POST /tasks` - Create new task (requires auth)
- `PUT /tasks/{task_id}` - Update task (requires auth)
- `DELETE /tasks/{task_id}` - Delete task (requires auth)
- `PATCH /tasks/{task_id}/toggle` - Toggle task completion (requires auth)

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing

Optional:
- `FRONTEND_URL` - Frontend URL (default: http://localhost:3000)
- `CORS_ORIGINS` - Comma-separated list of allowed origins (default: http://localhost:3000)
"# backend-todo-python-render" 
"# phase2H2" 
