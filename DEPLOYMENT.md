# Deployment Strategy

Guide for running the application in different environments.

---

## Environment Management

### Environment Files

```
project/
├── .env.local              # Development (git ignored)
├── .env.test              # Testing (committed)
└── .env.production        # Production (git ignored)
```

### Configuration Hierarchy

Higher priority overrides lower:

```
1. Environment variables (highest)
   PYTHONPATH, LOG_LEVEL, etc
   
2. .env file
   APP_NAME=PPP
   ENVIRONMENT=development
   
3. Defaults in code (lowest)
   class Settings:
       app_name: str = "PPP Expert IA"
       environment: str = "development"
```

### Current .env.test (Committed)

```bash
# Application
APP_NAME=PPP Expert IA
ENVIRONMENT=test
DEBUG=false

# Logging
LOG_LEVEL=DEBUG
LOGS_PATH=./data/logs

# Database (future)
DATABASE_URL=sqlite:///test.db
```

---

## Running Locally

### 1. Setup

```bash
# Clone repository
git clone https://github.com/WMSchindel/ppp-expert-ia.git
cd ppp-expert-ia

# Create virtual environment
python -m venv .venv

# Activate venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Configuration

Create `.env.local`:

```bash
APP_NAME=PPP Expert IA
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
LOGS_PATH=./data/logs
```

### 3. Run Tests

```bash
# All tests
pytest -v

# Specific test file
pytest tests/unit/domain/ -v

# With coverage
pytest --cov=src tests/
```

### 4. Run Application

```bash
# Will be available after CF-012 (HTTP framework integration)
python -m src.main
```

---

## Testing Environment

### Test Configuration (.env.test)

```bash
ENVIRONMENT=test
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///:memory:
```

### Running Tests

```bash
# All tests
pytest -v

# Specific suite
pytest tests/unit/ -v
pytest tests/integration/ -v

# Watch mode (requires pytest-watch)
ptw -v

# Coverage report
pytest --cov=src --cov-report=html
```

### GitHub Actions CI

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: pip install -e .
      - run: pytest -v
```

---

## Production Deployment

### Architecture

```
┌──────────────────┐
│   Load Balancer  │
└────────┬─────────┘
         │
┌────────▼────────────────────────┐
│  API Server (FastAPI)           │
│  - Port 8000                    │
│  - Gunicorn/Uvicorn            │
│  - Multiple workers             │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│  PostgreSQL Database            │
│  - Port 5432                    │
│  - Automated backups            │
│  - Replication (optional)       │
└─────────────────────────────────┘
```

### Environment Variables (Production)

```bash
# Application
APP_NAME=PPP Expert IA
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY=<generated-random-key>

# Logging
LOG_LEVEL=INFO
LOGS_PATH=/var/log/ppp-expert-ia

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/ppp_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# CORS
CORS_ORIGINS=https://example.com

# External Services
SENTRY_DSN=https://...
```

### Deployment Steps

#### 1. Prepare Server

```bash
# SSH into production server
ssh user@prod-server

# Create application directory
mkdir -p /opt/ppp-expert-ia
cd /opt/ppp-expert-ia

# Create Python virtual environment
python3.13 -m venv venv
source venv/bin/activate
```

#### 2. Deploy Code

```bash
# Clone or pull latest
git clone https://github.com/WMSchindel/ppp-expert-ia.git code
cd code

# Install dependencies
pip install -e .

# Run migrations (when database is ready)
alembic upgrade head
```

#### 3. Configure Application

```bash
# Create .env file with production secrets
nano /opt/ppp-expert-ia/.env.production

# Copy to application directory
cp .env.production code/.env
```

#### 4. Run Application

```bash
# With Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 src.main:app

# Or with Uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

#### 5. Setup Reverse Proxy (Nginx)

```nginx
upstream ppp_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://ppp_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 6. Enable HTTPS

```bash
# Use Let's Encrypt
certbot certonly --standalone -d api.example.com
certbot renew  # Automated renewal
```

### Database Setup (Production)

#### PostgreSQL Installation

```bash
# Docker
docker run -d \
  --name ppp-db \
  -e POSTGRES_USER=ppp_user \
  -e POSTGRES_PASSWORD=<secure-password> \
  -e POSTGRES_DB=ppp_db \
  -v ppp-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16

# Backup strategy
pg_dump -U ppp_user ppp_db > backup.sql
```

#### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add Usuario table"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## Logging Strategy

### Development

