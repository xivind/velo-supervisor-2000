# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**🚨 IMPORTANT**: Claude Code must ALWAYS read this repository-level CLAUDE.md file at startup. The CLAUDE.md file describes the application Velo Supervisor 2000, application architecture, design principles, learning points, and other key information that must be consulted when working on the application.Additionally, the ISSUES.md file must be read on startup. The ISSUES.md file contains information on what we are currently working on. Claude Code should ensure that the ISSUES.md file is up to date, as the work progress. Furthermore, on startup, Claude Code should state what we are working on and ask what parts we should focus on.

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