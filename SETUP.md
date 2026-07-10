# Setup Guide

Developer setup instructions for PPP Expert IA.

---

## Prerequisites

- Python 3.13+
- PostgreSQL 16+ (for production)
- SQLite 3 (included with Python)
- Git

### Install Python

**Windows:**
```bash
winget install Python.Python.3.13
```

**macOS:**
```bash
brew install python@3.13
```

**Linux:**
```bash
sudo apt-get install python3.13 python3.13-venv
```

### Verify Installation

```bash
python --version  # Should be 3.13+
pip --version     # Should be included
```

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/WMSchindel/ppp-expert-ia.git
cd ppp-expert-ia
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

Main dependencies:
- fastapi (web framework)
- uvicorn (ASGI server)
- sqlalchemy (ORM)
- pydantic (validation)
- loguru (logging)
- pytest (testing)

### 4. Environment Configuration

Create `.env.local`:

```bash
APP_NAME=PPP Expert IA
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///development.db
```

### 5. Database Initialization

```bash
python -c "from src.infrastructure.persistence.database import init_db; init_db()"
```

### 6. Run Tests

```bash
# Run all tests
pytest -v

# With coverage
pytest --cov=src
```

### 7. Run Development Server

```bash
uvicorn src.main:app --reload
```

Server: http://localhost:8000  
Docs: http://localhost:8000/docs

---

## Environment Variables

### Development

```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///development.db
```

### Testing

```bash
ENVIRONMENT=test
DATABASE_URL=sqlite:///:memory:
```

### Production

```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:password@host:5432/ppp_db
```

---

## IDE Setup

### VS Code

Install extensions:
- Python (Microsoft)
- Pylance
- Pytest
- SQLite Viewer

### PyCharm

File → Settings → Project → Python Interpreter → Add `.venv/bin/python`

---

## Database Setup

### SQLite (Development)

Already configured. Uses `development.db`.

### PostgreSQL (Production)

```bash
createdb ppp_db
createuser ppp_user
psql -d ppp_db -c "GRANT ALL PRIVILEGES ON DATABASE ppp_db TO ppp_user;"
```

Update `.env`:
```bash
DATABASE_URL=postgresql://ppp_user:password@localhost:5432/ppp_db
```

---

## First Steps

1. Clone and setup venv
2. Install dependencies: `pip install -e .`
3. Run tests: `pytest -v`
4. Start server: `uvicorn src.main:app --reload`
5. Visit http://localhost:8000/docs
6. Try creating a usuario via API
7. Start developing!

---

**Last Updated:** 2026-07-10
