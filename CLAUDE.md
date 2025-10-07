# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**🚨 IMPORTANT**: Claude Code must ALWAYS read this repository-level CLAUDE.md file at startup. The CLAUDE.md file describes the application Velo Supervisor 2000, application architecture, design principles, learning points, and other key information that must be consulted when working on the application.Additionally, the ISSUES.md file must be read on startup. The ISSUES.md file contains information on what we are currently working on. Claude Code should ensure that the ISSUES.md file is up to date, as the work progress. Furthermore, on startup, Claude Code should state what we are working on and ask what parts we should focus on.

REMEMBER: ONLY ONE ISSUE AT THE TIME IN ISSUES.MD. Full GITHUB-integration, with issue access and more. Use GH-MCP

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

## Architecture Overview

### Project Structure
- **Backend**: FastAPI application with Jinja2 templates for server-side rendering
- **Frontend**: HTML templates with JavaScript, CSS assets in `frontend/static/`
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
- **Workplans**: Maintenance scheduling
- **Service history**: Component maintenance records

### Testing
- **Test protocols**: Located in `tests/` directory
- **Manual testing approach**: Comprehensive test protocols document expected behavior and test cases
- **Available protocols**: See `tests/README.md` for full list and testing approach
- **Collections testing**: `tests/test_protocol_collections.md` (135 test cases)

## Development Notes

### Database Schema Changes
This project uses breaking database schema changes between versions. Always run `backend/db_migration.py` when upgrading and backup the database first using the provided script.

### Docker Development
The application is designed to run in Docker with mounted volumes for data persistence and secrets management.

### Logging
Application uses rotating file logs configured in `uvicorn_log_config.ini`, logs stored in `/data/logs/` when running in Docker.

## Agent System

### Overview
This project uses a specialized agent system to coordinate development work. Each agent has specific responsibilities and communicates via `issues.md` as the central coordination hub.

### Available Agents
Agents are defined in `.claude/agents/` directory:

1. **architect** (`.claude/agents/architect.md`)
   - Role: System design, technical decisions, feature planning
   - MCP Access: IDE diagnostics
   - Output: Architecture plans and task breakdowns in issues.md

2. **ux-designer** (`.claude/agents/ux-designer.md`)
   - Role: User experience design, UI patterns, user workflows
   - MCP Access: Playwright (browser automation)
   - Output: UX designs and interface specifications in issues.md

3. **full-stack-developer** (`.claude/agents/full-stack-developer.md`)
   - Role: Implementation across database, backend, and frontend
   - MCP Access: IDE diagnostics, Playwright
   - Output: Working code with implementation notes in issues.md

4. **qa-reviewer** (`.claude/agents/qa-reviewer.md`)
   - Role: Code review, quality assurance, test protocol creation
   - MCP Access: IDE diagnostics, Playwright
   - Output: Test protocols, QA reviews, and bug reports in issues.md

5. **documentation-specialist** (`.claude/agents/documentation-specialist.md`)
   - Role: Documentation maintenance (CLAUDE.md, issues.md, README.md, test protocols)
   - MCP Access: None (file operations only)
   - Output: Updated documentation files

### Agent Workflows

#### Feature Development Workflow
Standard workflow for implementing new features:

1. **architect**: Plan feature architecture
   - Read CLAUDE.md and issues.md for context
   - Create architecture plan with task breakdown
   - Document technical decisions and approach
   - Add plan to issues.md
   - Handoff to: **ux-designer**

2. **ux-designer**: Design user experience
   - Review architecture plan
   - Design UI components (pages, modals, forms)
   - Map user workflows (happy path + errors)
   - Document UX design in issues.md
   - Handoff to: **full-stack-developer**

3. **full-stack-developer**: Implement feature
   - Review architecture plan and UX design
   - Implement database layer (if needed)
   - Implement backend (API, business logic)
   - Implement frontend (templates, JavaScript)
   - Test locally and document progress in issues.md
   - Handoff to: **qa-reviewer**

4. **qa-reviewer**: Review and test
   - Review code for quality and conventions
   - Create/update test protocol
   - Execute test protocol
   - Document findings in issues.md
   - If approved, handoff to: **documentation-specialist**
   - If issues found, handoff back to: **full-stack-developer**

5. **documentation-specialist**: Update documentation
   - Update CLAUDE.md (if architecture/features changed)
   - Update README.md (if user-facing changes)
   - Move completed items in issues.md to "Resolved Issues"
   - Update current status
   - Mark feature as complete

#### Bug Fix Workflow
Streamlined workflow for fixing bugs:

1. **qa-reviewer**: Analyze issue and identify root cause
   - Reproduce bug
   - Identify affected code
   - Document in issues.md
   - Handoff to: **full-stack-developer**

2. **full-stack-developer**: Implement fix
   - Fix the bug
   - Test locally
   - Document fix in issues.md
   - Handoff to: **qa-reviewer**

3. **qa-reviewer**: Verify fix
   - Test that bug is fixed
   - Run regression tests
   - If verified, handoff to: **documentation-specialist**
   - If not fixed, handoff back to: **full-stack-developer**

4. **documentation-specialist**: Update issues.md
   - Move to resolved issues
   - Update status

#### Refactoring Workflow
Workflow for code quality improvements:

1. **qa-reviewer**: Identify technical debt
   - Review code for issues
   - Document duplication, inconsistencies, etc.
   - Add to issues.md
   - Handoff to: **architect**

2. **architect**: Plan refactoring approach
   - Design refactoring strategy
   - Break down into tasks
   - Document plan in issues.md
   - Handoff to: **full-stack-developer**

3. **full-stack-developer**: Implement refactoring
   - Refactor code
   - Test that functionality unchanged
   - Document in issues.md
   - Handoff to: **qa-reviewer**

4. **qa-reviewer**: Verify refactoring
   - Review code quality improvement
   - Run regression tests
   - Document results
   - Handoff to: **documentation-specialist**

5. **documentation-specialist**: Update docs
   - Update CLAUDE.md if patterns changed
   - Move to resolved issues

### Communication Protocol

#### issues.md as Central Hub
All agents communicate through `issues.md`:
- Architecture plans
- UX designs
- Implementation progress
- QA reviews and test results
- Documentation updates

#### Handoff Format
Each agent should clearly indicate handoff:
```markdown
### Handoff
Ready for: **[agent-name]**
```

#### Status Tracking
Use these status indicators in issues.md:
- **Planning**: architect working
- **Design**: ux-designer working
- **In Progress**: full-stack-developer working
- **Review**: qa-reviewer working
- **Documentation**: documentation-specialist working
- **Complete**: All work done

### Agent Invocation

To invoke an agent during a Claude Code session, you can reference them by name or request their specific expertise. For example:
- "Can the architect help plan this feature?"
- "Let's have the ux-designer design the UI for this"
- "Have the qa-reviewer check this code"

Agents will follow their defined roles and responsibilities as documented in their respective files in `.claude/agents/`.

### Benefits of Agent System
- **Clear separation of concerns**: Each agent focuses on their expertise
- **Consistent quality**: Structured reviews and testing for all features
- **Better planning**: Upfront design before implementation
- **Comprehensive testing**: Dedicated QA process
- **Maintained documentation**: Dedicated doc updates
- **Traceable workflow**: All work documented in issues.md