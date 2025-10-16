# Component Quick Swap - Requirements Document

**Feature:** Component Quick Swap
**Date:** 2025-10-11
**Status:** Complete
**Prepared by:** @product-manager
**Ready for:** @architect and @ux-designer (in parallel)

---

## Executive Summary

The Component Quick Swap feature is a streamlined workflow that allows users to replace one installed component with another component (either existing or newly created) in a single operation. This addresses a critical pain point where users currently must navigate to multiple pages and perform separate status changes to accomplish what should be a simple "swap" operation.

**Primary Use Cases:**
- Replacing worn components (e.g., brake pads reaching end of life)
- Seasonal component changes (e.g., swapping summer tires for winter tires)
- Rotating between multiple components of the same type (e.g., alternating waxed chains)

**Key Value Proposition:** Reduce a 4-6 step process across multiple pages into a single modal interaction.

---

## Context & Problem Statement

### Current Pain Points

Users currently face significant friction when replacing components:

1. **Multiple page navigations required**: Must visit two separate component detail pages
2. **Manual information re-entry**: When replacing a component with a similar one (e.g., new brake pads of same type), users must manually re-enter component type, service intervals, and expected lifetime
3. **Separate status operations**: Must perform two distinct status changes (uninstall/retire old + install new) rather than one atomic swap
4. **Cognitive overhead**: Must remember to update both components and ensure consistency

### User Scenarios

**Scenario 1: Worn Brake Pads**
> Sarah's brake pads have reached 2,500km (end of expected lifetime: 2,500km). She needs to retire the old pads and install new ones with the same specifications.
>
> **Current workflow:** Navigate to old brake pads page, change status to "Retired", navigate back to component overview, create new brake pads, manually enter all fields (type, service interval, lifetime), set status to "Installed", select bike.
>
> **Desired workflow:** Click "Quick Swap" button on old brake pads row, choose "Retire" (pre-selected because lifetime reached), check "Copy component", edit component name, click "Swap".

**Scenario 2: Seasonal Tire Change**
> Marcus is switching from summer tires to winter tires (both already exist as components in the system). Summer tires have 1,200km remaining (out of 5,000km expected lifetime).
>
> **Current workflow:** Navigate to summer tires page, change status to "Not installed", navigate to winter tires page, change status to "Installed", select bike.
>
> **Desired workflow:** Click "Quick Swap" on summer tires row, choose "Not installed" (pre-selected because lifetime not reached), select winter tires from dropdown, click "Swap".

**Scenario 3: Rotating Waxed Chains**
> Elena rotates between two pre-waxed chains every 200km to maintain optimal performance. Both chains already exist in the system.
>
> **Current workflow:** Navigate to Chain A page, set to "Not installed", navigate to Chain B page, set to "Installed" on correct bike.
>
> **Desired workflow:** On bike details page, click "Quick Swap" button next to Chain A, select Chain B from dropdown of "Not installed" chains, click "Swap".

---

## User Personas

### Primary Persona: The Meticulous Maintainer
- **Profile**: Tracks all component lifecycles, performs preventive maintenance
- **Frequency**: Swaps components 2-4 times per month
- **Pain point**: Friction in workflow makes tracking tedious
- **Needs**: Fast, accurate component replacement with minimal data re-entry

### Secondary Persona: The Multi-Bike Enthusiast
- **Profile**: Owns multiple bikes with seasonal component sets (summer/winter wheels, different cassettes)
- **Frequency**: Swaps components seasonally (4-8 times per year)
- **Pain point**: Managing multiple component sets across bikes
- **Needs**: Quick component swapping without losing component history

---

## Detailed Requirements

### Functional Requirements

#### FR-1: Quick Swap Access Points

The quick swap feature must be accessible from three locations:

**FR-1.1: Component Overview Page**
- Each installed component row in the component table displays a "Quick Swap" button
- Clicking the button opens the Quick Swap modal pre-filled with that component
- Modal shows all installed components in the "Component to swap out" dropdown

**FR-1.2: Bike Details Page**
- Each installed component row in the bike's component table displays a "Quick Swap" button
- Clicking the button opens the Quick Swap modal pre-filled with that component
- Modal shows only components installed on that specific bike in the "Component to swap out" dropdown

**FR-1.3: Component Details Page**
- Page displays a "Quick Swap" button (consistent with other action buttons)
- Clicking the button opens the Quick Swap modal pre-filled with the component being viewed
- Modal shows all installed components of all types in the dropdown (unless context limits to current bike)

#### FR-2: Component Selection (Old Component)

**FR-2.1: Eligibility**
- Only components with `installation_status = "Installed"` can be selected to swap out
- The dropdown is filtered to show only eligible components

**FR-2.2: Display Format**
- Components displayed as: `[Component Name] ([Component Type]) - [Bike Name]`
- Example: "Shimano 105 Brake Pads (Brake Pads) - Road Bike"

**FR-2.3: Context Filtering**
- On Component Overview page: Show all installed components
- On Bike Details page: Show only components installed on that bike
- On Component Details page: Pre-select the current component, show all installed components

#### FR-3: Old Component Fate Selection

**FR-3.1: Available Options**
Users must choose the fate of the component being swapped out:
- "Not installed" - Component is removed but can be re-installed later
- "Retired" - Component has reached end of life and should not be re-used

**FR-3.2: Default Selection Logic**
The default selection must be intelligently determined:

```
IF component_distance >= lifetime_expected THEN
    default = "Retired"
ELSE
    default = "Not installed"
END IF
```

**FR-3.3: User Override**
- Users can always override the default selection
- Selection persists until user changes it or modal is closed/re-opened

**FR-3.4: Retired Component Implications**
- Components marked "Retired" are excluded from the "swap to" dropdown
- Retired components should not appear in future quick swap operations

