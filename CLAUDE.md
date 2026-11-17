# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This file is the single source of truth for project conventions. All agents inherit these rules.

---

## Project Overview
Velo Supervisor 2000 is a FastAPI + Bootstrap web application for tracking bicycle component lifecycles using Strava activity data.

**Tech Stack:**
- Backend: Python, FastAPI, SQLite with Peewee ORM
- Frontend: Bootstrap 5, Jinja2 templates (server-side rendered), vanilla JavaScript, TomSelect for multi-select dropdowns
- Integration: Strava API
- Deployment: Docker (optional), local development with uvicorn

---

## Communication & Output Rules

These rules apply to ALL agents and Claude Code itself.

- **Be concise.** Short sentences, no filler, no restating what's already known.
- **Handovers: max 100 lines.** Focus on decisions made, files changed, and what the next agent needs. No preambles, no project summaries, no repeating CLAUDE.md content.
- **No redundant context.** Don't restate project architecture, tech stack, or patterns already documented here.
- **Progress updates: 1-2 sentences max.** Don't narrate every step you take.
- **No inline code comments,** except where the file already has that pattern (e.g. section comments in `main.py`, `Dockerfile`). Explanations of non-obvious logic go in the docstring. No boilerplate docstrings.
- **Don't repeat yourself.** If something is in CLAUDE.md, reference it - don't rewrite it.

---

## Architecture Overview

### Project Structure
- **`src/velo_supervisor/`**: the app as the package `velo_supervisor` (FastAPI, Jinja2 templates in `templates/`, JavaScript and CSS in `static/js/` and `static/css/`)
- **`config/`**: what an installation starts from: `config.json.example`, `strava_tokens.example.json`, `uvicorn_log_config.ini`, `template_db.sqlite`
- **`scripts/`**: `create-container-vs2000.sh` and `integrity/` (result extractor, comparison against `master`, deltas)
- **`tests/`**: pytest suite, see `tests/README.md`
- **`docs/`**: diagrams and `superpowers/` specs and plans (the rewrite roadmap and stage designs)
- **`.github/`**: CI workflow `tests.yml`, `dependabot.yml`, `release.yml`
- **Database**: SQLite with Peewee ORM. **External API**: Strava

### Core Components
- **`main.py`**: FastAPI route handlers and application setup
- **`business_logic.py`**: Core application logic and data processing
- **`database_manager.py`**: Database operations and queries
- **`database_model.py`**: Peewee ORM models
- **`strava.py`**: Strava API integration
- **`middleware.py`**: Custom middleware for request/response handling
- **`utils.py`**: Utility functions including configuration management
- **`main.js`**: Contains all javascript code. All javascript should be placed in this file.
- **`custom_styles.css`**: Contains all CSS code. All CSS should be placed in this file.

### Configuration
- **Required files**:
  - `config.json` (paths to database and Strava tokens), found through the environment variable `VELO_SUPERVISOR_CONFIG`, default `config.json` in the working directory. Locally: the project root (gitignored). Docker: `/data/config.json`
  - External Strava tokens file (location specified in config.json)
  - SQLite database file (location specified in config.json)
- **Template files**: `config/config.json.example` and `config/strava_tokens.example.json`
- **Version**: from the git tag through `hatch-vcs`, read with `importlib.metadata` (`utils.get_current_version()`). There is no version file

### Key Features
- **Component tracking**: Bicycle component lifetime and service intervals
- **Collections**: Group components for bulk operations (e.g., seasonal wheelsets)
- **Strava integration**: Automatic activity data sync
- **Incident reports**: Track maintenance issues
- **Workplans**: Maintenance scheduling with Markdown support
- **Service history**: Component maintenance records

---

## Development Commands

