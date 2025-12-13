# Install Unassigned Components/Collections - Requirements Document

**Feature:** Install Unassigned Components or Collections from Bike Details Page
**Date:** 2025-12-13
**Status:** Complete
**Prepared by:** @product-manager
**Ready for:** @ux-designer

---

## Executive Summary

This feature enables users to install components or collections that are currently unassigned (not installed on any bike) directly from the bike details page. This addresses a workflow gap where users must navigate to component detail pages to change status from "Not installed" to "Installed", even when they're already viewing the target bike.

**Primary Use Cases:**
- Installing spare components that were previously removed from another bike
- Installing new components that were created but never installed
- Installing seasonal collections (e.g., "Winter Wheelset") when switching bike configurations
- Onboarding existing components from inventory into active use

**Key Value Proposition:** Reduce a 3-5 step cross-page workflow into a single modal operation directly from the bike details page. This feature reuses existing backend endpoints (`/add_history_record` for components, `/change_collection_status` for collections), making it primarily a front-end orchestration feature.

---

## Context & Problem Statement

### Current Pain Points

Users face workflow friction when installing unassigned components or collections onto bikes:

1. **Navigation required**: Must leave bike details page, navigate to component overview or collection management, find the component/collection, then change its status
2. **Context switching**: Lose sight of the target bike when navigating to component detail pages
3. **Multiple operations**: For collections, must change status of multiple components individually, or use collection modal which isn't accessible from bike details page
4. **Mental overhead**: Must remember which bike they were working on when navigating across pages

### User Scenarios

**Scenario 1: Installing Spare Wheels**
> Marcus has a spare set of wheels that he removed from his road bike for winter storage. Now he wants to install them on his gravel bike. The wheels are currently marked "Not installed".
>
> **Current workflow:** Navigate away from gravel bike details page → Find wheels in component overview → Click each wheel → Change status to "Installed" → Select gravel bike → Save → Repeat for second wheel → Navigate back to gravel bike details.
>
> **Desired workflow:** On gravel bike details page → Click "Install Component" button → Search for wheel components → Select first wheel → Set installation date → Install → Repeat for second wheel (or use collection if wheels are in one).

**Scenario 2: Installing Seasonal Collection**
> Elena is preparing her mountain bike for winter. She has a "Winter Wheelset" collection containing wheels, tires, and a cassette - all currently "Not installed".
>
> **Current workflow:** Navigate to component overview → Find collection modal → Edit collection → Change status to "Installed" → Select mountain bike → Apply status change → Navigate back to bike details page.
>
> **Desired workflow:** On mountain bike details page → Click "Install Component" button → Switch to "Collection" tab → Select "Winter Wheelset" collection → Set installation date → Install collection.

**Scenario 3: Activating New Components**
> Sarah just purchased new brake pads and created them in the system with status "Not installed". Now she wants to install them on her road bike.
>
> **Current workflow:** Navigate to brake pads detail page → Change status to "Installed" → Select road bike → Navigate back to bike details page to verify installation.
>
> **Desired workflow:** On road bike details page → Click "Install Component" button → Search for brake pads → Select new brake pads → Set installation date → Install.

---

## User Personas

### Primary Persona: The Multi-Bike Owner
- **Profile**: Owns 2-3 bikes, rotates components between them seasonally or for maintenance
- **Frequency**: Installs unassigned components 2-4 times per month
- **Pain point**: Navigation friction when managing component assignments across bikes
- **Needs**: Quick, in-context component installation from bike details page

### Secondary Persona: The New User (Onboarding)
- **Profile**: Just started using Velo Supervisor 2000, has many existing components to track
- **Frequency**: Batch installing components when setting up system (10-20 components at once)
- **Pain point**: Repetitive navigation when assigning components to bikes during initial setup
- **Needs**: Efficient workflow for assigning components to bikes in bulk

---

## Detailed Requirements

### Functional Requirements

#### FR-1: Installation Access Point

**FR-1.1: Button Placement**
- A new button must appear on the bike details page in the action button row
- Button should be alongside existing buttons (after "New component") ("New collection", "New component", "New workplan", "New incident")
- Button label: "Install component" (icon: ⚙)

**FR-1.2: Button Visibility**
- Button is always visible when viewing bike details page
- Button is visible even if bike has no currently installed components
- Button is visible for both active and retired bikes