#### FR-4: New Component Source Selection

Users must be able to swap TO a component from two sources:

**FR-4.1: Select Existing Component**
- Dropdown shows components with `installation_status = "Not installed"`
- Components with `installation_status = "Retired"` are excluded
- Components must match the same `component_type` as the component being swapped out
- Display format: `[Component Name] ([Distance] km)`
- Example: "Shimano Ultegra Brake Pads (250 km)"

**FR-4.2: Create New Component (with Copy)**
- Checkbox labeled "Create new component (copy settings from current)"
- When checked:
  - Existing component dropdown is disabled
  - Inline form fields appear for creating new component
  - Fields are pre-populated from the component being swapped out

**FR-4.3: Copied Fields (when creating new)**
The following fields are copied from the old component and displayed for editing:

| Field | Source | Editable | Required |
|-------|--------|----------|----------|
| Component Type | Old component | No (locked) | Yes |
| Component Name | Old component | Yes | Yes |
| Service Interval | Old component | Yes | No |
| Expected Lifetime | Old component | Yes | No |
| Cost | Old component | Yes | No |
| Notes | Old component | Yes | No |

**FR-4.4: Non-Copied Fields**
- Component ID: Auto-generated (not visible to user)
- Distance: Starts at 0 km
- Installation Status: Set to "Installed"
- Bike ID: Inherited from old component
- Updated Date: User-specified (defaults to today)

#### FR-5: Component Type Matching Enforcement

**FR-5.1: Strict Type Matching**
- The system MUST enforce that the new component has the same `component_type` as the old component
- This is a hard requirement - swap cannot proceed if types don't match
- Error message: "Components must be of the same type. Cannot swap [Type A] with [Type B]."

**FR-5.2: Benefits of Type Matching**
- Shorter dropdowns (pre-filtered to same type + "Not installed")
- Prevents logical errors (e.g., swapping brake pads with a saddle)
- Simplifies bike component state (no duplicate component types on same bike, unless intentional)

#### FR-6: Component Health Warnings

**FR-6.1: End of Life Warning**
When selecting a component to swap TO, if that component meets any of these conditions:

```
IF new_component.lifetime_remaining <= 500 km THEN
    show warning
END IF

IF new_component.service_next <= 100 km THEN
    show warning
END IF
```

**FR-6.2: Warning Display**
- Warning appears as an alert banner above the component selection
- Icon: Warning triangle (Bootstrap warning icon)
- Message examples:
  - "This component has only 250 km remaining before end of life. Are you sure you want to install it?"
  - "This component needs service in 50 km. Consider servicing before installation."

**FR-6.3: Warning Behavior**
- Warning does NOT block the swap (user can proceed)
- Warning persists until user changes selection or closes modal
- User can dismiss warning but it reappears if modal is re-opened with same selection

#### FR-7: Bike Assignment Logic

**FR-7.1: Bike Determination**
- The bike is ALWAYS determined from the component being swapped out
- The new component automatically inherits the `bike_id` from the old component
- No bike selection dropdown is shown (bike context is implicit)

**FR-7.2: Bike Display**
- Modal displays the bike name prominently: "Swapping component on: [Bike Name]"
- This provides context and confirmation to the user

#### FR-8: Date and Time Handling

**FR-8.1: Single Date for Both Operations**
- Both operations (remove old + install new) use the SAME date/time
- This represents the moment of the swap operation

**FR-8.2: Date Input Behavior**
- Default value: Current date and time
- Format: YYYY-MM-DD HH:MM (consistent with existing date inputs)
- User can edit the date (e.g., if performing the swap retroactively)
- Date validation: Cannot be in the future

**FR-8.3: Date Picker**
- Use existing datepicker-input pattern (consistent with create component modal)
- Include calendar icon toggle (🗓 emoji, consistent with existing pattern)

#### FR-9: History Recording

**FR-9.1: Component History Records**
The swap operation creates TWO separate history records in the `component_history` table:

**Record 1 (Old Component Uninstall/Retire):**
```
history_id: [auto-generated UUID]
component_id: [old_component_id]
bike_id: [bike_id from old component]
component_name: [old component name]
updated_date: [user-specified swap date]
update_reason: "Not installed" OR "Retired" (based on user selection)
distance_marker: [component_distance at time of swap]
```

**Record 2 (New Component Install):**
```
history_id: [auto-generated UUID]
component_id: [new_component_id]
bike_id: [bike_id from old component]
component_name: [new component name]
updated_date: [user-specified swap date]
update_reason: "Installed"
distance_marker: [current bike total_distance]
```

**FR-9.2: No Special "Swapped" Entry**
- History records are treated as independent status changes
- No special "swapped from X to Y" indicator in history
- The relationship is implied by matching timestamps and bike_id

**FR-9.3: History Display**
- Component detail pages show these as separate historical records
- Records appear in chronological order with all other history
- No visual indication that they were part of a swap operation

#### FR-10: Duplicate Component Type Checking

**FR-10.1: No Validation**
The system should NOT check if the bike already has a component of the same type installed.

**FR-10.2: Rationale**
- Some bikes legitimately have multiple components of the same type (e.g., two bottle cages, multiple lights)
- Component types table has a `max_quantity` field that may be used for validation in the future, but is not part of MVP
- User is responsible for managing component assignments

#### FR-11: User Workflow

**FR-11.1: Step-by-Step Flow**

