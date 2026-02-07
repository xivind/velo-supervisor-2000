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
- **Code comments only where logic isn't self-evident.** No boilerplate docstrings.
- **Don't repeat yourself.** If something is in CLAUDE.md, reference it - don't rewrite it.

---

## Architecture Overview

### Project Structure
- **Backend**: FastAPI application with Jinja2 templates for server-side rendering
- **Frontend**: HTML templates with JavaScript, Javascript and CSS assets in `frontend/static/`
- **Database**: SQLite with Peewee ORM
- **External API**: Strava integration for activity data

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
  - `backend/config.json` (paths to database and Strava tokens)
  - External Strava tokens file (location specified in config.json)
  - SQLite database file (location specified in config.json)
- **Template files**: `config.json.example` and `strava_tokens.example.json`

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
- **Development (local)**: From the `backend` directory, run: `uvicorn main:app --log-config uvicorn_log_config.ini`
- **Docker deployment**: Use `./create-container-vs2000.sh` to build and deploy as Docker container
- **Server runs on**: Port 8000 (http://localhost:8000)

### Dependencies
- **Install Python dependencies**: `pip install -r requirements.txt`
- **Python version**: 3.9+ (as specified in DOCKERFILE)
- **Create virtual environment**: Recommended for local development

### Database Operations
- **Database backup**: Use `./backup_db.sh` (Docker-specific script)
- **Database migration**: Run `python3 backend/db_migration.py` for schema updates between versions
- **Template database**: Located at `backend/template_db.sqlite`

### Testing
- **WE NEED TO IMPLEMENT PIPELINE FOR TESTING**

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

11. HUMAN: Review, commit, and push
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

5. HUMAN: Review, commit, and push
```

### For Documentation Updates

```
1. @docs-maintainer
   ↓ updates documentation
   
2. HUMAN: Review, commit, and push
```

---

## Agent Communication via Handovers

Agents communicate through **handover documents** stored in `.handovers/`. These documents serve as persistent records of decisions, work completed, and context for the next agent in the workflow.

### Handover Structure

```
.handovers/
├── CLAUDE.md              # Detailed instructions for using handovers
├── TEMPLATE.md            # Template for creating new handovers
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
- ❌ NEVER execute `git commit`, `git push`, or `git merge`
- ✅ Produce artifacts that the human will review and commit
- ✅ Can use `git status`, `git diff`, `git log` for context
- ✅ Reference commits/PRs in handover documents when needed
- ✅ Work always in **dev branch**
- ❌ Never commit directly to **master** or **staging**
- ✅ Human reviews and commits all agent work

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
- Updates CHANGELOG.md
- Creates PR description templates

### Commit Process
1. Agent completes work
2. Agent creates handover document
3. HUMAN reviews work
4. HUMAN commits using messages from docs-maintainer

### Branch Strategy
- Feature branches: `feature/[feature-name]`
- Bug branches: `fix/[bug-description]`
- Always branch from and merge back to **dev**
- Never commit directly to **master** or **staging**

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

### Database Schema Changes
This project uses breaking database schema changes between versions. Always run `backend/db_migration.py` when upgrading and backup the database first using the provided script.

### Docker Development
The application is designed to run in Docker with mounted volumes for data persistence and secrets management.

### Logging
Application uses rotating file logs configured in `uvicorn_log_config.ini`, logs stored in `/data/logs/` when running in Docker.

---

## Important Notes

- Handovers ARE committed to git (serve as architectural decision records)
- Always search project knowledge before assuming
- Test before marking work complete
- Check recent handovers to understand current work context