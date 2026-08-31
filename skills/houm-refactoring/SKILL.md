---
name: houm-refactoring
description: "Refactor Houmy Python/FastAPI and React/Vite codebase. TRIGGER when: user asks to refactor, clean up, restructure, simplify, or remove dead code. Also triggers on 'implicit code', 'magic', 'coupling', 'discoverability', or 'make explicit'. Covers backend (Python/FastAPI/SQLAlchemy) and frontend (React/TypeScript/Vite)."
---

# Houmy Refactoring Skill

Systematic refactoring for the Houmy RAG chatbot codebase. Replaces implicit/magic patterns with explicit, grep-able, testable code.

## When to Activate

- User asks to refactor, restructure, or clean up code
- Implicit patterns are found (dynamic discovery, string-based dispatch, magic imports)
- Code smells: large files (>800 lines), large functions (>50 lines), deep nesting (>4 levels)
- Dead code removal requests
- Registry/plugin system restructuring
- Coupling reduction between modules

## Core Principles

1. **Explicit over implicit** -- Every registration, dispatch, and dependency must be grep-able
2. **Investigate before cutting** -- Read all usages before removing anything
3. **Atomic changes** -- One refactoring per commit, tests after each
4. **No behavior change** -- Refactoring must not alter external behavior; run `conda run -n houmy pytest` after each step
5. **Preserve the API contract** -- Public endpoints, request/response shapes, and env vars must not change without explicit user approval

## Workflow

### Step 1: Scope and Audit

Identify what to refactor. Run these **in parallel**:

```bash
# File size audit (>400 lines = candidate)
find app/ prompts/ web/src/ -name "*.py" -o -name "*.tsx" -o -name "*.ts" | xargs wc -l | sort -rn | head -20

# Function size audit (Python functions >50 lines)
grep -n "def \|async def " app/**/*.py | head -40

# Import complexity (most-imported modules = high coupling)
grep -rn "^from app\." app/ --include="*.py" | awk -F: '{print $2}' | sort | uniq -c | sort -rn | head -15
```

Categorize findings:

| Category | Risk | Action |
|----------|------|--------|
| Dead code (unused functions/files) | LOW | Delete with test verification |
| Implicit registries (importlib, module scanning) | MEDIUM | Replace with explicit dict/registry |
| God files (>800 lines) | MEDIUM | Extract into focused modules |
| String-based dispatch | MEDIUM | Replace with Strategy or explicit methods |
| Circular imports | HIGH | Restructure dependency graph |
| Public API changes | CRITICAL | Requires user approval |

### Step 2: Plan the Refactoring

**STOP and present the plan to the user.** Include:

1. What will change and why
2. Which files are affected
3. Risk assessment (will tests break? will API change?)
4. Execution order (dependencies first)

**Do NOT proceed without user confirmation.**

### Step 3: Execute Refactorings

Apply one technique at a time from the catalog below. After each:

```bash
# Verify nothing broke
conda run -n houmy pytest

# For frontend changes
cd web && npx tsc --noEmit
```

### Step 4: Verify and Report

```
Refactoring Summary
---------------------------------------
Applied:    [list techniques used]
Files:      [count] modified, [count] new, [count] deleted
Lines:      [net change]
Tests:      All passing
---------------------------------------
```

## Refactoring Catalog

### R1: Replace Magic Registry with Explicit Dict

**When:** Module uses `importlib`, `vars()`, `__dict__` scanning, or convention-based discovery to build registries.

**Before (implicit):**
```python
# Scans module attributes at runtime -- invisible to grep
module = importlib.import_module(f"prompts.{layer_id}")
for attr, value in vars(module).items():
    if isinstance(value, dict):
        return value  # hopes the first dict is the right one
```

**After (explicit):**
```python
# prompt_manager.py -- explicit import, grep-able, type-safe
from prompts.user import USER_PROMPTS
from prompts.system import SYSTEM_PROMPTS

LAYER_REGISTRY: dict[str, dict[str, str]] = {
    "user": USER_PROMPTS,
    "system": SYSTEM_PROMPTS,
}
```

**Checklist:**
- [ ] All consumers updated to use explicit registry
- [ ] Old dynamic discovery code removed
- [ ] Tests pass

### R2: Replace String Dispatch with Strategy Pattern

**When:** Code uses string keys to branch behavior (`if source_type == "pdf"` / `elif ...`).

**Before:**
```python
def process(source_type: str, data):
    if source_type == "pdf":
        return process_pdf(data)
    elif source_type == "url":
        return process_url(data)
    # adding a new type requires modifying this function
```