```
Step 1: User initiates quick swap
  ↓
Step 2: System presents swap interface with old component pre-selected (if context available)
  ↓
Step 3: User confirms/selects component to swap out
  ↓
Step 4: User selects fate of old component (default: "Not installed" or "Retired")
  ↓
Step 5: User either:
  Option A: Selects existing "Not installed" component
  Option B: Chooses to create new component with copied settings
  ↓
Step 6: System validates (type matching, required fields)
  ↓
Step 7: System shows warnings if applicable (component health)
  ↓
Step 8: User confirms the swap operation
  ↓
Step 9: System performs atomic swap operation
  ↓
Step 10: System provides success feedback, updates display
```

**FR-11.2: Required Data Elements**

The swap interface must present these data elements to the user:

| Data Element | When Visible | Behavior |
|------------|------------|---------------|
| Bike context | Always visible | Display which bike the swap is occurring on |
| Component to swap out | Always visible | Pre-filled from context, or allow user to select |
| Fate selection | Always visible | Default set by lifetime logic, user can override |
| Swap to existing component | When not creating new | Filtered by type and "Not installed" status |
| Create new component option | Always available | Alternative to selecting existing component |
| New component fields | When creating new | Pre-filled from old component, component type locked |
| Health warnings | When applicable | Displayed when selected component has issues |
| Swap date | Always visible | Defaults to current date/time, user can edit |

#### FR-12: Backend Orchestration

**FR-12.1: Atomic Operation**
The swap must be treated as a single atomic operation:
- Either BOTH operations succeed (old component status change + new component status change/creation)
- OR the entire operation fails and rolls back (no partial state)

