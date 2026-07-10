# Troubleshooting Guide

Solutions to common problems.

---

## Python & Environment

### ImportError: No module named 'src'

**Problem:** Tests or app fail to import `src` module.

**Solutions:**

1. **Ensure `.venv` activated:**
   ```bash
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. **Ensure `conftest.py` exists in project root:**
   ```bash
   ls conftest.py  # Should exist
   ```

3. **Reinstall dependencies:**
   ```bash
   pip install -e .
   ```

---

### ModuleNotFoundError: No module named 'fastapi'

**Problem:** FastAPI not installed.

**Solution:**
```bash
pip install fastapi uvicorn
```

---

### Pydantic Deprecation Warnings

**Warning:**
```
Support for class-based `config` is deprecated
```

**Status:** Safe to ignore. Will be fixed in next Pydantic update.

**Suppress:**
```bash
pytest -W ignore::DeprecationWarning
```

---

## Database Issues

### SQLite Database is Locked

**Problem:** Error: `database is locked`

**Causes:**
- Another process accessing database
- Stale connection
- Incomplete transaction

**Solutions:**

1. **Delete lock file:**
   ```bash
   rm development.db-journal
   ```

2. **Close all connections:**
   - Stop running app
   - Close any open database tools

3. **Restart database:**
   ```bash
   rm development.db
   ```

---

### No such table: usuarios

**Problem:** `(sqlite3.OperationalError) no such table: usuarios`

**Solution:**

Initialize database:
```bash
python -c "from src.infrastructure.persistence.database import init_db; init_db()"
```

---

### PostgreSQL Connection Refused

**Problem:** `(psycopg2.OperationalError) could not connect to server`

**Causes:**
- PostgreSQL not running
- Wrong connection string
- Wrong credentials

**Solutions:**

1. **Check PostgreSQL running:**
   ```bash
   # Windows
   pg_isready -h localhost
   
   # macOS
   brew services list
   ```

2. **Check connection string:**
   ```bash
   # Format: postgresql://user:password@host:port/database
   # Example: postgresql://ppp_user:password@localhost:5432/ppp_db
   ```

3. **Create database/user:**
   ```bash
   createdb ppp_db
   createuser ppp_user
   ```

---

## FastAPI Issues

### Port 8000 Already in Use

**Problem:** `Address already in use`

**Solutions:**

1. **Kill process on port:**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -i :8000
   kill -9 <PID>
   ```

2. **Use different port:**
   ```bash
   uvicorn src.main:app --port 8001 --reload
   ```

---

### Cannot Import App from main.py

**Problem:** `ImportError: cannot import name 'app' from 'src.main'`

**Causes:**
- Circular imports
- main.py has syntax error

**Solutions:**

1. **Check main.py syntax:**
   ```bash
   python -m py_compile src/main.py
   ```

2. **Check for circular imports:**
   - Look for imports at top level
   - Move imports inside functions if needed

---

## Testing Issues

### Tests Fail Locally But Pass in CI

**Common Causes:**
- Missing environment variables
- Different Python versions
- Timing/race conditions
- Unset database state

**Solutions:**

1. **Set required env vars:**
   ```bash
   export ENVIRONMENT=test
   export DATABASE_URL=sqlite:///:memory:
   pytest -v
   ```

2. **Reset database state:**
   ```bash
   pytest --forked  # Isolate each test
   ```

---

### Slow Tests

**Problem:** Tests take > 5 seconds.

**Debug:**
```bash
pytest --durations=10
```

Shows 10 slowest tests.

**Optimize:**
- Mock I/O operations
- Use in-memory database
- Avoid database calls in unit tests
- Cache expensive setup

---

### Test Fails Only Sometimes (Flaky Test)

**Causes:**
- Timing dependencies
- Shared state between tests
- Random data

**Solutions:**

1. **Fix shared state:**
   ```python
   @pytest.fixture
   def repo():
       return UsuarioRepository()  # Fresh instance per test
   ```

2. **Avoid timing assumptions:**
   ```python
   # ❌ BAD: Depends on timing
   # ✅ GOOD: Checks state, not time
   assert usuario.data_criacao is not None
   ```

---

## Logging Issues

### No Log Output

**Problem:** Logger not outputting anything.

**Causes:**
- LOG_LEVEL too high
- Loguru not configured

**Solutions:**

1. **Check LOG_LEVEL:**
   ```bash
   echo $LOG_LEVEL  # Should be DEBUG or INFO
   ```

2. **Set in `.env.local`:**
   ```bash
   LOG_LEVEL=DEBUG
   ```

---

### Too Much Log Output

**Problem:** Console flooded with debug logs.

**Solution:**
```bash
# In .env.local
LOG_LEVEL=INFO
```

---

## Performance Issues

### App Startup Slow

**Debug:**
```bash
time uvicorn src.main:app --reload
```

**Optimize:**
- Remove unnecessary imports from main.py
- Lazy-load heavy dependencies

---

### API Requests Slow

**Debug:**
```bash
pytest --durations=10 tests/integration/
```

**Optimize:**
- Add database indexes
- Optimize queries
- Use connection pooling

---

## Git Issues

### Cannot Push (Permission Denied)

**Problem:** `fatal: Authentication failed`

**Solutions:**

1. **Check credentials:**
   ```bash
   git config user.name
   git config user.email
   ```

2. **Setup SSH key:**
   ```bash
   ssh-keygen -t ed25519
   # Add public key to GitHub
   git remote set-url origin git@github.com:WMSchindel/ppp-expert-ia.git
   ```

---

### Merge Conflicts

**Problem:** Multiple changes to same file.

**Solution:**
```bash
# View conflicts
git status

# Edit conflicted files (remove <<<< >>>> markers)

# Mark as resolved
git add <file>
git commit
```

---

## IDE Issues

### PyCharm Can't Find Interpreter

**Solution:**
1. Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select Existing Environment
4. Choose `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)

---

### VS Code IntelliSense Not Working

**Solutions:**

1. **Install Pylance extension**
2. **Set interpreter in settings.json:**
   ```json
   {
     "python.defaultInterpreterPath": ".venv/bin/python"
   }
   ```
3. **Reload window:** Ctrl+Shift+P → Developer: Reload Window

---

## Getting Help

1. **Check documentation first:**
   - SETUP.md (setup issues)
   - TESTING.md (test failures)
   - API.md (API questions)

2. **Search existing issues:**
   - GitHub Issues

3. **Create new issue if not found:**
   - Include error message
   - Include steps to reproduce
   - Include environment (Python version, OS)

---

**Last Updated:** 2026-07-10