**After:**
```python
from typing import Protocol

class SourceProcessor(Protocol):
    def process(self, data) -> Result: ...

PROCESSORS: dict[str, SourceProcessor] = {
    "pdf": PdfProcessor(),
    "url": UrlProcessor(),
}

def process(source_type: str, data):
    processor = PROCESSORS.get(source_type)
    if not processor:
        raise ValueError(f"Unknown source type: {source_type}")
    return processor.process(data)
```

### R3: Extract Class / Extract Module

**When:** A file exceeds 800 lines or a class has multiple unrelated responsibilities.

**Rules:**
- New module name must clearly describe its single responsibility
- Move related functions together; don't scatter
- Update all imports in one pass (use grep to find all usages first)
- Re-export from original module if it's a public API (temporary compatibility)

```bash
# Find all files importing from the module you're splitting
grep -rn "from app.services.retrieval import\|from app.services.retrieval " app/ --include="*.py"
```

### R4: Remove Dead Code

**Process (strict order):**

1. **Detect** -- Find candidates:
   ```bash
   # Python: unused imports and variables
   conda run -n houmy ruff check app/ --select F401,F841

   # Grep for function definitions, then check if they're called
   grep -rn "def function_name" app/
   grep -rn "function_name" app/ --include="*.py" | grep -v "def function_name"
   ```

2. **Categorize** by risk:
   - **SAFE**: Private functions (`_helper`), test utilities, unused imports
   - **CAUTION**: Public functions, anything referenced in configs or migrations
   - **DANGER**: Entry points, things that might be called dynamically

3. **Delete one item at a time**, run tests after each deletion

4. **If tests fail**, revert immediately:
   ```bash
   git checkout -- path/to/file.py
   ```

### R5: Flatten Deep Nesting

**When:** Code has >4 levels of nesting.

**Techniques:**
- **Guard clauses**: Return early instead of nesting
- **Extract method**: Pull nested block into named function
- **Invert condition**: Flip `if` to reduce else-nesting

**Before:**
```python
def process(data):
    if data:
        if data.is_valid:
            if data.has_permission:
                result = do_work(data)
                if result:
                    return result
    return None
```

**After:**
```python
def process(data):
    if not data or not data.is_valid or not data.has_permission:
        return None
    result = do_work(data)
    return result if result else None
```

### R6: Stabilize Callback References (React)

**When:** `useCallback` / `useMemo` dependencies cause unnecessary re-renders or effect re-fires.

**Symptoms:** Race conditions in `useEffect`, stale closures, infinite re-render loops.

**Fix patterns:**
- Move stable functions outside component or into `useRef`
- Use functional state updates (`setState(prev => ...)`) to avoid dependency on current state
- Add `useEffect` cleanup with `cancelled` flag for async operations

### R7: Introduce Parameter Object

**When:** Same group of parameters appears across 3+ function signatures.

**Before:**
```python
def fetch_doc(source_id: str, doc_id: str, db: Session): ...
def delete_doc(source_id: str, doc_id: str, db: Session): ...
def update_doc(source_id: str, doc_id: str, db: Session): ...
```

**After:**
```python
class DocumentRef(BaseModel):
    source_id: str
    doc_id: str

def fetch_doc(ref: DocumentRef, db: Session): ...
def delete_doc(ref: DocumentRef, db: Session): ...
def update_doc(ref: DocumentRef, db: Session): ...
```

## Houmy-Specific Patterns

### Prompt System
- Prompt variants live in `prompts/{layer}/` with explicit `DICT_{LAYER}_PROMPTS` dicts
- `PromptManager` should import these dicts directly, not discover them via introspection
- Adding a new variant = add file + add to dict + done (no magic)

### API Routers
- Each router file < 400 lines
- Complex business logic belongs in `app/services/`, not in route handlers
- Use `Depends()` for shared logic (auth, db, pagination)

### Frontend Components
- Each component file < 400 lines
- Extract hooks into `hooks/` when reused across 2+ components
- API calls should use a shared `useApi` pattern, not inline `fetch()` in every component

## Anti-Patterns to Watch For

| Anti-Pattern | Why Bad | Fix With |
|---|---|---|
| `importlib.import_module` for registries | Invisible to grep, fragile | R1: Explicit Dict |
| `vars(module)` scanning | Picks up unintended attributes | R1: Explicit Dict |
| `isinstance` chains for dispatch | Violates Open/Closed principle | R2: Strategy |
| 1000+ line service files | Impossible to navigate | R3: Extract Module |
| `getattr(obj, method_name)()` | Untraceable at static analysis | R2: Explicit Methods |
| Unused imports accumulating | Noise, slower imports | R4: Dead Code |
| `useEffect` without cleanup | Race conditions, memory leaks | R6: Stabilize Callbacks |
