# ISSUES CURRENTLY IN PROGRESS
This file (ISSUES.md) must be read on startup. This file contains information on what we are currently working on. Claude Code should ensure that this file is up to date, as the work progress.

**Current Status**: Collections feature core functionality is complete and stable. Component details page edit collection button fixed. Enhanced modal UI with improved layout and validation. Focus on remaining UI enhancements and edge case handling.

**Note**: Collection icons (📦) in component overview table - need to implement `component_collections` field in payload to show collection membership icons.  

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
4. **Frontend validation**: Collection name validation handled in JavaScript modal (empty name prevention)
5. **Backend validation**: Focus on data integrity (component existence, unique membership)
6. **Bike assignment rule**: Collections with installed components must be assigned to a bike (validate in both frontend and backend)

## UI/UX Design

### Page Integration
1. **Component Overview Page**: 
   - Show all collections in dedicated table
   - Allow creation/management of collections
   - Add collection name column to component table (show "-" if no collection assigned)
   - Display collection icons next to components

2. **Bike Details Page**: 
   - NO separate collections table (removed)
   - Add collection name column to component table (show "-" if no collection assigned)
   - Collection management via "New collection" button and component overview page

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
3. ✅ Create database manager methods (create, read, update collections)
4. ✅ Add basic business logic validation methods
5. ⏸️ Collection delete functionality (deferred - need to handle component cleanup)
6. ⏸️ Update component deletion validation (prevent deletion of components in collections)
7. ⏸️ Update component retirement validation (handle components in collections)

### Phase 2: Collection Management Modal 🚧
1. ✅ Create collection management modal with full CRUD functionality
2. ✅ Implement component selection using existing patterns
3. ✅ Add frontend validation for mixed statuses
4. ✅ Integrate with existing toast notification system
5. 🔲 **MISSING**: Collection deletion functionality (JavaScript handler and API endpoint)
6. 🔲 **MISSING**: Proper error handling in JavaScript functions

### Phase 3: Table Integration 🚧
1. ✅ Add collections tables to component overview page
2. ✅ ~~Add collections tables to bike details page~~ (REMOVED per user feedback)
3. ✅ Integrate modal invocation from table actions
4. 🔲 **NEW**: Add collection name column to component tables (both overview and bike details)

### Phase 4: Status Change Operations ✅
1. ✅ Extend existing status change logic to handle collections
2. ✅ Implement bulk status change validation
3. ✅ Add status change functionality to collection modal
4. ✅ Handle partial success scenarios gracefully

