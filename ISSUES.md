# ISSUES CURRENTLY IN PROGRESS

This file (ISSUES.md) must be read on startup. This file contains information on what we are currently working on. Claude Code should ensure that this file is up to date, as the work progress. Always reference issue [#177](https://github.com/xivind/velo-supervisor-2000/issues/177) in the commit messages.

**Current Status**: Collections feature is PRODUCTION READY! Core functionality complete, stable, and fully tested. Delete functionality implemented and ready for testing.

---

## Outstanding Collections Tasks

### Missing Functionality
- **Add proper error handling in JavaScript collection functions**: JavaScript functions need better error handling for robustness and user feedback
- **Add column sorting JavaScript handlers**: Collections tables need JavaScript to make column sorting work (data-sort attributes exist but no handlers)
- **Update component overview legend**: Add collection icon explanation to the legend
- **Add component details page collection integration**: Component details page references `#editCollectionModal` which doesn't exist, missing collections table and management functionality

### Data Consistency Issues
- **Collection updated_date preservation**: When saving collection changes (like description) without status changes, the `updated_date` field gets overwritten/nulled. The `updated_date` should only track status change operations and be preserved during regular collection saves

### Edge Cases & Business Logic
- **Retired component handling in existing collections**: What happens when a collection contains components that are retired after the collection is created, since retired components are filtered out from the dropdown?
- **Test and Fix Bike Assignment Field Logic**: Need to test new bike assignment field implementation and fix identified bug in the logic. Field should properly handle component selection state changes and bike dropdown population

---

## Code Quality & Technical Debt

### System-wide Issues
- **Fix mismatched label for attributes**: Browser console reports "The label's for attribute doesn't match any element id." This affects form accessibility and autofill functionality. Need to audit all HTML templates and ensure every `<label for="...">` has a corresponding `<input id="...">` element. Collections modal is verified clean - issue likely in older templates like component_details.html and modal_create_component.html

### Backend Consistency
- **Inconsistent NULL/Empty String Handling**: Inconsistent use of `or ""` vs `None` values throughout business_logic.py
  - Problem: 12 occurrences of `or ""` in frontend payloads while rest of codebase uses `None` values consistently
  - Location: Collection data payload construction (lines ~185, 259, 455, 660, etc.)
  - Fix: Review all `or ""` patterns and change to pass `None` values for NULL database fields

- **Backend validation empty string handling**: Backend validation for "Installed" status checks `component_bike_id is None` but frontend sends empty string `""`
  - Problem: `create_history_record` validation (line 1359) only catches `None` values, not empty strings
  - Impact: Users can install components without selecting a bike, bypassing intended validation
  - Fix: Update backend validation to check `(component_bike_id is None or component_bike_id == '')` for consistency

### Architecture Issues
- **HTML Code in Business Logic**: Business logic contains significant amounts of HTML formatting code
  - Problem: Violation of separation of concerns - business logic should not handle presentation
  - Examples: Collection status change messages, validation error messages, bulk operation feedback
  - Fix: Extract HTML formatting to a separate presentation layer or utility module, keep business logic returning plain text/structured data

### Code Organization & Conventions
- **Review and fix main.py endpoints**: Ensure collections endpoints follow app conventions
- **Ensure endpoints are placed in correct location**: Collections endpoints should be positioned appropriately in main.py
- **Ensure business logic methods are placed correctly**: Collections methods should follow business_logic.py organization patterns
- **Update business logic methods to follow app conventions**: Remove default parameters from collections methods to match app standards
- **Organize JavaScript code in correct location**: Collections JavaScript should be properly organized in main.js
- **Ensure JavaScript reuses existing patterns**: Collections JavaScript should follow existing patterns for dates, validation, etc.

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