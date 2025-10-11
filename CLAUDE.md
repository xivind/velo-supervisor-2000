# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**🚨 IMPORTANT**: Claude Code must ALWAYS read this repository-level CLAUDE.md file at startup. The CLAUDE.md file describes the application Velo Supervisor 2000, application architecture, design principles, learning points, and other key information that must be consulted when working on the application.

---

## Project Overview
Velo Supervisor 2000 is a FastAPI + Bootstrap web application for tracking bicycle component lifecycles using Strava activity data.

**Tech Stack:**
- Backend: Python, FastAPI, SQLite with Peewee ORM
- Frontend: Bootstrap 5, Jinja2 templates (server-side rendered), vanilla JavaScript
- Integration: Strava API
- Deployment: Docker (optional), local development with uvicorn

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

---

## Standard Development Workflow

### For New Features

```
1. @product-manager (for vague/unclear requirements)
   ↓ produces requirements document with user stories

2. @architect + @ux-designer (IN PARALLEL)
   │   ├─ @architect: produces architecture document
   │   └─ @ux-designer: produces UX specifications
   │   (These agents can read each other's handovers and iterate if needed)
   ↓ both complete

3. @database-expert (if schema changes needed)
   ↓ produces migration plan + scripts

4. @fullstack-developer
   ↓ implements complete feature (backend + frontend)

5. @code-reviewer
   ↓ reviews implementation

6. @fullstack-developer (if revisions needed)
   ↓ addresses review findings

7. @docs-maintainer
   ↓ updates documentation + creates commit messages

8. HUMAN: Review, commit, and push
```

**Note**:
- Skip @product-manager if requirements are already crystal clear. Start with @architect + @ux-designer in that case.
- @architect and @ux-designer work in parallel and may interact by reading each other's handovers
- If architectural decisions affect UX or vice versa, agents can iterate

### For Bug Fixes

```
1. @fullstack-developer
   ↓ analyzes and fixes bug
   
2. @code-reviewer
   ↓ validates fix
   
3. @docs-maintainer
   ↓ creates commit message
   
4. HUMAN: Review, commit, and push
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

**Pattern:** `[feature-name]-[source-agent]-to-[target-agent].md`

**Examples:**
- `requirements/component-swap-requirements.md`
- `architecture/tire-pressure-architect-to-ux-designer.md`
- `ux/tire-pressure-ux-designer-to-fullstack.md`
- `fullstack/tire-pressure-fullstack-to-reviewer.md`

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
- Progressive enhancement
- Mobile-first responsive design

### Database
- Use SQLite best practices with Peewee ORM
- Always create migration scripts for schema changes
- Document schema changes
- Never delete data without user confirmation
- **Note**: This project uses breaking database schema changes between versions

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

## Communication Patterns

### Requesting Work
```
@architect - Please design the architecture for [feature]
Based on: [context or requirements]
Output needed: Architecture document in .handovers/architecture/
```

### Handover Format
Each agent ends their response with:
```
**Handover Created:** `.handovers/[path]/[filename].md`
**Next Agent:** @[agent-name]
**Action Required:** [Brief description]
```

---

## Development Notes

### Database Schema Changes
This project uses breaking database schema changes between versions. Always run `backend/db_migration.py` when upgrading and backup the database first using the provided script.

### Docker Development
The application is designed to run in Docker with mounted volumes for data persistence and secrets management.

### Logging
Application uses rotating file logs configured in `uvicorn_log_config.ini`, logs stored in `/data/logs/` when running in Docker.

---

## Emergency Procedures

### If Agent Gets Stuck
1. Document the blocker in handover
2. Mark status as "BLOCKED"
3. Human investigates
4. Provide additional context or simplify task

### If Code Breaks Production
1. Immediate rollback by human
2. @fullstack-developer investigates
3. @code-reviewer validates fix
4. Fast-track commit

---

## Important Notes

- 📁 Handovers ARE committed to git (serve as architectural decision records)
- 🔍 Always search project knowledge before assuming
- 💬 Clear communication in handovers is critical
- 🧪 Test before marking work complete
- 📝 Document decisions and rationale in handovers
- 📋 Check recent handovers to understand current work context