**FR-1.3: Modal Launch**
- Clicking button opens a modal dialog
- Modal is similar in structure to existing component/collection modals
- Modal should be distinct (not reusing create component modal)

#### FR-2: Component vs Collection Mode Selection

**FR-2.1: Mode Toggle**
- Modal contains a toggle/tab to switch between "Component" mode and "Collection" mode
- Default mode: "Component" (individual component installation)
- Toggle pattern: Radio button toggle

**FR-2.2: Mode Switching**
- Switching modes clears current selection (if any)
- Switching modes changes the search/select interface appropriately
- Mode selection persists while modal is open (doesn't reset between interactions)

**FR-2.3: Single Operation Mode**
- User can install ONE component OR ONE collection per modal submission
- User cannot mix component and collection installation in single operation
- User cannot select multiple components or multiple collections

#### FR-3: Component Mode - Selection Interface

**FR-3.1: Component Eligibility**
- Only components with `installation_status = "Not installed"` are selectable
- Components with `installation_status = "Installed"` or `"Retired"` are excluded
- No component type filtering (all types of unassigned components are shown)

**FR-3.2: Component Display Format**
- Components displayed as: `[Component Name] ([Component Type]) - [Distance] km`
- Example: "Shimano 105 Brake Pads (Brake Pads) - 250 km"
- Sorted by component name (alphabetically)

**FR-3.3: Search/Filter Functionality**
- Search box allows filtering components by name or type (use TomSelect)
- Search is case-insensitive
- Search updates results in real-time (as user types)

**FR-3.4: Empty State**
- If no "Not installed" components exist, show message: "No unassigned components available. Create a new component first."

**FR-3.5: Component Type Compliance Warning**
- The user should receive component compliance warning, according to functionality and logic that already exists for status change for collections and components
- Use existing backend logic to validate component status change
- Use existing pattern for feedback to user (probably a toast when changing status for component)

#### FR-4: Collection Mode - Selection Interface

**FR-4.1: Collection Eligibility**
- Only collections where ALL member components have `installation_status = "Not installed"` are selectable
- Collections with mixed statuses (some installed, some not) are excluded
- Collections with all "Retired" components are excluded

**FR-4.2: Collection Display Format**
- Collections displayed as: `[Collection Name] ([X] components)`
- Example: "Winter Wheelset (4 components)"

**FR-4.3: Filtering Help Text**
- Display muted text below collection selection: "Only showing collections where all components are unassigned." Something similar for components
- This clarifies why some collections may not appear

**FR-4.4: Empty State**
- If no eligible collections exist, show message: "No unassigned collections available. Collections with mixed installation statuses cannot be installed as a group."

**FR-4.5: Collection Member Validation**
- Use existing backend logic to validate collection status change
- Use existing pattern for feedback to user (probably a modal when changing status for collection)

#### FR-5: Installation Date Selection

**FR-5.1: Date Input**
- Single date/time input field labeled "Installation Date"
- Default value: Current date and time (format: YYYY-MM-DD HH:MM)
- Use existing datepicker pattern (consistent with other modals)
- Use same calendar icon (🗓) toggle for opening datepicker as in other modals

**FR-5.2: Date Validation**
- Date cannot be in the future
- Date can be in the past (user may be retroactively logging installations)
- Error message: "Installation date cannot be in the future."
- Use the same methods for validating dates as other date pickers

**FR-5.3: Date Application**
- For components: Single component gets the specified installation date
- For collections: ALL member components get the same installation date
- Date is used for both `updated_date` and history record `updated_date` fields

#### FR-6: Bike Context Display

**FR-6.1: Bike Identification**
- Modal displays prominently: "Installing on: [Bike Name]"
- Bike name shown at top of modal (in header)
- Bike is implicitly determined from current bike details page context

**FR-6.2: Bike Assignment Logic**
- Component/collection is installed on the bike whose details page is currently being viewed
- No bike selection dropdown (bike context is implicit)
- Bike ID is automatically passed to backend from page context

#### FR-7: Backend Integration - Component Installation

**FR-7.1: Endpoint Reuse**
- Component installation uses existing endpoint: `POST /add_history_record`
- Endpoint located at `/home/xivind/code/velo-supervisor-2000/backend/main.py:260`
- Business logic: `business_logic.create_history_record()` in `business_logic.py:1340`

**FR-7.2: Request Parameters**
```
component_id: [selected component ID]
component_installation_status: "Installed"
component_bike_id: [current bike ID from page context]
component_updated_date: [user-specified installation date]
```

**FR-7.3: Response Handling**
- Success: Close modal, show toast notification (reuse existing toast pattern)
- Success message: Use whats already defined for the /add_history_record endpoint
- Warning or error: Close modal, show toast notification (reuse existing toast pattern)
- Warning or error message: Use whats already defined for the /add_history_record endpoint
- After submit and closing modal: Refresh bike details page to show newly installed component in table

#### FR-8: Backend Integration - Collection Installation

**FR-8.1: Endpoint Reuse**
- Collection installation uses existing endpoint: `POST /change_collection_status`
- Endpoint located at `/home/xivind/code/velo-supervisor-2000/backend/main.py:377`
- Business logic: `business_logic.change_collection_status()` in `business_logic.py:1885`

**FR-8.2: Request Parameters**
```
collection_id: [selected collection ID]
new_status: "Installed"
updated_date: [user-specified installation date]
bike_id: [current bike ID from page context]
```

**FR-8.3: Response Handling**
- Success: Close modal, show response in modal format (reuse existing collection status change feedback pattern)
- Success feedback shows: reuse existing feedback as for collection status change (report modal or something)
- Partial failure feedback shows: reuse existing feedback as for collection status change (report modal or something)
- Error: reuse existing feedback as for collection status change (report modal or something)
- After success: Refresh bike details page to show newly installed components in table

**FR-8.4: Collection Bike Assignment**
- Collection's `bike_id` field is automatically updated to match the bike being installed on
- This follows existing business rules from `change_collection_status` function
- Backend handles this automatically (no frontend logic needed)

#### FR-9: User Workflow

**FR-9.1: Component Installation Flow**
```
Step 1: User clicks "Install Component" button on bike details page
  ↓
Step 2: Modal opens with "Component" mode selected (default)
  ↓
Step 3: User searches/selects a component from "Not installed" components
  ↓
Step 4: User specifies installation date (defaults to today)
  ↓
Step 5: User clicks "Install" button
  ↓
Step 6: System calls /add_history_record endpoint
  ↓
Step 7: Success: Modal closes, toast notification appears, page refreshes
        Error: Modal closes, error shown in toast, user can retry
```

**FR-9.2: Collection Installation Flow**
```
Step 1: User clicks "Install Component" button on bike details page
  ↓
Step 2: Modal opens, user switches to "Collection" mode
  ↓
Step 3: User selects a collection from eligible collections
  ↓
Step 4: System displays collection info (number of components, names)
  ↓
Step 5: User specifies installation date (defaults to today)
  ↓
Step 6: User clicks "Install Collection" button
  ↓
Step 7: System calls /change_collection_status endpoint
  ↓
Step 8: Success: Modal shows status change feedback (like existing collection modal)
        Partial failure: Modal shows which components succeeded/failed
        Error: Modal shows which components succeeded/failed (same behaviour as the collection modal)
  ↓
Step 9: User clicks "Done" or "Close" on feedback modal (verify that this is the same behaviour as the collection modal)
  ↓
Step 10: Page refreshes to show newly installed components
```

#### FR-10: Validation Rules

**FR-10.1: Component Mode Validation**
- Component must be selected (not empty)
- Installation date must be valid and not in future (use existing validation rules for dates, defined in js)
- Component must still be "Not installed", but this is handled through what is shown in the selector/search box (filtering)
- Bike must exist

**FR-10.2: Collection Mode Validation**
- Collection must be selected (not empty)
- Installation date must be valid and not in future (use existing validation rules for dates, defined in js)
- All collection member components must be "Not installed", but this is handled through what is shown in the selector/search box (filtering)
- Collection must exist
- Bike must exist

**FR-10.3: Backend Validation**
- All validation performed by existing endpoints and if logic exist in the js, we reuse that also, e.g for valid date validation
- No new validation logic needed
- Existing `create_history_record` and `change_collection_status` functions handle all validation, including relevant validation rules in the js

---

## User Stories with Acceptance Criteria

### User Story 1: Install Individual Component from Bike Details Page

**As a** bike owner managing multiple bikes
**I want to** install an unassigned component directly from the bike details page
**So that** I don't have to navigate away from the bike I'm working on

**Acceptance Criteria:**
- [ ] Bike details page displays an "Install Component" button alongside existing action buttons
- [ ] Clicking button opens a modal dialog
- [ ] Modal defaults to "Component" mode (not "Collection" mode)
- [ ] Modal displays "Installing on: [Bike Name]" prominently
- [ ] Dropdown/search shows only components with status "Not installed"
- [ ] Components display format: "[Name] ([Type]) - [Distance] km"
- [ ] User can search/filter components by name or type
- [ ] Installation date defaults to current date/time
- [ ] User can edit installation date (cannot be future date)
- [ ] Clicking "Install" calls existing `/add_history_record` endpoint
- [ ] Success: Modal closes, toast notification appears, page refreshes showing new component
- [ ] Error: Error displays in modal, user can retry without losing form data

**Edge Cases:**
- What if no "Not installed" components exist? Display empty state message with guidance

---

### User Story 2: Switch Between Component and Collection Modes

**As a** user choosing how to install components
**I want to** toggle between installing individual components or entire collections
**So that** I can use the same modal for both types of installation operations

**Acceptance Criteria:**
- [ ] Modal contains a toggle or tab control labeled "Component" and "Collection"
- [ ] Default selection is "Component" mode
- [ ] Clicking "Collection" tab switches interface to show collections instead of components
- [ ] Clicking "Component" tab switches back to component interface
- [ ] Switching modes clears any current selection
- [ ] Selection interface changes appropriately (component dropdown vs collection dropdown)
- [ ] Mode persists while modal is open (doesn't reset if user changes date or other fields)
- [ ] Closing and re-opening modal resets to "Component" mode (default)

**Edge Cases:**
- What if user selects a component, then switches to collection mode? Selection is cleared, no error
- What if user switches modes rapidly? Interface updates smoothly, no UI glitches or race conditions

---

### User Story 3: Install Collection with All Member Components

**As a** user managing seasonal component sets
**I want to** install an entire collection onto a bike in one operation
**So that** I don't have to individually install each component in the collection

**Acceptance Criteria:**
- [ ] Switching to "Collection" mode shows dropdown of eligible collections
- [ ] Only collections where ALL components are "Not installed" appear in dropdown
- [ ] Collections display as: "[Collection Name] ([X] components)"
- [ ] Muted help text states: "Only showing collections where all components are unassigned."
- [ ] Selecting collection shows collection details (optional preview of member components)
- [ ] Installation date applies to all member components in collection
- [ ] Clicking "Install Collection" calls existing `/change_collection_status` endpoint
- [ ] Success: Modal shows status change feedback (reusing existing collection feedback pattern)
- [ ] Feedback shows: Total components updated, list of component names
- [ ] Collection's `bike_id` is automatically updated to match target bike
- [ ] After closing feedback modal, bike details page refreshes showing all new components

**Edge Cases:**
- What if no eligible collections exist (all have mixed statuses)? Display empty state message
- What if collection has 10+ components? Feedback modal handles large lists gracefully (scrollable or truncated with count)
- What if one component in collection fails to install? Partial failure feedback shows which succeeded and which failed (reuse existing logic)

---

## Integration Points

**Existing Endpoints Reused:**
- `POST /add_history_record` (line 260 in `backend/main.py`)
  - Used for: Installing individual components
  - Parameters: component_id, component_installation_status, component_bike_id, component_updated_date
  - Returns: Success/error response with message, frontend displays as toast

- `POST /change_collection_status` (line 377 in `backend/main.py`)
  - Used for: Installing collections
  - Parameters: collection_id, new_status, updated_date, bike_id
  - Returns: JSONResponse with success/error and detailed message (partial failure handling), frontend displays as modal

**Database Tables Affected:**
- `components` table: `installation_status`, `bike_id`, `updated_date` fields modified
- `component_history` table: New records inserted for each component installed
- `collections` table: `bike_id` and `updated_date` field updated for installed collections

**Pages Requiring Updates:**
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/bike_details.html`
  - Add "Install Component" button in action button row (around line 30-43)
  - Include new modal template
  - Add JavaScript for modal behavior and endpoint calls

**No Backend Changes Required:**
- All functionality uses existing endpoints
- All validation uses existing business logic
- No new routes, no new database tables, no schema changes

---

## MVP vs. Future Enhancements

### MVP Scope (Must Have for First Release)

- Single component installation from bike details page
- Single collection installation from bike details page
- Component/Collection mode toggle
- Search/filter for components
- Installation date selection
- Reuse existing `/add_history_record` endpoint
- Reuse existing `/change_collection_status` endpoint
- Empty state handling
- Basic error handling and validation

---

## Technical Implementation Notes for Architect

### Reuse Strategy Validation

The user hypothesis is that this feature is **primarily front-end orchestration** with minimal backend work. Please validate:

1. **Component Installation:** Can we directly reuse `POST /add_history_record` as-is?
   - Endpoint at `backend/main.py:260`
   - Business logic at `business_logic.py:1340` (`create_history_record`)
   - Does this endpoint handle all required validation (component exists, status is "Not installed", bike exists)?

2. **Collection Installation:** Can we directly reuse `POST /change_collection_status` as-is?
   - Endpoint at `backend/main.py:377`
   - Business logic at `business_logic.py:1885` (`change_collection_status`)
   - Does this endpoint validate that all collection members are "Not installed"?
   - Does it automatically update collection's `bike_id` and `updated_date` field?

3. **Data Retrieval:** What endpoints provide the data for populating dropdowns?
   - Need: All components with `installation_status = "Not installed"`
   - Need: All collections where all member components have `installation_status = "Not installed"`
   - Can this be queried from existing page context, or do we need new API endpoints?

4. **Response Patterns:**
   - Component installation: Currently uses `RedirectResponse` (line 272-274 in main.py). Can reuse as-is?
   - Collection installation: Already uses JSONResponse (line 389 in main.py). Can reuse as-is?

Please review and confirm the reuse strategy or flag any backend modifications needed.

---

## Next Steps

This requirements document is now **complete** and ready for handover to **@ux-designer**.

**Handover Summary:**
- **Feature:** Install Unassigned Components or Collections from Bike Details Page
- **Scope:** Fully defined MVP with 4 user stories, comprehensive acceptance criteria, and reuse strategy
- **Key Decisions:**
  - Single-select only (one component OR one collection per operation)
  - Component/Collection mode toggle within one modal
  - Reuse existing backend endpoints (no new routes)
  - Component type compliance warnings are non-blocking
  - Collections only installable if ALL members are "Not installed"

**Action Required from @ux-designer:**
1. Design modal layout and interaction pattern
2. Specify Component/Collection mode toggle design (tabs, radio buttons, other)
3. Design search/filter interface for components
4. Design dropdown/selection interface for collections
5. Specify empty state designs (no components, no collections)
6. Design component type compliance warning appearance
7. Design success feedback (toast for components, modal for collections)
8. Ensure responsive design for mobile/tablet
9. Specify accessibility considerations (keyboard navigation, screen reader support)
10. Create UX specifications handover document for @architect

**Note for @architect:**
- Review "Technical Implementation Notes for Architect" section above
- Validate reuse strategy for existing endpoints
- Identify any backend modifications or new API endpoints needed
- Coordinate with @ux-designer on response format requirements (JSONResponse vs RedirectResponse)

---

## References

- **Existing Quick Swap feature:** `.handovers/requirements/component-quick-swap-requirements.md` (similar modal pattern)
- **Backend endpoints:**
  - `/home/xivind/code/velo-supervisor-2000/backend/main.py:260` (`/add_history_record`)
  - `/home/xivind/code/velo-supervisor-2000/backend/main.py:377` (`/change_collection_status`)
- **Business logic:**
  - `/home/xivind/code/velo-supervisor-2000/backend/business_logic.py:1340` (`create_history_record`)
  - `/home/xivind/code/velo-supervisor-2000/backend/business_logic.py:1885` (`change_collection_status`)
- **Existing collection modal:** `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_collection.html`
- **Bike details page:** `/home/xivind/code/velo-supervisor-2000/frontend/templates/bike_details.html`
- **Database model:** `/home/xivind/code/velo-supervisor-2000/backend/database_model.py`
- **Application overview:** `/home/xivind/code/velo-supervisor-2000/CLAUDE.md`

---

**Document Status:** Complete - Ready for UX Designer Review
**Date Completed:** 2025-12-13
**Next Agent:** @ux-designer
