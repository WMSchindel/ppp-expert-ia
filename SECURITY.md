# Security Best Practices

Security hardening guide.

---

## Secrets Management

### Never Commit Secrets

**❌ WRONG:**
```bash
git add .env
echo "DATABASE_URL=postgresql://user:password@host/db" >> config.py
```

**✅ RIGHT:**
```bash
# .gitignore
.env
.env.local
.env.production
*.key
*.pem
secrets/
```

### Environment Variables

Store secrets in environment:

```bash
# .env.local (not committed)
DATABASE_URL=postgresql://user:password@localhost:5432/ppp_db
SECRET_KEY=your-secret-key-here
API_KEY=external-service-key
```

### Rotate Secrets Regularly

```bash
# Change passwords every 90 days
# Rotate API keys every 180 days
# Update database credentials on team changes
```

---

## SQL Injection Prevention

### Current Protection

Using SQLAlchemy ORM prevents SQL injection:

```python
# ✅ SAFE: ORM parameterizes
usuario = db.query(UsuarioModel).filter(
    UsuarioModel.email == user_email
).first()

# ❌ UNSAFE: String concatenation
usuario = db.execute(f"SELECT * FROM usuarios WHERE email = '{user_email}'")
```

### Best Practices

- Never use f-strings in SQL
- Always use ORM or parameterized queries
- Validate input at API boundary

---

## Cross-Site Scripting (XSS)

### Current Protection

FastAPI automatically escapes JSON responses:

```python
# ✅ SAFE: Automatically escaped
@app.get("/usuarios")
def get_usuarios():
    return {"usuarios": [{"nome": "<script>alert('xss')</script>"}]}
```

### When Adding HTML/Templates

Use Jinja2 auto-escaping:

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates", auto_escape=True)
```

---

## Cross-Site Request Forgery (CSRF)

### Stateless API (No CSRF Risk)

Current design uses stateless authentication:
- No cookies/sessions
- Each request authenticated independently
- CSRF not applicable for REST APIs with OAuth2

### If Adding Forms

```python
from fastapi_csrf_protect import CsrfProtect

@app.post("/form")
async def submit_form(csrf_protect: CsrfProtect = Depends()):
    # Validates CSRF token automatically
    ...
```

---

## Authentication & Authorization

### Current State

No authentication yet. Planned for CF-015+.

### Implementation Plan

1. **JWT Tokens:**
   ```python
   from fastapi.security import OAuth2PasswordBearer
   
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
   ```

2. **Role-Based Access Control (RBAC):**
   ```python
   class Role(Enum):
       ADMIN = "admin"
       USER = "user"
       VIEWER = "viewer"
   ```

3. **API Key for Services:**
   ```python
   API_KEY = os.getenv("API_KEY")
   
   async def validate_api_key(key: str = Header()):
       if key != API_KEY:
           raise HTTPException(status_code=403)
   ```

---

## Dependency Vulnerabilities

### Check Dependencies

```bash
pip install safety

safety check  # Check for known vulnerabilities
```

### Keep Dependencies Updated

```bash
# Show outdated packages
pip list --outdated

# Update specific package
pip install --upgrade sqlalchemy

# Update all
pip install --upgrade -r requirements.txt
```

### Recommended Updates

Check monthly:
- Security advisories for Python packages
- Database version updates
- Framework updates

---

## Data Protection

### Sensitive Data Handling

**Email & CPF are protected:**
- Validated with strong rules
- Cannot be NULL
- Unique constraints prevent duplicates
- Only lowercase emails stored

### Encryption (Future)

For sensitive fields:

```python
from cryptography.fernet import Fernet

class EncryptedString(str):
    def __new__(cls, value):
        cipher = Fernet(ENCRYPTION_KEY)
        return cipher.encrypt(value.encode())
```

### Data Retention

- Deleted usuarios marked `ativo=False`
- Actually delete data monthly
- Backup retention: 30 days
- Log retention: 90 days

---

## API Security

### Rate Limiting

Prevent brute force attacks:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/usuarios")
@limiter.limit("100/minute")
def listar_usuarios():
    ...
```

### Input Validation

All inputs validated via Pydantic:

```python
class CriarUsuarioRequest(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    email: EmailStr  # Validates email format
    cpf: str = Field(..., pattern=r"^\d{11}$")
```

### Output Filtering

Never return sensitive data:

```python
# ❌ WRONG: Returns password
class UsuarioResponse(BaseModel):
    nome: str
    password: str  # Never!
    
# ✅ RIGHT: Only public fields
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
```

---

## HTTPS/TLS

### Development

HTTP fine (localhost only).

### Production

**Always use HTTPS:**

```python
# Redirect HTTP to HTTPS
@app.middleware("http")
async def https_redirect(request, call_next):
    if request.url.scheme == "http" and request.url.hostname != "localhost":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=url, status_code=301)
    return await call_next(request)
```

**Setup:**
- Use Let's Encrypt (free SSL certificates)
- Nginx/Apache as reverse proxy
- Auto-renew certificates

---

## Logging Security

### Don't Log Sensitive Data

**❌ WRONG:**
```python
logger.info(f"Login attempt: username={user}, password={password}")
```

**✅ RIGHT:**
```python
logger.info(f"Login attempt: username={user}")
```

### Secure Log Storage

- Store logs on secure server
- Encrypt logs at rest
- Restrict access (ACLs)
- Regular backups

---

## Database Security

### PostgreSQL Hardening

```sql
-- Use strong passwords
ALTER USER ppp_user WITH PASSWORD 'very-strong-password';

-- Restrict connections
-- (in postgresql.conf)
# host  all  all  127.0.0.1/32  md5

-- Create read-only user for reporting
CREATE USER read_only WITH PASSWORD 'password';
GRANT USAGE ON SCHEMA public TO read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;
```

### Backup Security

- Encrypt backups
- Store off-site
- Test recovery regularly

---

## Code Security

### Use Security Linters

```bash
# Check for common security issues
pip install bandit
bandit -r src/
```

### Code Review

All PRs must be reviewed for:
- No hardcoded secrets
- Proper input validation
- No SQL injection
- Secure error messages

### Dependency Scanning

```bash
# GitHub automatically scans dependencies
# Also run locally:
pip install safety
safety check
```

---

## Incident Response

### Security Breach Procedure

1. **Immediate:**
   - Stop the bleeding (take affected service offline if needed)
   - Notify all users
   - Preserve evidence

2. **Investigation:**
   - Determine what was compromised
   - Root cause analysis
   - Timeline reconstruction

3. **Recovery:**
   - Reset all passwords
   - Rotate all keys/tokens
   - Deploy security patch

4. **Post-Mortem:**
   - Document lessons learned
   - Update security procedures
   - Implement preventive measures

---

## Security Checklist

- [ ] All secrets in environment variables
- [ ] `.env` files in `.gitignore`
- [ ] Dependencies up-to-date
- [ ] No hardcoded credentials
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (JSON auto-escape)
- [ ] HTTPS in production
- [ ] Rate limiting configured
- [ ] Secure logging (no sensitive data)
- [ ] Access controls implemented
- [ ] Backups encrypted and tested
- [ ] Security headers configured

---

## Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/
- **SQLAlchemy Security:** https://docs.sqlalchemy.org/en/20/faq/security.html

---

**Last Updated:** 2026-07-10