**FR-12.2: Required Backend Endpoint**
A new orchestrator endpoint is needed (technical implementation is architect's responsibility):
- Endpoint path suggestion: `POST /api/swap_component`
- Must handle both "swap to existing" and "swap to new (create)" scenarios
- Must validate all business rules before committing changes
- Must create both history records in a transaction

**FR-12.3: Validation Requirements**
The endpoint must validate:
- Old component exists and is "Installed"
- New component (if existing) exists and is "Not installed"
- Component types match
- Required fields are present (if creating new)
- Swap date is valid (not in future)
- Bike context is preserved

---

## User Stories with Acceptance Criteria

### User Story 1: Quick Swap from Component Overview Page

**As a** component tracker
**I want to** initiate a quick swap from the component overview page
**So that** I can replace any installed component without navigating to its detail page

**Acceptance Criteria:**
- [ ] Each installed component row in the component overview table displays a "Quick Swap" button
- [ ] Button is visually consistent with existing action buttons (same style, placement)
- [ ] Button is only visible for components with `installation_status = "Installed"`
- [ ] Clicking the button opens the Quick Swap modal
- [ ] Modal is pre-filled with the selected component in the "Component to swap out" dropdown
- [ ] Dropdown shows all installed components (across all bikes)
- [ ] User can change the pre-selected component if desired

**Edge Cases:**
- What if there are no installed components? Button should not appear on any rows
- What if component is installed but bike no longer exists? Display warning in modal, prevent swap

**Out of Scope (Future Enhancements):**
- Bulk swap operations (swapping multiple components at once)

---

### User Story 2: Quick Swap from Bike Details Page

**As a** bike owner
**I want to** initiate a quick swap from the bike details page
**So that** I can replace components on a specific bike without seeing components from other bikes

**Acceptance Criteria:**
- [ ] Each installed component row in the bike details component table displays a "Quick Swap" button
- [ ] Button is only visible for components with `installation_status = "Installed"` on this bike
- [ ] Clicking the button opens the Quick Swap modal pre-filled with that component
- [ ] Modal displays "Swapping component on: [Bike Name]" at the top
- [ ] "Component to swap out" dropdown shows only components installed on THIS bike
- [ ] "Swap to" dropdown is filtered to same component type + "Not installed" status
- [ ] New component inherits the bike_id from the old component

**Edge Cases:**
- What if bike has only one installed component? Swap should still work, just shorter dropdowns
- What if there are no "Not installed" components of the same type? User must use "Create new component" option

**Out of Scope (Future Enhancements):**
- Swapping components between different bikes

---

### User Story 3: Quick Swap from Component Details Page

**As a** user viewing a component's detail page
**I want to** initiate a quick swap directly from this page
**So that** I don't have to navigate back to overview/bike pages to perform the swap

**Acceptance Criteria:**
- [ ] Component details page displays a "Quick Swap" button in the action button area
- [ ] Button is only visible if component has `installation_status = "Installed"`
- [ ] Clicking the button opens the Quick Swap modal
- [ ] Modal is pre-filled with the current component as the "component to swap out"
- [ ] User can see which bike the component is currently installed on
- [ ] After successful swap, user is redirected to the component overview page (or remains on same page with updated data)

**Edge Cases:**
- What if component status changes between page load and button click? Validate on submit, show error if no longer installed
- What if user navigates directly to component detail page via URL (not from overview)? Button should still work

**Out of Scope (Future Enhancements):**
- Quick swap directly to the NEW component's detail page after swap

---

### User Story 4: Swap to Existing "Not Installed" Component

**As a** user with pre-existing spare components
**I want to** swap an installed component with an existing "Not installed" component
**So that** I can rotate between multiple components without creating duplicates

**Acceptance Criteria:**
- [ ] "Swap to" dropdown shows all components with `installation_status = "Not installed"`
- [ ] Dropdown is filtered to show only components matching the same `component_type` as old component
- [ ] Components with `installation_status = "Retired"` do NOT appear in dropdown
- [ ] Each dropdown option displays: "[Component Name] ([Distance] km)"
- [ ] Selecting a component populates the preview area (if implemented)
- [ ] If selected component has low lifetime remaining (<=500km), warning appears
- [ ] If selected component needs service soon (<=100km), warning appears
- [ ] User can proceed with swap despite warnings
- [ ] After swap: old component status changes to selected fate, new component status changes to "Installed"

**Edge Cases:**
- What if no "Not installed" components of matching type exist? Dropdown shows "No available components", user must check "Create new"
- What if selected component has 0km distance? No warning, proceed normally
- What if selected component belongs to a different bike? Should work (component is "Not installed" so no bike assignment conflict)

**Out of Scope (Future Enhancements):**
- Previewing full details of selected component before swap
- Filtering dropdown by additional criteria (e.g., cost, age)

---

### User Story 5: Create New Component During Swap (with Copy)

**As a** user replacing worn components
**I want to** create a new component during the swap with settings copied from the old component
**So that** I don't have to manually re-enter component type, service intervals, and lifetime expectations

**Acceptance Criteria:**
- [ ] Modal displays checkbox labeled "Create new component (copy settings from current)"
- [ ] When checkbox is checked, existing component dropdown is disabled
- [ ] Inline form fields appear below the checkbox
- [ ] Fields are pre-populated with values from the old component:
  - Component Name (editable)
  - Component Type (NOT editable, locked/disabled)
  - Service Interval (editable, can be blank)
  - Expected Lifetime (editable, can be blank)
  - Cost (editable, can be blank)
  - Notes (editable, can be blank)
- [ ] User can edit all fields except Component Type
- [ ] Component Name is required (validation on submit)
- [ ] When checkbox is unchecked, inline form disappears and dropdown re-enables
- [ ] After successful swap, new component is created with `installation_status = "Installed"` and assigned to the bike

**Edge Cases:**
- What if old component has null/empty values for service interval or lifetime? Copy as-is (empty fields in form)
- What if user checks the box, fills in form, then unchecks the box? Form data is discarded, dropdown selection is restored
- What if Component Name field is left unchanged (same as old component)? Allow it - user may want to track generations (e.g., "Chain A v1", "Chain A v2")

**Out of Scope (Future Enhancements):**
- Auto-incrementing component names (e.g., "Brake Pads #3")
- Copying additional fields like collections, tags, or custom metadata

---

### User Story 6: Default Fate Selection Based on Lifetime

**As a** user swapping out a worn component
**I want to** have "Retired" pre-selected when the component has reached its expected lifetime
**So that** I don't accidentally mark end-of-life components as "Not installed" and risk re-using them

**Acceptance Criteria:**
- [ ] When opening modal, system checks: `old_component.component_distance >= old_component.lifetime_expected`
- [ ] If condition is true, "Retired" radio button is pre-selected
- [ ] If condition is false, "Not installed" radio button is pre-selected
- [ ] User can override the default selection at any time
- [ ] Selection persists while modal is open (doesn't reset when user changes other fields)
- [ ] If user closes modal and re-opens, default logic re-applies (doesn't remember previous override)

**Edge Cases:**
- What if component has no expected lifetime set (null or 0)? Default to "Not installed"
- What if component distance equals exactly the expected lifetime? Default to "Retired" (use >= condition)
- What if component is way over expected lifetime (e.g., 5000km on a 2500km component)? Default to "Retired", no special handling

**Out of Scope (Future Enhancements):**
- Smart suggestions based on component condition or service history
- Warning if user selects "Not installed" for a component that's reached end of life

---

### User Story 7: Enforce Component Type Matching

**As a** system administrator
**I want to** ensure users can only swap components of the same type
**So that** bike configurations remain logically consistent and prevent errors

**Acceptance Criteria:**
- [ ] "Swap to" dropdown only shows components with `component_type` matching the old component
- [ ] When creating new component, Component Type field is auto-populated and disabled (not editable)
- [ ] If user somehow attempts to swap to a different type (e.g., via API), backend validation rejects the operation
- [ ] Error message clearly states: "Components must be of the same type. Cannot swap [Type A] with [Type B]."
- [ ] Error message appears in modal (not as page-level error)
- [ ] User can close error message and correct their selection

**Edge Cases:**
- What if component type is renamed or deleted between page load and swap? Validate on submit, show error if type mismatch
- What if no components of matching type exist and user doesn't want to create new? Show informational message: "No components available. Please create a new component."

**Out of Scope (Future Enhancements):**
- Cross-type swapping with explicit user confirmation (e.g., swapping "Road Cassette" with "MTB Cassette")
- Type compatibility rules (e.g., some saddles fit on any bike)

---

### User Story 8: Warn About Components Near Service or End of Life

**As a** proactive maintainer
**I want to** receive warnings when swapping TO a component that's close to needing service or retirement
**So that** I can make informed decisions and avoid installing components that will immediately need attention

**Acceptance Criteria:**
- [ ] When user selects a component to swap to (from dropdown), system checks:
  - `new_component.lifetime_remaining <= 500` km
  - `new_component.service_next <= 100` km
- [ ] If either condition is true, warning banner appears in modal
- [ ] Warning displays relevant message:
  - End of life: "This component has only [X] km remaining before end of life. Are you sure you want to install it?"
  - Service needed: "This component needs service in [X] km. Consider servicing before installation."
- [ ] Warning includes Bootstrap warning icon (triangle with exclamation mark)
- [ ] Warning does NOT block swap operation (user can still click "Swap Components")
- [ ] Warning disappears if user changes component selection to one that's healthy
- [ ] Warning reappears if user re-selects the same component (not dismissible permanently)

**Edge Cases:**
- What if component meets BOTH conditions (needs service AND near end of life)? Show both warnings stacked
- What if component has negative lifetime remaining (over lifetime)? Show end of life warning
- What if service_next or lifetime_remaining is null? Don't show warning for that metric

**Out of Scope (Future Enhancements):**
- Configurable warning thresholds (e.g., user sets 200km instead of 500km)
- Blocking swap if component is retired or in critical condition
- Suggestions for servicing component before installing

---

### User Story 9: Single Date for Swap Operation

**As a** user performing a component swap
**I want to** specify a single date/time for the swap operation
**So that** both components' history records reflect the same moment of change

**Acceptance Criteria:**
- [ ] Modal displays a single date/time input field labeled "Swap Date"
- [ ] Date input uses the existing datepicker-input pattern (consistent with create component modal)
- [ ] Calendar icon toggle (🗓) is present and functional
- [ ] Default value is current date and time (format: YYYY-MM-DD HH:MM)
- [ ] User can edit the date to perform retroactive swaps
- [ ] Date validation: Cannot be in the future (show error if user tries)
- [ ] Both history records (old component uninstall + new component install) use the same date
- [ ] Both component records' `updated_date` field is set to this date

**Edge Cases:**
- What if user enters a date before the old component was originally installed? Allow it (user may be correcting historical data)
- What if user enters a date before the new component was created? Allow it for existing components, block for new component creation (can't install before creation)
- What if swap date is far in the past (e.g., 2 years ago)? Allow it - user may be retroactively logging maintenance

**Out of Scope (Future Enhancements):**
- Time zone handling (assume all times are local time)
- Separate dates for uninstall and install operations
- Auto-suggesting date based on last service or ride date

---

## Non-Functional Requirements

### NFR-1: Performance
- Modal must open in < 500ms on standard hardware
- Dropdown filtering must occur in < 200ms
- Swap operation must complete in < 2 seconds for typical scenarios

### NFR-2: Usability
- Modal must be operable with keyboard only (tab navigation, enter to submit, ESC to close)
- Form validation errors must be clear and actionable
- Success confirmation must be visible and clear

### NFR-3: Data Integrity
- Swap operation must be atomic (all-or-nothing)
- Database constraints must prevent orphaned records
- History records must accurately reflect state changes

### NFR-4: Browser Compatibility
- Must work on modern browsers (Chrome, Firefox, Safari, Edge)
- Must be responsive (mobile, tablet, desktop)
- Must follow existing Bootstrap 5 patterns

### NFR-5: Accessibility
- Modal must be screen-reader accessible
- Form labels must be properly associated with inputs
- Focus management must be logical (return focus after modal closes)

---

## Questions for UX Designer

The following questions should guide the UI/UX design for the Component Quick Swap feature:

### General Interface Design
1. **Access Points**: How should users access the quick swap feature from three different pages (component overview, bike details, component details)? What visual treatment makes the feature discoverable without cluttering existing layouts?

2. **Interface Pattern**: What interface pattern best suits this workflow - modal dialog, slide-out panel, inline expansion, or something else? Consider the amount of information to display and the need for user focus.

3. **Workflow Presentation**: How should the multi-step workflow (select old component → choose fate → select/create new component → confirm) be presented to users? Should it be a single form, wizard-style steps, or progressive disclosure?

### Component Selection
4. **Old Component Selection**: On pages where multiple components are available, how should users select which component to swap out? What information should be shown in the selection interface to help users choose?

5. **Component Display Format**: How should components be displayed in selection interfaces? What information is most helpful (component name, type, bike, distance, health status)?

6. **Empty States**: How should the system communicate when no suitable components are available to swap to? What guidance should users receive?

### Fate Selection
7. **Default Fate Indication**: How can we make the default fate selection (Retired vs. Not installed) obvious to users while still allowing easy override? Should there be visual indication of why a particular default was chosen?

8. **Fate Options Presentation**: What's the best way to present the two fate options - radio buttons, toggle switch, dropdown, or another pattern?

### Create vs. Select Workflow
9. **Swap Source Choice**: How should users choose between swapping to an existing component vs. creating a new one? What interaction pattern makes this decision clear?

10. **Copy Settings Option**: How should the "copy settings from current component" functionality be presented? Should it be opt-in (checkbox) or the default behavior with opt-out?

11. **Inline Form Display**: When creating a new component, how should the form fields appear? Should they replace the existing component selection, appear alongside it, or use another pattern?

12. **Locked Component Type**: How should we visually communicate that the component type is locked (not editable) when creating a new component during swap?

### Warnings and Feedback
13. **Component Health Warnings**: How should warnings about components near end of life or needing service be displayed? What level of prominence is appropriate for non-blocking warnings?

14. **Multiple Warnings**: When a component has multiple issues (needs service AND near end of life), how should multiple warnings be presented?

15. **Validation Errors**: How should validation errors be displayed? Should they be inline, at the top of the form, or use another pattern?

16. **Success Feedback**: After a successful swap, what feedback should users receive? Should they stay on the current page, be redirected, or see a confirmation?

### Date and Context
17. **Swap Date Input**: How should the swap date input be presented? Should it be prominent or de-emphasized (since most swaps use current date)?

18. **Bike Context Display**: How should the bike context ("swapping on Bike X") be displayed to provide clarity without taking excessive space?

### Responsive Design
19. **Mobile Experience**: How should the swap workflow be adapted for mobile devices? What simplifications or adaptations are needed for smaller screens?

20. **Tablet Experience**: What layout works best for tablet screens that have more space than mobile but less than desktop?

### Consistency
21. **Pattern Reuse**: Which existing UI patterns from the application should be reused (modals, forms, buttons, date pickers)? How can we maintain visual consistency?

22. **Button Placement**: Where should the "Quick Swap" action buttons be placed on each of the three access points to be discoverable but not intrusive?

23. **Action Button Treatment**: What visual treatment should the "Quick Swap" button receive on different pages (primary, secondary, icon-only, icon+text)?

### Edge Cases
24. **Pre-selection Indication**: When a component is pre-selected from context, how should this be visually indicated to the user?

25. **Type Matching Filter**: How should we communicate to users that the component list is filtered to match types? Should this be explicit or implicit?

---

## Edge Cases & Error Handling

### Edge Case 1: No Available Components to Swap To
**Scenario:** User wants to swap, but no "Not installed" components of matching type exist

**Handling:**
- System communicates that no existing components are available
- User is guided to create new component option
- Form for creating new component becomes the primary path
- User must create new component to proceed

### Edge Case 2: Component Status Changed Since Page Load
**Scenario:** User initiates swap on component that was "Installed", but another user (or process) changed it to "Not installed" before swap submission

**Handling:**
- Backend validation detects status mismatch
- Return error message: "This component is no longer installed. Please refresh the page."
- Interface remains available with error displayed
- User can dismiss and refresh page

### Edge Case 3: Selected "Swap To" Component No Longer "Not Installed"
**Scenario:** User selects existing component, but it was installed on another bike before swap submission

**Handling:**
- Backend validation detects status conflict
- Return error message: "Selected component is no longer available. It may have been installed on another bike."
- User can change selection or dismiss and refresh

### Edge Case 4: Bike No Longer Exists
**Scenario:** Old component's bike_id references a deleted bike

**Handling:**
- System displays warning: "Warning: The bike this component was assigned to no longer exists."
- Swap operation is blocked until issue is resolved
- Suggest: "Please update the component's bike assignment before swapping."

### Edge Case 5: Duplicate Component Name When Creating New
**Scenario:** User creates new component with name that already exists (exact match)

**Handling:**
- Allow it (component names don't have to be unique)
- System distinguishes by component_id
- Optional: Show informational message: "A component with this name already exists. Components will be distinguished by ID."

### Edge Case 6: User Changes from Create New to Select Existing
**Scenario:** User chooses to create new component, fills in fields, then switches to selecting existing

**Handling:**
- Create new component interface closes/hides
- Select existing component interface becomes active
- Form data is discarded (not saved)
- If user switches back to create new, form is re-populated from old component (not previous user input)

### Edge Case 7: Swap Date in the Future
**Scenario:** User enters a swap date in the future

**Handling:**
- Client-side validation shows error: "Swap date cannot be in the future."
- Submission is disabled until date is corrected
- Backend also validates and rejects if validation is bypassed

### Edge Case 8: Component at Exactly 0 km
**Scenario:** User swaps to a component with exactly 0 km distance

**Handling:**
- No special handling needed
- No warnings displayed
- Swap proceeds normally
- Component starts accumulating distance from next ride

### Edge Case 9: Old Component Already "Retired" (shouldn't happen, but validate)
**Scenario:** User somehow initiates swap on a component that's already retired

**Handling:**
- Quick swap action should not be available on retired components (front-end prevention)
- Backend validation rejects: "Cannot swap retired components."
- Suggest: "Please refresh the page."

### Edge Case 10: Type Matching with Null/Empty Type
**Scenario:** Component has null or empty component_type field (data integrity issue)

**Handling:**
- Backend validation rejects swap
- Error message: "Component type is missing. Please update the component before swapping."
- Log warning for administrator to investigate data integrity

---

## Validation Rules

### Client-Side Validation (Modal)

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| Component to swap out | Must be selected | "Please select a component to swap out." |
| Fate selection | Must select one option | "Please choose what to do with the old component." |
| Swap to (dropdown) | Required if "create new" unchecked | "Please select a component or create a new one." |
| Component Name (create new) | Required, max 100 chars | "Component name is required." |
| Swap Date | Required, valid date format, not in future | "Please enter a valid date (not in the future)." |

### Server-Side Validation (Backend)

| Validation Check | Error Response |
|-----------------|---------------|
| Old component exists | 404: "Component not found." |
| Old component is "Installed" | 400: "Component must be installed to be swapped." |
| New component exists (if selecting existing) | 404: "Selected component not found." |
| New component is "Not installed" (if selecting existing) | 400: "Selected component is not available for installation." |
| Component types match | 400: "Components must be of the same type." |
| Swap date not in future | 400: "Swap date cannot be in the future." |
| Required fields present (if creating new) | 400: "Missing required fields: [field names]." |
| Bike exists | 404: "Bike not found." |

### Business Logic Validation

| Rule | Enforcement |
|------|-------------|
| Only "Installed" components can be swapped out | Hard requirement (blocks operation) |
| Only "Not installed" components can be swapped to | Hard requirement (blocks operation) |
| Component types must match | Hard requirement (blocks operation) |
| Retired components excluded from "swap to" | Filter at query level (don't show in dropdown) |
| One swap = two history records | Enforced at backend transaction level |
| Atomic operation (all-or-nothing) | Database transaction with rollback on failure |

---

## Integration Points

### Existing Features Impacted

**1. Component Status Management**
- Quick Swap creates history records in `component_history` table
- Existing status change logic is reused (not duplicated)
- History display on component detail pages shows swap-related records

**2. Component Creation**
- "Create new component during swap" reuses existing component creation logic
- New component validation rules must be consistent with create component modal
- Default field population follows existing patterns

**3. Bike Details Page**
- Component table on bike details page needs new "Quick Swap" button column
- Table must refresh after successful swap to show updated component list

**4. Component Overview Page**
- Component table needs new "Quick Swap" button column
- Table must refresh after successful swap to show updated statuses

**5. Component Details Page**
- Page needs new "Quick Swap" button in action area
- May need redirect logic after swap (TBD by architect/UX designer)

### Database Tables Affected

**1. `components` table**
- Fields modified: `installation_status`, `bike_id`, `updated_date`
- Two records updated per swap (old component + new component)

**2. `component_history` table**
- Two new records inserted per swap
- Fields: `history_id`, `component_id`, `bike_id`, `component_name`, `updated_date`, `update_reason`, `distance_marker`

**3. `bikes` table**
- NOT directly modified by quick swap
- Bike's component associations are managed through `components.bike_id` foreign key

### API Endpoints Needed

**New Endpoint (Orchestrator):**
- `POST /api/swap_component`
- Handles both "swap to existing" and "swap to new (create)" scenarios
- Request body includes: old_component_id, new_component_id (optional), new_component_data (optional), fate_selection, swap_date
- Response: Success (200) with updated component data, or Error (400/404) with message

**Existing Endpoints Reused:**
- Component creation logic (if creating new component during swap)
- Component status update logic (for changing installation_status)
- History record creation logic

### Strava Integration Considerations

**No direct Strava integration needed for this feature.**

However, note:
- Swapped components will continue to accumulate distance from subsequent rides
- Distance calculation logic must account for components swapped mid-ride (use component's updated_date to determine which rides count)
- Strava sync process is unaffected by quick swap feature

---

## Success Metrics

### Quantitative Metrics

**Efficiency Gain:**
- **Target:** Reduce average time to swap components by 60%
- **Measurement:** Time from initiating swap to completion (currently ~2-3 minutes across multiple pages, target < 1 minute in modal)

**Usage Adoption:**
- **Target:** 80% of component replacements use Quick Swap within 3 months of release
- **Measurement:** Ratio of (quick swaps) to (manual two-step status changes that result in a swap pattern)

**Error Reduction:**
- **Target:** Reduce component swap-related errors by 50%
- **Measurement:** Number of support tickets or user-reported issues related to incorrect component swaps, forgotten status changes, or inconsistent history

### Qualitative Metrics

**User Satisfaction:**
- Positive feedback on reduced friction in component management
- Users report feeling confident in swap operation (no fear of losing data)

**Feature Discoverability:**
- Users discover the Quick Swap button without needing documentation
- Button placement is intuitive and doesn't clutter existing UI

### Success Criteria (MVP)

The feature is considered successful if:
1. Users can complete all three use case scenarios (worn components, seasonal swap, chain rotation) using Quick Swap
2. No data integrity issues reported (history records accurate, component statuses correct)
3. Average swap time reduced to < 1 minute
4. Zero critical bugs in first month post-launch
5. Positive qualitative feedback from beta testers

---

## Open Questions for Architect

1. **Backend Architecture:**
   - Should the orchestrator endpoint be a new route in `main.py` or a new business logic function in `business_logic.py`?
   - How should we structure the transaction to ensure atomicity?
   - Should we validate component type matching at the database query level or in business logic?

2. **API Design:**
   - What should the exact request/response schema be for `POST /api/swap_component`?
   - Should we use a single endpoint for both "swap to existing" and "swap to new", or separate endpoints?
   - How should we handle partial failures (e.g., new component created but old component status change fails)?

3. **Database Considerations:**
   - Do we need any new indexes to optimize the dropdown queries (filtering by type + status)?
   - Should we add a `swap_operation_id` field to link related history records? (Optional, not required for MVP)
   - Any foreign key constraints that might block the swap operation?

4. **Performance:**
   - Are there any performance concerns with filtering large component lists in the dropdown?
   - Should we implement pagination or lazy loading for the "swap to" dropdown if user has hundreds of components?

5. **Error Handling:**
   - What HTTP status codes should we use for different validation failures?
   - Should we log failed swap attempts for debugging/auditing?
   - How should we handle concurrent swap operations on the same component?

---

## MVP vs. Future Enhancements

### MVP Scope (Must Have for First Release)

All features described in this document are considered MVP. Specifically:

- [x] Quick swap accessible from 3 locations (overview, bike details, component details)
- [x] Swap to existing "Not installed" component
- [x] Create new component during swap with copy functionality
- [x] Default fate selection based on lifetime
- [x] Component type matching enforcement
- [x] Health warnings for components near service/end of life
- [x] Single date for both operations
- [x] Two separate history records
- [x] Modal-based UI with responsive design

### Future Enhancements (Nice to Have, Post-MVP)

**Phase 2 Enhancements:**
- Bulk swap operations (swap multiple components at once)
- Quick swap directly between bikes (cross-bike component transfer)
- Component compatibility rules (beyond just type matching)
- Configurable warning thresholds (user sets their own limits)
- Swap operation reversal ("undo swap")

**Phase 3 Enhancements:**
- Visual component comparison in modal (side-by-side old vs new)
- Swap suggestions based on component health, service history, or seasonal patterns
- Swap templates for common operations (e.g., "Winter Tire Swap" template)
- Integration with workplans (auto-create workplan item when swapping worn component)

**Potential Long-Term Features:**
- Batch swap from CSV import (for users migrating from other systems)
- Swap analytics (most frequently swapped component types, average swap intervals)
- Predictive swap recommendations (machine learning based on ride patterns)

---

## Technical Considerations for Architect

### 1. Orchestrator Endpoint Design

The quick swap operation requires coordination of multiple database operations:

**Operation Sequence:**
1. Validate old component status (must be "Installed")
2. Validate new component (if selecting existing: must be "Not installed"; if creating: validate required fields)
3. Validate component type matching
4. BEGIN TRANSACTION
5. Create history record for old component (uninstall/retire)
6. Update old component status and bike_id
7. IF creating new component: Create new component record
8. Create history record for new component (install)
9. Update new component status and bike_id
10. COMMIT TRANSACTION
11. Return success response

**Error Handling:**
- Any validation failure: Return error before transaction
- Any database failure during transaction: ROLLBACK, return error
- Success: Return updated component data

**Suggested Approach:**
- Create a new business logic function: `swap_component_orchestrator()`
- Implement transaction management using Peewee's `database.atomic()`
- Reuse existing functions where possible (e.g., `create_component()`, `add_history_record()`)

### 2. Frontend-Backend Communication

**Request Payload Options:**

**Option A: Separate endpoints**
- `POST /api/swap_component_existing` (for swapping to existing component)
- `POST /api/swap_component_create` (for creating new component during swap)

**Option B: Single endpoint with conditional logic**
- `POST /api/swap_component`
- Request includes either `new_component_id` OR `new_component_data` (but not both)

**Recommendation:** Option B (single endpoint) for simplicity and consistency

**Sample Request Body:**
```json
{
  "old_component_id": "uuid-123",
  "fate": "Retired",
  "swap_date": "2025-10-11 14:30",
  "new_component_id": "uuid-456",  // Present if swapping to existing
  "new_component_data": {           // Present if creating new
    "component_name": "Shimano Ultegra Brake Pads",
    "component_type": "Brake Pads",
    "service_interval": 2000,
    "lifetime_expected": 2500,
    "cost": 450,
    "notes": "Front brake pads"
  }
}
```

### 3. Database Transaction Management

**Critical Requirements:**
- Use database transactions to ensure atomicity
- If any operation fails, rollback entire transaction
- Both history records must be created in same transaction

**Peewee Transaction Pattern:**
```python
with database.atomic():
    # All database operations here
    # If exception raised, auto-rollback
    # If successful, auto-commit
```

### 4. Component Type Validation

**Where to Enforce:**
- **Frontend:** Filter dropdowns to only show matching types (user experience)
- **Backend:** Validate before transaction begins (security/data integrity)

**Query Optimization:**
- When querying "Not installed" components for dropdown, filter by type in SQL:
  ```python
  Components.select().where(
      (Components.installation_status == "Not installed") &
      (Components.component_type == old_component.component_type)
  )
  ```

### 5. Concurrency Handling

**Potential Race Condition:**
- User A and User B both attempt to swap to the same "Not installed" component simultaneously
- One should succeed, one should fail

**Solution:**
- Use database-level locking or check-then-act validation
- In transaction, re-check component status before updating:
  ```python
  with database.atomic():
      component = Components.get_by_id(new_component_id)
      if component.installation_status != "Not installed":
          raise ValidationError("Component no longer available")
      # Proceed with swap
  ```

### 6. Performance Considerations

**Dropdown Query Optimization:**
- Current approach: Load all components, filter in Python
- Optimized approach: Use SQL WHERE clauses to filter at database level
- For large datasets (1000+ components): Consider pagination or search-as-you-type

**Index Recommendations:**
- Index on `components.installation_status` (for filtering "Installed" / "Not installed")
- Composite index on `(installation_status, component_type)` (for "swap to" dropdown query)
- Existing index on `component_id` (primary key) sufficient for lookups

---

## Dependencies & Requirements

### Dependencies on Existing Code

**1. Database Manager (`database_manager.py`):**
- Reuse component query functions for populating dropdowns
- May need new function: `get_components_by_status_and_type(status, component_type)`

**2. Business Logic (`business_logic.py`):**
- Reuse component creation logic
- Reuse history record creation logic
- May need new function: `swap_component_orchestrator(old_id, new_id_or_data, fate, date)`

**3. Frontend Templates:**
- Extend existing modal patterns (consistent styling and behavior)
- Reuse datepicker JavaScript from create component modal
- Reuse form validation patterns

**4. API Routes (`main.py`):**
- Add new route: `POST /api/swap_component`
- Reuse existing error handling and response formatting

### External Dependencies

**None.** This feature is self-contained within the Velo Supervisor 2000 application.

### Environment Requirements

**No changes to environment, dependencies, or deployment.**

---

## Next Steps

This requirements document is now **complete** and ready for handover to **@architect and @ux-designer** (work can proceed in parallel).

**Handover Summary:**
- **Feature:** Component Quick Swap
- **Scope:** Fully defined MVP with 9 user stories and comprehensive acceptance criteria
- **Key Decisions:**
  - Single atomic operation for swap (not two separate status changes)
  - Component type matching strictly enforced
  - Default fate selection based on component lifetime
  - Create new component with copy functionality
  - Single date for both operations (uninstall old + install new)
- **Open Questions:** Listed in "Open Questions for Architect" and "Questions for UX Designer" sections above

**Action Required from @architect:**
1. Review requirements and user stories
2. Design technical architecture for the orchestrator endpoint
3. Define API request/response schema
4. Specify database transaction approach
5. Identify any technical constraints or implementation risks
6. Create architecture handover document for @fullstack-developer

**Action Required from @ux-designer:**
1. Review requirements, user stories, and user workflow diagrams
2. Answer the 25 design questions in "Questions for UX Designer" section
3. Design interface pattern and layout for the swap workflow
4. Specify component placement for three access points (overview, bike details, component details)
5. Design warning displays, error states, and success feedback
6. Ensure consistency with existing UI patterns
7. Create UX specifications handover document for @fullstack-developer

**Note:** Both @architect and @ux-designer can work independently on their respective areas. The @fullstack-developer will integrate both outputs.

---

## References

- Existing UI patterns: `frontend/templates/modal_update_component_status.html`, `frontend/templates/modal_create_component.html`
- Database model: `backend/database_model.py` (Components, ComponentHistory tables)
- Component tables: `frontend/templates/component_overview.html`, `frontend/templates/bike_details.html`
- Application overview: `/home/xivind/code/velo-supervisor-2000/CLAUDE.md`

---

**Document Status:** Complete - Ready for Architect and UX Designer Review
**Date Completed:** 2025-10-11
**Date Revised:** 2025-10-11 (Updated to reflect product-manager role boundaries)
**Next Agents:** @architect and @ux-designer (parallel work)