```bash
# Console output
# Level: DEBUG
# Format: colored, detailed

# Example output:
2026-07-09 10:23:45.123 | DEBUG    | src.domain.entities.usuario:__init__:45 - Usuario criado
```

### Production

```bash
# File output
# Location: /var/log/ppp-expert-ia/app.log
# Level: INFO
# Rotation: daily, 30-day retention
# Format: JSON for log aggregation

# Example:
{
  "timestamp": "2026-07-09T10:23:45.123Z",
  "level": "INFO",
  "logger": "src.domain.entities.usuario",
  "message": "Usuario criado",
  "usuario_id": 1,
  "env": "production"
}
```

### Monitoring Logs

```bash
# Watch logs in real-time
tail -f /var/log/ppp-expert-ia/app.log

# Search for errors
grep "ERROR" /var/log/ppp-expert-ia/app.log

# Log aggregation (ELK Stack, Datadog, etc)
# Ship logs to centralized system
```

---

## Monitoring & Observability

### Health Check Endpoint

```python
# GET /health
{
  "status": "ok",
  "uptime": 3600,
  "database": "connected",
  "version": "0.1.0"
}
```

### Metrics to Track

```python
# Application metrics
- Request latency (p50, p95, p99)
- Error rate
- Active usuarios
- Database query time

# System metrics
- CPU usage
- Memory usage
- Disk space
- Network I/O
```

### Alerting

```yaml
# Example alert rules
- Alert if error_rate > 5%
- Alert if latency_p95 > 1000ms
- Alert if disk_space < 10%
- Alert if database_connections > 50
```

---

## Scaling Strategy

### Phase 1: Single Server (Current)

```
User → Single Server (API + DB)
```

**Suitable for:** < 100 concurrent users

### Phase 2: Separate Database

```
User → API Server → PostgreSQL (separate)
```

**Suitable for:** < 500 concurrent users

### Phase 3: Multiple API Servers

```
User → Load Balancer → API 1
                    → API 2
                    → API 3
        └→ PostgreSQL
```

**Suitable for:** < 5000 concurrent users

### Phase 4: Microservices

```
User → API Gateway → User Service
                  → Project Service
                  → Report Service
                  → ...
        └→ Shared Database
```

**Suitable for:** > 5000 concurrent users, complex domains

---

## Backup & Recovery

### Automated Backups

```bash
# Daily at 2 AM
0 2 * * * pg_dump -U ppp_user ppp_db | gzip > /backups/ppp_db_$(date +\%Y\%m\%d).sql.gz

# Keep 30 days of backups
find /backups -name "ppp_db_*.sql.gz" -mtime +30 -delete
```

### Disaster Recovery

```bash
# Restore from backup
gunzip < /backups/ppp_db_20260709.sql.gz | psql -U ppp_user ppp_db

# Verify restored data
psql -U ppp_user ppp_db -c "SELECT COUNT(*) FROM usuarios;"
```

---

## Security

### Environment Variables

Never commit secrets to git:

```bash
# ❌ WRONG
.env  # Contains DATABASE_URL, SECRET_KEY, etc

# ✅ RIGHT
.env.local           # git ignored
.env.production      # git ignored, in secure vault
.env.test            # OK to commit (no secrets)
```

### Database

```bash
# Use strong passwords
PASSWORD=$(openssl rand -base64 32)

# Use connection pooling
DATABASE_POOL_SIZE=20

# Encrypt sensitive data at rest
# (Implement in CF-012+)
```

### API Security

```bash
# HTTPS only
SECURE_SSL_REDIRECT=true

# CORS
CORS_ORIGINS=https://example.com

# Rate limiting
# (Implement in CF-012+)

# API keys
# (Implement in CF-012+)
```

---

## Troubleshooting

### Common Issues

**1. "Module not found: src"**
```bash
# Make sure .venv is activated
source .venv/bin/activate

# Make sure conftest.py exists in root
ls conftest.py
```

**2. "Database connection refused"**
```bash
# Check PostgreSQL is running
psql -U postgres

# Check connection string
echo $DATABASE_URL
```

**3. "Port 8000 already in use"**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
gunicorn -b 0.0.0.0:8001
```

---

## Deployment Checklist

- [ ] Tests passing (pytest -v)
- [ ] Type checking (mypy src/)
- [ ] Secrets configured (.env files)
- [ ] Database migrations applied (alembic upgrade head)
- [ ] Health check working (GET /health)
- [ ] Logs configured
- [ ] Backups scheduled
- [ ] Monitoring alerts enabled
- [ ] SSL certificate valid
- [ ] Rollback plan documented

---

**Last Updated:** 2026-07-09
