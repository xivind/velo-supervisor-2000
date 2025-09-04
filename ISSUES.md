# ISSUES CURRENTLY IN PROGRESS
This file (ISSUES.md) must be read on startup. This file contains information on what we are currently working on. Claude Code should ensure that this file is up to date, as the work progress.

**Current Status**: Phase 1 database work completed (commit 64626d7). Next: Phase 1 database manager methods.  

# Component Collections Feature Specification

## Problem Statement

Users currently need to change status individually for each component when working with logical groupings (e.g., a wheel consists of tube, hub, and rim). The current process is cumbersome when users want to retire, uninstall, or change status for multiple related components simultaneously.

**Example Use Case:** When changing a wheel, users currently must:
1. Change status for tube (e.g., to "Retired")
2. Change status for hub (e.g., to "Retired") 
3. Change status for rim (e.g., to "Retired")

**Desired Outcome:** Users should be able to create a "Front Wheel" collection containing tube, hub, and rim, then change status for the entire collection in one operation.

## Solution Overview

Implement a **Component Collections** system that allows users to:
- Create named collections of related components
- Perform bulk status changes on entire collections
- Manage collections through intuitive UI integrated into existing pages
- Maintain full compatibility with existing individual component workflows

## Database Design

### Collections Table
```sql
CREATE TABLE collections (
    collection_id TEXT PRIMARY KEY UNIQUE,
    collection_name TEXT,
    comment TEXT,
    updated_date TEXT,
    bike_id TEXT,  -- Optional (NULL allowed for template collections)
    components TEXT,  -- JSON string of component IDs
    sub_collections TEXT  -- JSON string of collection IDs (future use, populate as "[]")
)
```

**Rationale:** Single table design follows existing patterns from `Workplans` and `Incidents` tables that use JSON strings for component references.

## Architecture Decisions

### 1. **Integration Strategy**
- **No new dedicated pages** - integrate into existing component overview and bike details pages
- **Reuse existing patterns** - leverage current modal system, JSON handling, and validation frameworks
- **Table-based display** - add collections tables to existing pages where contextually appropriate

### 2. **Component-Collection Relationship**
- **One collection per component** - enforced at business logic level
- **Individual component changes remain possible** - collections don't lock components
- **Collection membership is flexible** - components can be added/removed from collections

### 3. **Status Management**
- **Bulk status changes** - entire collection can change status simultaneously
- **Status consistency validation** - all components in collection must have same status for bulk operations
- **Individual overrides allowed** - single components can still be changed independently

## Business Rules

### Collection Management Rules
1. **Unique component membership**: Each component can only belong to one collection
2. **Flexible bike assignment**: Collections can exist without being assigned to a bike (templates)
3. **Non-destructive deletion**: Deleting a collection leaves components untouched

### Status Change Rules
1. **Collection status consistency**: All components within a collection must have identical status for bulk operations
2. **Mixed status blocking**: Bulk status changes are blocked if collection contains components with different statuses
3. **Individual component flexibility**: Components can be changed individually even when part of collections
4. **Persistent warnings**: Users receive clear, persistent warnings about mixed statuses that prevent bulk operations

### Validation Strategy
1. **Dual validation**: Frontend modal validation + backend business logic enforcement
2. **Clear user feedback**: Toast notifications for errors, persistent modal warnings for mixed statuses
3. **Graceful degradation**: Mixed status collections show warnings but remain functional for individual component operations

## UI/UX Design

### Page Integration
1. **Component Overview Page**: 
   - Show all collections in dedicated table
   - Allow creation/management of collections
   - Display collection icons next to components

2. **Bike Details Page**: 
   - Show bike-specific collections in dedicated table
   - Same functionality as overview page but filtered by bike

3. **Component Details Page**: 
   - Show "Edit Collection" button (since component can only be in one collection)
   - No collections table needed

### Collections Table Columns
- Collection Name
- Component Count
- Bike (if assigned)
- Last Updated  
- Actions (Edit/Delete buttons)

### Collection Modal Functionality
- **Create/Edit collections**: Name, description, bike assignment
- **Component selection**: Reuse existing component selection UI (similar to workplans/incidents)
- **Status change operations**: Bulk status change with validation
- **Persistent warnings**: Show mixed status warnings directly in modal
- **Frontend validation**: Prevent submission of invalid operations

### Visual Indicators
- **Component tables**: Show icon next to components that are part of collections
- **Consistent iconography**: Use clear, intuitive icons throughout the interface

## Implementation Plan

### Phase 1: Database and Core CRUD ✅
1. ✅ Add `Collections` table to `database_model.py` (commit 64626d7)
2. ✅ Add Collections table creation to `db_migration.py` (commit 64626d7)
3. 🔄 Create database manager methods (create, read, update, delete collections)
4. 🔄 Add basic business logic validation methods

**Status**: Database schema complete. Ready for database manager implementation.

### Phase 2: Collection Management Modal
1. Create collection management modal with full CRUD functionality
2. Implement component selection using existing patterns
3. Add frontend validation for mixed statuses
4. Integrate with existing toast notification system

### Phase 3: Table Integration  
1. Add collections tables to component overview page
2. Add collections tables to bike details page (bike-filtered)
3. Integrate modal invocation from table actions

### Phase 4: Status Change Operations
1. Extend existing status change logic to handle collections
2. Implement bulk status change validation
3. Add status change functionality to collection modal
4. Handle partial success scenarios gracefully

### Phase 5: Visual Integration
1. Add collection icons to component tables
2. Add "Edit Collection" button to component details page
3. Ensure consistent visual design across all integration points

### Phase 6: Advanced Features (Future)
1. Collection templates and duplication
2. Nested collections (using `sub_collections` field)
3. Collection-based reporting and analytics

## Technical Considerations

### Existing Code Reuse
- **JSON handling**: Use existing `parse_json_string()` and component ID processing
- **Modal system**: Follow existing modal patterns from workplans/incidents
- **Validation framework**: Leverage existing dual frontend/backend validation
- **Toast notifications**: Use existing user feedback system

### Performance Considerations
- **JSON field indexing**: Consider indexing strategies for component lookups
- **Bulk operations**: Ensure efficient processing of multiple component status changes
- **UI responsiveness**: Handle large collections gracefully in modal interfaces

### Future Extensibility
- **Sub-collections field**: Database ready for nested collection functionality
- **Additional metadata**: Schema allows easy addition of new collection properties
- **API compatibility**: Design endpoints to support future mobile or API integrations

## Success Criteria

1. **User Experience**: Users can change status for multiple related components in single operation
2. **Data Integrity**: All existing component validation rules remain enforced
3. **System Integration**: Collections integrate seamlessly with existing workflows
4. **Performance**: No degradation in existing component management operations
5. **Flexibility**: System supports both collection-based and individual component workflows

## Non-Goals (Current Phase)

- **Nested collections**: Implemented later if needed using `sub_collections` field
- **Collection templates**: Advanced feature for future consideration  
- **Automated collection suggestions**: AI/ML-based collection recommendations
- **Collection sharing**: Cross-user or cross-system collection sharing