### Phase 5: Visual Integration 🚧
1. ✅ Add collection icons to component tables
2. 🔲 **MISSING**: Add "Edit Collection" button to component details page (references #editCollectionModal which doesn't exist)
3. 🔲 **MISSING**: Collections table on component details page
4. 🔲 **MISSING**: Collection management functionality on component details page
5. ✅ Ensure consistent visual design across all integration points

### Phase 6: Backend API Implementation 🚧
1. ✅ Add backend API endpoints for collections (add, update, change_status)
2. 🔲 **MISSING**: Collection deletion API endpoint (/delete_collection)
3. 🔲 **MISSING**: Collection read API endpoint for component details page
4. ✅ Implement business logic methods for collections
5. 🔲 **MISSING**: Collection deletion business logic method
6. ✅ Integrate with existing history record system

### Phase 7: Code Cleanup and Convention Compliance 🚧
1. 🔲 Review and fix main.py endpoints to follow app conventions
2. 🔲 Ensure endpoints are placed in correct location in main.py
3. 🔲 Ensure business logic methods are placed correctly in business_logic.py
4. 🔲 Update business logic methods to follow app conventions (remove default parameters)
5. 🔲 Update component overview legend with collection icon
6. 🔲 Add collection management to component details page
7. 🔲 Add collections table to component details page (filtered by component)
8. 🔲 Organize JavaScript code in correct location in main.js
9. 🔲 Ensure JavaScript reuses existing patterns (dates, validation)
10. 🔲 Test complete Collections feature end-to-end

**Status**: Core functionality implemented and stable. Collections table fully enhanced with improved UX. Focus on remaining functionality gaps.

## Recent Updates - Collections UI/UX Major Enhancements ✅

Successfully completed comprehensive enhancements to collections system including table improvements and modal redesign:
- ✅ **Column Redesign**: Renamed "Status use" to "Components" and replaced count display with actual component names
- ✅ **Interactive Components**: Made component names clickable to their detail pages (following workplan table pattern)
- ✅ **Interactive Bike Names**: Made bike names clickable to bike detail pages with proper "Not assigned" handling
- ✅ **Enhanced Search**: Updated search functionality to include Components column for comprehensive filtering
- ✅ **Clean UI Design**: Removed unnecessary legend and colored indicators for cleaner text-only approach
- ✅ **Critical Bug Fix**: Resolved issue where collections with deleted components would lose remaining components when saved
- ✅ **Backend Optimization**: Removed unused component status field from get_collections method for improved efficiency
- ✅ **Existing Functionality Preserved**: Column sorting and all existing features continue to work seamlessly
- ✅ **Bike Assignment Field Redesign**: Converted from computed-only to user-selectable with intelligent state management and validation

Collections system now provides intuitive, workplan-style component display with full interactivity, clean design, and logical installation workflow.

## Previous Updates - Collections Modal Date Field Consolidation ✅

Successfully consolidated to single `updated_date` field throughout the entire system:
- ✅ Removed duplicate `collection_updated_date` hidden field
- ✅ Renamed `status_change_date` to `updated_date` in modal, JavaScript, and backend
- ✅ Updated templates to consistently use `updated_date` instead of `last_updated`
- ✅ Made field conditional - required only for status changes, optional for collection CRUD
- ✅ Field now properly tracks last status change date, not general collection updates

### Completed Tasks for Collections Modal:
1. ✅ **UI Enhancement**: Current status indicator with icons (⚡💤⛔) displayed below "New Status" field
2. ✅ **Content Review**: Reviewed and improved field titles and supporting texts for clarity and consistency
3. ✅ **UI Cleanup**: Optimized spacing, removed redundant elements, cleaner visual hierarchy
4. ✅ **Field Name Alignment**: Fixed all field name mismatches between modal, API, business logic, and database model
5. ✅ **TomSelect Integration**: Fixed dropdown initialization and behavior to match incidents/workplans pattern
6. ✅ **Component Filtering**: Added filtering of retired components from dropdown selection
7. ✅ **Computed Bike Assignment**: Implemented automatic bike field computation based on selected components
8. ✅ **Advanced Business Rules**: Added validation preventing mixed installation statuses and mixed bike assignments
9. ✅ **Smart Status Dropdown**: Dynamic dropdown that excludes current status and adapts to validation state
10. ✅ **Integrated Validation System**: Unified frontend and backend validation with clear error messaging
11. ✅ **Enhanced User Experience**: Real-time status computation with "Unable to compute" states for invalid selections

### Recently Completed - Major Collections Feature Enhancements:
- ✅ **Backend validation integration**: Both `add_collection` and `update_collection` now call enhanced validation methods
- ✅ **Business rule enforcement**: Cannot mix installed/not-installed components or components from different bikes
- ✅ **Dynamic UI feedback**: "Unable to compute bike" and "Unable to compute status" messaging for invalid selections
- ✅ **Streamlined interface**: Removed redundant status displays, optimized modal spacing
- ✅ **Context-aware controls**: Status dropdown shows only valid transitions, disabled for invalid states

### Collections Feature Ready for Production Testing

## Outstanding Collections Tasks:
1. ✅ **Review validation rules triggers**: Completed - validation rules properly separated between 'Save collection' (name + business rules) and 'Set new status' (collection saved + components + status + date + business rules)
2. ✅ **Review toast messages text**: Completed - all validation messages improved with structured formatting, bold headers, clear explanations, and actionable tips
3. ✅ **Ensure frontend and backend validation alignment**: Completed - frontend validation prevents invalid submissions, backend messages aligned with "Operation cancelled" and "No changes made" formatting
4. 🔲 **Implement collection deletion functionality**: Add JavaScript handler and API endpoint for collection deletion
5. 🔲 **Add proper error handling in JavaScript collection functions**: JavaScript functions need better error handling for robustness
6. ✅ **Implement component_collections field in payload**: COMPLETED - Added component_collections, component_collection_names, and component_collection_data fields to component overview payload
7. ✅ ~~Fix bike_details.html collections table~~ (REMOVED - table no longer exists)
8. 🔲 **Add column sorting JavaScript handlers**: Collections tables need JavaScript to make column sorting work (data-sort attributes exist but no handlers)
9. 🔲 **Update component overview legend**: Add collection icon explanation to the legend
10. 🔲 **Database null handling**: Verify that empty values are always written as null to the database for all collection fields (not empty strings)
11. 🔲 **Database manager updated_date behavior**: Review how database manager handles updated_date when sometimes skipped - does it overwrite existing value or keep it? Ensure proper handling
12. 🔲 **Sub_collections field**: Ensure sub_collections is always written as null (not empty array) for now until nested collections are implemented
13. 🔲 **Retired component handling in existing collections**: What happens when a collection contains components that are retired after the collection is created, since retired components are filtered out from the dropdown?
14. 🔲 **Collection updated_date preservation bug**: When saving collection changes (like description) without status changes, the `updated_date` field gets overwritten/nulled. The `updated_date` should only track status change operations and be preserved during regular collection saves.
15. ✅ **Collections status change feedback**: Completed - Implemented reusable report modal feedback for "Set new status" operations. Success cases work perfectly, but failure cases still have modal conflicts (see issue #17).
16. 🔲 **Collections and sub_collections NULL handling**: Empty `components` and `sub_collections` fields should write NULL to database instead of empty strings to maintain consistent NULL handling across all collection fields.
17. ✅ **Collections status change modal conflict bug**: RESOLVED - Fixed complex modal conflict issue where loading modal would hang during status changes. Root cause was focus management and Bootstrap modal lifecycle conflicts in confirmation→loading→report modal chain. Solution: Added proper focus management (`confirmAction.blur()`), created reusable `forceCloseLoadingModal()` helper function with multi-level cleanup (Bootstrap methods + DOM manipulation), and established proper timing (200ms internal cleanup + 500ms transition delay). Both success and failure scenarios now work reliably.
18. ✅ **Add collection name column to component tables**: COMPLETED for both component overview and bike details pages - Integrated Collections column with clickable names, showing "-" for components not in collections. Full functionality including backend payload, JavaScript search/sort integration, and modal click handlers.
19. 🔲 **Implement collection deletion functionality**: Add JavaScript handler and API endpoint for collection deletion - delete buttons exist but have no functionality.
20. 🔲 **Add component details page collection integration**: Component details page references `#editCollectionModal` which doesn't exist, missing collections table and management functionality.
21. ✅ **Implement component_collections field for collection icons**: COMPLETED - Added component_collections field to payload and integrated into component overview table (icons removed per user preference, clean text-only design).
22. 🔲 **Add proper error handling to JavaScript collection functions**: JavaScript collection functions need better error handling for robustness and user feedback.
23. ✅ **Collections status change timing optimization**: RESOLVED - Tested with 10-second backend delay to simulate large collections. Current modal system works perfectly: loading modal waits for actual backend response (no timeout needed), 200ms + 500ms delays are only for modal transition cleanup and work reliably. System properly handles any collection size without modification.
24. ✅ **Improve collections status change user feedback**: COMPLETED - Enhanced backend to return detailed component-by-component feedback with friendly names and specific error messages. Implemented structured HTML messages showing successful/failed components separately. Fixed modal backdrop double-dimming issue in error scenarios. Users now get clear, actionable feedback for debugging collection status changes.
25. ✅ **Component Overview Collections Integration**: COMPLETED - Successfully integrated Collections column into component overview table with full functionality.
26. ✅ **Bike Details Collections Integration**: COMPLETED - Successfully integrated Collections column into bike details page component table with full functionality including backend payload, clickable collection names, modal integration, and JavaScript search/sort support.
27. ✅ **Table Sorting Bug Fixes**: COMPLETED - Fixed table sorting issues in both component overview and bike details pages caused by column index shifts after Collections integration. All columns now properly support ascending/descending sort functionality.
28. ✅ **Component Table Naming Consistency**: COMPLETED - Renamed "Name" column to "Component" in both component overview and bike details pages for improved consistency and clarity.
29. ✅ **Component Details Collections Integration**: COMPLETED - Successfully integrated collections functionality into component details page with backend payload, template display, and modal inclusion. Collection membership display shows below installation history with clickable collection names.
30. ✅ **Component Details Edit Collection Button**: COMPLETED - Fixed edit collection button by adding proper data attributes to button and replacing incorrect function calls. Button now works identically to collection name link.
31. ✅ **Collection Table Component Names**: COMPLETED - Collections table now displays actual component names (clickable to component details) in Components column instead of component count. Follows workplan table pattern with clean text-only approach, "Not assigned" for empty collections, and proper handling of deleted components.
32. ✅ **Collection Bike Assignment Field Logic**: COMPLETED - Converted bike assignment field from fully computed to user-selectable dropdown with intelligent state management. Field starts blank on modal open, disables when no components selected or when components already assigned to bikes, filters out retired bikes, shows current bike assignment status, and maintains all existing validation rules. Now follows same pattern as New Status field for consistent UX.
33. ✅ **Collection updated_date Preservation**: COMPLETED - Fixed business logic to preserve existing updated_date values during collection saves. Only status changes should modify this field.
34. ✅ **Enhanced Collection Validation**: COMPLETED - Expanded validation to prevent status changes when collection name, description, or components have unsaved changes. Provides clear user feedback about what needs to be saved.
35. ✅ **Collection Modal UI Enhancement**: COMPLETED - Redesigned modal layout with better field arrangement, improved button positioning, and clearer visual hierarchy. Changed "Save Collection" to "Save details" for accuracy.
36. ✅ **Collections Table Column Enhancement**: COMPLETED - Renamed "Status use" column to "Components" and replaced component count display with actual component names (clickable to detail pages).
37. ✅ **Collections Table Bike Names Clickable**: COMPLETED - Made bike names in collections table clickable to bike detail pages, with "Not assigned" for collections without bikes.
38. ✅ **Collections Table Search Integration**: COMPLETED - Updated collections table search functionality to include Components column content for comprehensive searching.
39. ✅ **Collections Table Legend Removal**: COMPLETED - Removed unnecessary legend for collections table since clean text-only approach eliminates need for colored indicator explanations.
40. ✅ **Collections Save Bug Fix**: COMPLETED - Fixed critical bug where saving collections with deleted components would accidentally remove all remaining components. Now properly filters deleted component IDs in JavaScript validation and TomSelect handling.
41. ✅ **Collections Backend Optimization**: COMPLETED - Removed unused component status field from get_collections method, keeping only essential ID and name fields for cleaner, more efficient backend processing.
42. ✅ **Collection Bike Assignment Field Redesign**: COMPLETED - Redesigned bike assignment field from computed-only display to user-selectable dropdown with intelligent state management, retired bike filtering, current state display, and preserved validation rules for proper installation workflow.
43. 🔲 **Test and Fix Bike Assignment Field Logic**: Need to test new bike assignment field implementation and fix identified bug in the logic. Field should properly handle component selection state changes and bike dropdown population.

## ✅ COMPLETED: Component Overview Collections Integration

### Implementation Details for Replication on Bike Details Page:

#### **Backend Changes (business_logic.py:224-244):**
```python
# In get_component_overview() method, add these payload fields:
component_collections = {}  # component_id -> True (for icons)
component_collection_names = {}  # component_id -> collection_name  
component_collection_data = {}  # component_id -> (collection_id, collection_name, components, bike_id, comment, updated_date)

collections = database_manager.read_all_collections()
for collection in collections:
    component_ids = json.loads(collection.components) if collection.components else []
    for component_id in component_ids:
        component_collections[component_id] = True
        component_collection_names[component_id] = collection.collection_name
        component_collection_data[component_id] = (
            collection.collection_id, collection.collection_name, collection.components,
            collection.bike_id or "", collection.comment or "", collection.updated_date or ""
        )

# Add to payload:
"component_collections": component_collections,
"component_collection_names": component_collection_names,
"component_collection_data": component_collection_data,
```

#### **Template Changes (component_overview.html:148-181):**
```html
<!-- Add Collections column header after Name -->
<th data-sort="collection">Collection <span class="sort-indicator"></span></th>

<!-- Add Collections column data -->
<td>
    {% if component_id in payload.component_collection_names %}
        {% set collection_data = payload.component_collection_data[component_id] %}
        <span class="collection-name-link" role="button" 
              data-collection-id="{{ collection_data[0] }}"
              data-collection-name="{{ collection_data[1] }}"
              data-components="{{ collection_data[2] }}"
              data-bike-id="{{ collection_data[3] }}"
              data-comment="{{ collection_data[4] }}"
              data-updated-date="{{ collection_data[5] }}"
              onclick="event.stopPropagation();" 
              style="cursor: pointer;">
            {{ payload.component_collection_names[component_id] }}
        </span>
    {% else %}
        <span class="text-muted">-</span>
    {% endif %}
</td>

<!-- Update empty table colspan from 8 to 9 -->
<td colspan="9" class="text-center">No components registered</td>
```

#### **JavaScript Changes (main.js:1088-1093, 1108, 3674-3735):**
```javascript
// 1. Update search function cell indices:
const name = row.cells[0].textContent.toLowerCase();
const collection = row.cells[1].textContent.toLowerCase();  // NEW
const type = row.cells[2].textContent.toLowerCase();        // Was [1]
const bike = row.cells[7].textContent.toLowerCase();        // Was [6]
const rowText = `${name} ${collection} ${type} ${bike}`;    // Include collection

// 2. Update "no results" colspan from 8 to 9:
newRow.innerHTML = '<td colspan="9" class="text-center">No components match your criteria</td>';

// 3. Add initial filter call on page load:
updateRowVisibility();  // Add this after event listeners

// 4. Add collection name click handlers:
document.querySelectorAll('.collection-name-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        isNewCollection = false;
        document.getElementById('collectionModalLabel').textContent = 'Edit collection';
        document.getElementById('collection_form').action = '/update_collection';
        
        // Get data from attributes and populate modal
        const collectionId = this.dataset.collectionId;
        const collectionName = this.dataset.collectionName;
        const components = this.dataset.components ? JSON.parse(this.dataset.components) : [];
        // ... (full handler code as implemented)
        
        const modal = new bootstrap.Modal(document.getElementById('collectionModal'));
        modal.show();
    });
});
```

### **Key Points for Bike Details Replication:**
- Must implement same backend payload structure
- Template column insertion requires careful cell index management  
- JavaScript search/filter functions need cell index updates
- Collection click handlers use data attributes (no payload passing needed)
- Remember to add initial `updateRowVisibility()` call on page load
- Update all colspan values for "no results" rows

## Critical Missing Functionality:

### Component Details Page Integration
- Component details page references `#editCollectionModal` which doesn't exist
- No collections table or management functionality on component details page
- Missing API endpoint to get collection data for a specific component
- **SIMPLIFIED APPROACH NEEDED**: Add simple collection membership line to existing card showing:
  - "Not part of any collection" if component not in collection
  - "Part of collection: [Collection Name]" with clickable link to launch modal if component is in collection
- **BACKEND**: Need to pass collection data (if any) for the specific component to component details page payload
- **MODAL**: Reuse existing collection modal with component's collection data pre-populated

### Collection Deletion
- Delete buttons exist in tables but no JavaScript handlers
- No `/delete_collection` API endpoint
- No business logic method for collection deletion

### Error Handling and Validation
- JavaScript functions lack proper error handling
- Missing validation for edge cases in collection management

### Phase 8: Advanced Features (Future)
1. Collection templates and duplication
2. Nested collections (using `sub_collections` field)
3. Collection-based reporting and analytics

## Accessibility Issues (Technical Debt)

25. 🔲 **Fix mismatched label for attributes**: Browser console reports "The label's for attribute doesn't match any element id." This affects form accessibility and autofill functionality. Need to audit all HTML templates and ensure every `<label for="...">` has a corresponding `<input id="...">` element. Collections modal is verified clean - issue likely in older templates like component_details.html and modal_create_component.html.

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