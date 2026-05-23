# Web-Based TODO Application - Backend

FastAPI backend for the TODO application.

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows (Git Bash)
source venv/Scripts/activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/complete` - Mark task as complete
- `DELETE /api/tasks/{id}` - Delete a task

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Project Structure

```
backend/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── api/             # FastAPI routes and schemas
├── tests/               # Test files
├── data/                # Task storage (created at runtime)
└── requirements.txt     # Python dependencies
```

## Data Storage

Tasks are stored in `data/tasks.json` in JSON format. The file is created automatically on first run.
