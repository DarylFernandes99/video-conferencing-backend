# Meet Clone - Backend

FastAPI Backend for Video Conferencing Application with Socket.IO Signaling.

## Architecture
This service follows a **Layered Architecture**:
- **API/Controller Layer**: `main.py` & Socket.IO Event Handlers.
- **Service Layer**: `app/services/signaling_service.py` (Business Logic).
- **Repository Layer**: `app/repositories/room_repository.py` (Redis/DB interactions).

## Tech Stack
- **Framework**: FastAPI + Python-SocketIO.
- **Database**: PostgreSQL (User Config).
- **Cache**: Redis (Room State & Signaling).

## Setup
### Prerequisites
- Python 3.11+
- Redis & Postgres (running via Docker)

### Environment Variables
Create a `.env` file (or use defaults):
```env
DATABASE_URL=postgresql://user:password@localhost:5432/meetdb
REDIS_URL=redis://localhost:6379/0
```

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```