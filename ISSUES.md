# ISSUES CURRENTLY IN PROGRESS

This file (ISSUES.md) must be read on startup. This file contains information on what we are currently working on. Claude Code should ensure that this file is up to date, as the work progress. Always reference issue [#177](https://github.com/xivind/velo-supervisor-2000/issues/177) in the commit messages. When issues are confirmed to be resolved, move them to the bottom of the file in a separate section, and reformulate them to a short one sentence description, to keep a log of whats have been resolved.

**Current Status**: Collections feature is PRODUCTION READY! Core functionality complete, stable, and fully tested. Delete functionality implemented and ready for testing.

---

## Outstanding Collections Tasks

### Missing Functionality
- **Bike overview pages should show emoji for bikes that have active collections**: Visual indicator needed to show which bikes have collections at a glance

### Data Consistency Issues

### Edge Cases & Business Logic
- **Set new status button page reload**: The "Set new status" button should reload the page after completion so users can see the toast notification at the top of the page

---

## Code Quality & Technical Debt

### System-wide Issues

### Backend Consistency


### Architecture Issues
- **HTML Code in Business Logic**: ✅ **FIXED** - Extracted HTML formatting from business logic
  - Solution: Business logic now returns structured data objects, JavaScript formatter handles HTML presentation
  - Implementation: `formatCollectionStatusMessage()` function formats collection status messages following existing HTML patterns
  - Architecture: Proper separation of concerns maintained - business logic returns data, frontend handles presentation

### Code Organization & Conventions
- **Review and fix main.py endpoints**: Ensure collections endpoints follow app conventions
- **Ensure endpoints are placed in correct location**: Collections endpoints should be positioned appropriately in main.py
- **Ensure business logic methods are placed correctly**: Collections methods should follow business_logic.py organization patterns
- **Update business logic methods to follow app conventions**: Remove default parameters from collections methods to match app standards
- **Organize JavaScript code in correct location**: Collections JavaScript should be properly organized in main.js
- **Ensure JavaScript reuses existing patterns**: Collections JavaScript should follow existing patterns for dates, validation, etc.
- **Review all user feedback messages**: In business_logic and js

---

## Collections Feature Overview

### Core Functionality ✅ COMPLETED
- Database schema and CRUD operations
- Collection management modal with full functionality
- Status change operations with validation
- Integration with component overview, bike details, and component details pages
- Collection name columns in component tables
- Delete functionality

### Business Rules ✅ IMPLEMENTED
- Each component can only belong to one collection
- Collections can exist without being assigned to a bike (templates)
- Deleting a collection leaves components untouched
- All components within a collection must have identical status for bulk operations
- Mixed status collections block bulk operations but allow individual component changes

### UI/UX Features ✅ IMPLEMENTED
- Collections tables with component names (clickable to detail pages)
- Interactive bike names (clickable to bike detail pages)
- Comprehensive search functionality including collection content
- Status change modal with validation and user feedback
- Clean text-only design with intuitive component display
- Smart bike assignment field with state management

---

## Development Commands

### Running the Application
- **Development (local)**: From the `backend` directory, run: `uvicorn main:app --log-config uvicorn_log_config.ini`
- **Docker deployment**: Use `./create-container-vs2000.sh` to build and deploy as Docker container
- **Server runs on**: Port 8000 (http://localhost:8000)

### Dependencies
- **Install Python dependencies**: `pip install -r requirements.txt`
- **Python version**: 3.9+ (as specified in DOCKERFILE)

### Database Operations
- **Database backup**: Use `./backup_db.sh` (Docker-specific script)
- **Database migration**: Run `python3 backend/db_migration.py` for schema updates between versions

---

## Resolved Issues

- **Collection updated_date preservation**: Fixed - updated_date field is properly preserved during regular collection saves and only updated during status changes
- **Status change modal cancel button bug**: Fixed - cancel button now properly prevents status changes and cleans up event listeners to prevent duplicate API calls
- **JavaScript collection error handling**: Reviewed - current error handling is sufficient for form submissions and API calls
- **Bike assignment field logic**: Tested and confirmed working correctly with proper component selection state changes and dropdown population
- **Retired component handling in existing collections**: Fixed - collections with retired components are now locked with clear warning, retired components show as "- Retired" but are preserved for data integrity
- **Collection modal component field state bug**: Fixed - improved modal state cleanup to prevent form state persistence between modal sessions, component selector stays enabled for retired component removal