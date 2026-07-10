# Contributing Guide

How to contribute to PPP Expert IA.

---

## Code Style

### Python

Follow **PEP 8** and **Black** formatter.

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/
```

### Type Hints

All functions must have type hints:

```python
def criar_usuario(self, nome: str, email: str) -> Usuario:
    """Create usuario."""
    ...
```

### Naming Conventions

- **Classes:** PascalCase (`UsuarioController`)
- **Functions:** snake_case (`criar_usuario`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_UPLOAD_SIZE`)
- **Private:** `_leading_underscore`

---

## Git Workflow

### Branch Naming

```
feature/description      # New feature
fix/description         # Bug fix
docs/description        # Documentation
refactor/description    # Code refactoring
test/description        # Tests
```

### Commit Messages

Format: `<type>: <description>`

```
feat: add usuario email validation
fix: correct CPF checksum algorithm
docs: update API documentation
refactor: simplify repository interface
test: add more edge case tests
```

**Message guidelines:**
- Start with verb in imperative mood
- Lowercase (except proper nouns)
- 50 characters or less
- Explain WHY, not WHAT

### Pull Request Process

1. **Create feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and commit:**
   ```bash
   git add src/
   git commit -m "feat: my feature"
   ```

3. **Push and create PR:**
   ```bash
   git push origin feature/my-feature
   ```

4. **Write PR description** following template

5. **Wait for review** and CI to pass

6. **Address feedback** with new commits

7. **Merge** when approved

---

## PR Description Template

```markdown
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
- [ ] Tests added
- [ ] Tests passing
- [ ] Manual testing done

## Related
Fixes #123
```

---

## Code Review Checklist

Before submitting PR, ensure:

- [ ] Code follows PEP 8
- [ ] Type hints on all functions
- [ ] Tests added for new code
- [ ] All tests passing
- [ ] No console.log/print statements
- [ ] No hardcoded secrets
- [ ] Documentation updated
- [ ] Commit messages clear

---

## Testing Requirements

**For any PR:**
- All existing tests must pass
- New tests for new functionality
- Target 90%+ code coverage

```bash
# Before pushing
pytest -v --cov=src
```

---

## Documentation

### Code Comments

Only explain WHY, not WHAT:

```python
# ✅ GOOD: Explains why
# We validate uniqueness here instead of in UseCase
# to prevent bypassing via direct Repository call
if self._existe_email(email):
    raise ValueError("Email já existe")

# ❌ BAD: Just repeats code
# Check if email exists
if self._existe_email(email):
    raise ValueError("Email já existe")
```

### Docstrings

One-liner for simple functions:

```python
def desativar(self) -> None:
    """Mark usuario as inactive."""
    self.ativo = False
```

---

## Adding New Features

### Step 1: Create Specification

Write REQ-XXXX.md in `docs/05_REQUISITOS/`:

```markdown
# Objective
What is this feature?

# Implementation Plan
How will we build it?

# Tests
What tests are needed?
```

### Step 2: Write Tests First

TDD approach:

```python
def test_novo_recurso():
    """Test new feature."""
    resultado = novo_recurso()
    assert resultado is not None
```

### Step 3: Implement Feature

Make tests pass:

```python
def novo_recurso():
    return "implementacao"
```

### Step 4: Document

Update API.md, SETUP.md, etc.

### Step 5: Submit PR

---

## Reporting Issues

### Bug Report Template

```markdown
## Description
What is the bug?

## Steps to Reproduce
1. Do this
2. Then this
3. See error

## Expected Behavior
What should happen?

## Actual Behavior
What actually happened?

## Environment
- OS: Windows 11
- Python: 3.13
- Browser: Chrome
```

---

## Release Process

Before releasing new version:

1. Update VERSION in code
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.2.0`
4. Create GitHub release
5. Announce in docs

---

## Community Guidelines

- Be respectful
- Assume good intent
- Provide constructive feedback
- Help others learn

---

**Last Updated:** 2026-07-10