### Running the Application
- **Development (local)**: From the project root, run: `uv run uvicorn velo_supervisor.main:app --log-config config/uvicorn_log_config.ini`
- **Docker deployment**: `scripts/create-container-vs2000.sh` builds the image from `Dockerfile` and starts the container. The image is multi-stage and runs as UID 1000; `/data` (database, `config.json`, logs) and `/secrets` (Strava tokens) are bind mounts
- **Server runs on**: Port 8000 (http://localhost:8000)

### Dependencies
- **Install Python dependencies**: `uv sync` from the project root (creates `.venv` from `uv.lock` and installs `velo_supervisor` into it). Add packages with `uv add` (`uv add --dev` for test tools), never edit `uv.lock` by hand
- **Python version**: 3.12 (as specified in `Dockerfile`, `pyproject.toml` requires 3.11+)

### Database Operations
- **Database migration**: Run `uv run python -m velo_supervisor.db_migration` for schema updates between versions. It does not read `config.json`; it searches the user's home folders for the database and asks
- **Template database**: Located at `config/template_db.sqlite`, the starting database for new installs and for the tests

### Testing
- **Run**: `uv run pytest -q` (about 290 tests, a few minutes). Coverage: `uv run pytest --cov=velo_supervisor --cov-report=term-missing`. Lint: `uv run ruff check && uv run ruff format --check`
- **What they pin**: characterisation tests compare recalculation and every write operation on a synthetic dataset, with the clock fixed at 2026-11-16 12:00 UTC, against expected-result files. Rule, page render, Strava sync, health and migration tests cover the rest. Details in `tests/README.md`
- **Comparison against `master`**: `uv run python scripts/integrity/compare.py --ref master --db <copy> --out-dir <folder outside the repo>` on a local copy of the production database. The database and outputs are never committed (public repository)

### CI and workflow
- CI (`.github/workflows/tests.yml`) runs `test`, `lint` and `docker` on every push and pull request. Tests and lint pass locally before a pull request is opened, and CI is green before it is merged
- Feature branches come off `dev`. `master` and `staging` accept changes only through pull requests, admins included (branch protection, 0 approvals). Required checks (`test`, `lint`, `docker`) are switched on for `staging` after the next `dev` → `staging` merge, and for `master` at switch-over (Stage 6)
- Lint scope is `tests/` and `scripts/`. App modules join the scope as Stage 4 rewrites them
- Expected-result files (`tests/fixtures/expected/`) are never overwritten. Changing one means deleting it by hand with a documented reason (issue or feature) and recording it again with `RECORD_EXPECTED=1`
- Run `scripts/integrity/compare.py --ref master --db <copy>` whenever a change touches calculations. Any difference must trace back to a documented feature change
- Releases are made on the GitHub Releases page (tag `vX.Y.Z`, target `master`, generated notes sorted by `.github/release.yml`). Pull requests that need a database migration get the `breaking-change` label
- New issues go on the project "Sprintboard Velo Supervisor 2000" (#2) with a Priority
- Commit messages reference issues with "Refs #N", never "Closes" or "Fixes". The user closes issues
- Dependabot pull requests (weekly, grouped, targeting `dev`) go through CI like any other change

---

## Sub-Agent Team

### Available Agents
1. **@product-manager** - Requirements gathering, user stories, and feature scoping (interactive)
2. **@architect** - System design and architecture decisions
3. **@ux-designer** - UI/UX design and specifications
4. **@fullstack-developer** - Full-stack implementation (Python + templates)
5. **@database-expert** - Database schema and migrations
6. **@code-reviewer** - Code quality and best practices
7. **@docs-maintainer** - Documentation and commit messages

Agents will follow their defined roles and responsibilities as documented in their respective files in `.claude/agents/`

### Direct Invocation

Any agent can be invoked directly for a focused task without following the full workflow. Examples:
- "Use @fullstack-developer to fix this checkbox bug"
- "Use @code-reviewer to review the changes in main.js"
- "Use @database-expert to optimize the component query"

The full workflows below are for **formal feature development**. For ad-hoc tasks, just invoke the relevant agent directly.

---

## Standard Development Workflow

### For New Features

```
1. @product-manager (for vague/unclear requirements)
   ↓ produces requirements document with user stories

2. @ux-designer
   ↓ produces initial UX specifications (v1) based on requirements

3. @architect
   ↓ produces architecture document using requirements + UX handover as input

4. @ux-designer
   ↓ updates UX specifications (v2) to align with architecture

5. @database-expert (if schema changes needed)
   ↓ produces migration plan + scripts

6. DECISION POINT - Implementation Approach:

   **Option A: Autonomous Agent**
   - Invoke @fullstack-developer agent
   - Agent reads handovers and implements autonomously
   - Suitable for well-defined tasks with clear requirements

   **Option B: Guided Execution**
   - Claude Code (main instance) reads fullstack-developer directive
   - Claude Code reads the same handover documents
   - Works collaboratively with human for implementation
   - Suitable for complex tasks requiring frequent iteration

   → HUMAN chooses approach at this point

7. @fullstack-developer (or Claude Code following fullstack directive)
   ↓ implements complete feature (backend + frontend)

8. @code-reviewer
   ↓ reviews implementation

9. @fullstack-developer (if revisions needed)
   ↓ addresses review findings

10. @docs-maintainer
   ↓ updates documentation + creates commit messages

11. HUMAN: Review, commit (or authorise the agent to commit) and merge the pull request
```

**Note**:
- Skip @product-manager if requirements are already crystal clear. Start with @ux-designer in that case.
- @ux-designer creates initial UX design first, then @architect uses it as input
- @ux-designer then aligns their design with architectural constraints
- This sequential approach ensures UX and architecture are properly coordinated
- **Implementation Decision Point**: At step 6, Claude Code will ask whether to invoke the @fullstack-developer agent (autonomous) or execute guided implementation (collaborative). Both approaches follow the same fullstack-developer directive and read the same handover documents.

### For Bug Fixes

```
1. DECISION POINT - Implementation Approach:

   **Option A: Autonomous Agent**
   - Invoke @fullstack-developer agent to analyze and fix

   **Option B: Guided Execution**
   - Claude Code reads fullstack-developer directive
   - Works collaboratively with human to analyze and fix

   → HUMAN chooses approach at this point

2. @fullstack-developer (or Claude Code following fullstack directive)
   ↓ analyzes and fixes bug

3. @code-reviewer
   ↓ validates fix

4. @docs-maintainer
   ↓ creates commit message

5. HUMAN: Review, commit (or authorise the agent to commit) and merge the pull request
```

### For Documentation Updates

```
1. @docs-maintainer
   ↓ updates documentation
   
2. HUMAN: Review, commit (or authorise the agent to commit) and merge the pull request
```

---

## Agent Communication via Handovers

Agents communicate through **handover documents** stored in `.handovers/`. These documents serve as persistent records of decisions, work completed, and context for the next agent in the workflow.

### Handover Structure

```
.handovers/
├── CLAUDE.md              # Detailed instructions for using handovers
├── TEMPLATE.md            # Template for creating new handovers
├── stages/                # One handover per rewrite stage, written at the end of the stage
├── requirements/          # Requirements and user stories from @product-manager
├── architecture/          # Architecture plans from @architect
├── database/              # Database designs from @database-expert
├── ux/                   # UI/UX specs from @ux-designer
├── fullstack/            # Implementation notes from @fullstack-developer
├── review/               # Code reviews from @code-reviewer
└── documentation/        # Doc updates from @docs-maintainer
```

### Naming Convention

**Pattern:** `[subdirectory]/[feature-name]-[source-agent]-to-[target-agent].md`

### Creating Handovers

1. Copy `.handovers/TEMPLATE.md` to appropriate subdirectory
2. Follow naming convention
3. Fill all sections: Context, Deliverables, Decisions, Next Steps
4. Include specific file paths and line numbers
5. Document the "why" behind decisions

### Reading Handovers

```bash
# Find recent handovers
find .handovers -name "*.md" -mtime -7

# Find handovers for you
find .handovers -name "*to-ux-designer.md"

# Search by feature
find .handovers -name "*tire-pressure*"
```

### Detailed Instructions

See `.handovers/CLAUDE.md` for comprehensive instructions on creating and using handovers.

---

## Git Workflow Rules

### For All Agents
- ✅ May commit on a feature branch when the user authorises it for the work at hand; otherwise produce artifacts the human reviews and commits
- ❌ Never commit to **dev**, **staging** or **master**
- ❌ Never merge. The user merges pull requests
- ✅ Can use `git status`, `git diff`, `git log` for context
- ✅ Reference commits/PRs in handover documents when needed
- ✅ Follow the rules in [CI and workflow](#ci-and-workflow)

### For fullstack-developer
- Can use `git status` and `git diff` to check work
- Can use `git log` to understand context
- Must notify in handover when work is ready to commit

### For code-reviewer
- Can use `git diff` to review changes
- Can reference `git log` for context
- Produces commit message suggestions in review document

### For docs-maintainer
- Produces well-formatted commit messages
- Drafts release notes for the GitHub Releases page (there is no CHANGELOG file)
- Creates PR description templates

### Commit Process
1. Agent completes work
2. Agent creates handover document
3. HUMAN reviews work
4. HUMAN commits using messages from docs-maintainer, or authorises the agent to commit on the feature branch
5. Pull request into `dev`; the user merges it when CI is green

### Branch Strategy
- Feature branches: `feature/[feature-name]`
- Bug branches: `fix/[bug-description]`
- Always branch from and merge back to **dev**, through a pull request
- Changes flow `dev` → `staging` → `master`, only through pull requests

---

## Code Style & Standards

### Python (Backend)
- Follow PEP 8
- Async/await for I/O operations
- Comprehensive error handling, but avoid unneeded complexity
- Document all public functions

### Frontend
- Bootstrap 5 utility classes only (no custom CSS compilation)
- Vanilla JavaScript (no frameworks beyond what's already used)
- **TomSelect**: Use TomSelect for multi-select dropdowns when populating data from backend
  - Common pattern: Initialize with `new TomSelect(element, {plugins: ['remove_button'], maxItems: null})`
  - Store instance on element: `element.tomSelect = ts`
  - Used in: Collections, Incidents, Workplans for component selection
- Progressive enhancement
- Mobile-first responsive design
- Don't use Python built-ins like `zip()` in Jinja2 templates - they're not available unless explicitly passed
- When making UI/CSS changes, start with small incremental adjustments, not bold redesigns

### Database
- Use SQLite best practices with Peewee ORM
- Always create migration scripts for schema changes
- Document schema changes
- Never delete data without user confirmation
- **Note**: This project uses breaking database schema changes between versions

---

## Debugging & Bug Fixing Rules

- Always identify the root cause before implementing a fix. Don't fix symptoms.
- Trace the bug through the full stack (route -> business logic -> database -> template -> JS) before proposing changes.
- If the first hypothesis seems too shallow, dig deeper before editing code.
- List top hypotheses ranked by likelihood. Show evidence for the most likely one before changing code.

---

## Change Management Rules

- Follow existing code patterns. Use partial updates (not full updates), match existing architecture layers, keep logic simple.
- Don't over-engineer: no unnecessary parameters, no overly defensive conditionals, no complex abstractions when simpler approaches exist.
- Make the smallest change that solves the problem. Iterate from there.
- When refactoring across files, enumerate ALL affected files first and get approval before editing.
- Verify ALL occurrences across the full stack - including JS references to CSS (classList vs style.display), template references, and Python code.
- Before editing a file, confirm the correct filename exists using Glob or Read.

---

## Testing Requirements

### Before Creating Handover
- ✅ Code runs without errors
- ✅ `uv run pytest -q` and lint pass (see [Testing](#testing))
- ✅ Manual testing completed
- ✅ No obvious bugs introduced
- ✅ Existing functionality preserved

### For fullstack-developer
- Test both backend and frontend
- Verify database operations
- Check responsive behavior
- Test error handling

---

## Development Notes

### Technical Debt
Known technical debt is tracked in [issue #356](https://github.com/xivind/velo-supervisor-2000/issues/356), not in a file in the repository. Add findings there, and say in the issue when an item is cleared.

### Database Schema Changes
This project uses breaking database schema changes between versions. Always run `uv run python -m velo_supervisor.db_migration` when upgrading and backup the database first.

### Docker Development
The application is designed to run in Docker with mounted volumes for data persistence and secrets management.
The Docker `HEALTHCHECK` runs `python -m velo_supervisor.healthcheck` every 600s against `/health`, which returns 503 if an ERROR was logged in the last 24 hours or the database can't be read.

### Logging
Application uses rotating file logs configured in `config/uvicorn_log_config.ini`, logs stored in `/data/logs/` when running in Docker.

**Log levels drive container health:** any ERROR logged in the last 24 hours marks the container unhealthy (see `/health`, #103). Use `logging.error` only when something actually failed (exception, failed database write, failed recalculation, Strava API failure), logged once where it fails. Use `logging.warning` for rejected input (validation, business rules) and for callers repeating a failure already logged below them.

---

## Important Notes

- Handovers ARE committed to git (serve as architectural decision records)
- Always search project knowledge before assuming
- Test before marking work complete
- Check recent handovers to understand current work context

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
