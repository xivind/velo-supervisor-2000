# UX Designer Handover: Component Quick Swap

**Feature:** Component Quick Swap
**Date:** 2025-10-11 (Revised 2025-10-12)
**Status:** Complete - Revised per stakeholder feedback
**Prepared by:** @ux-designer
**Ready for:** @fullstack-developer

**Revision Note:** This document was revised based on stakeholder feedback to:
- Use icon-only buttons (♻) in table rows, with text only outside tables
- Use `validation_modal` for all validation errors
- Follow Collections modal pattern EXACTLY for all user feedback (loading → report)
- Use NO toast notifications - modal feedback only
- Update endpoint name to `/quick_swap` per architect's specification
- Integrate existing date picker and validation functionality
- Ensure data structure matches architect's Form data requirements

---

## Context

This document provides complete UX specifications for the Component Quick Swap feature, which streamlines the process of replacing one installed component with another. The design supports three user entry points (component overview, bike details, component details), uses TomSelect for component selection, and follows the established patterns from the Collections feature.

**Requirements Source:** `.handovers/requirements/component-quick-swap-requirements.md`

**Architecture Status:** Architecture handover reviewed at `.handovers/architecture/component-quick-swap-architect-handover.md`. This UX design has been updated to align with architectural specifications and stakeholder feedback.

**Design Philosophy:**
- Follow the Collections feature pattern as primary reference
- Use TomSelect for all component dropdowns
- Mobile-first responsive design
- Progressive disclosure (show only relevant fields)
- Smart defaults based on component state
- Non-blocking warnings for user guidance

---

## Deliverables

### 1. Complete Modal Specification
- Modal structure, size, and layout following Collections pattern
- Form fields with Bootstrap components and validation
- TomSelect implementation for component selection
- Warning banner designs
- Button placement and states

### 2. User Workflows
- Step-by-step flows for each of the 3 access points
- Interaction patterns for "create vs select" decision
- Validation and error handling flows

### 3. Responsive Design
- Mobile, tablet, and desktop layouts
- Breakpoint specifications
- Touch-friendly interactions

### 4. Accessibility Specifications
- ARIA labels and roles
- Keyboard navigation patterns
- Screen reader considerations

---

## User Workflows

### Workflow 1: Quick Swap from Component Overview Page

**Trigger:** User clicks "Quick swap" button in component table row (installed component)

**Steps:**
1. User locates installed component in the component overview table
2. User clicks "Quick swap" button (♻ icon only in table) in the action column
3. Modal opens with:
   - Old component pre-selected in TomSelect dropdown
   - Fate defaulted based on lifetime (Retired if lifetime reached, otherwise "Not installed")
   - Bike context displayed prominently at top
   - "Swap to existing component" section ready
   - "Create new component" checkbox unchecked by default
4. User reviews pre-filled fate selection (can override)
5. User chooses path A or B:
   - **Path A: Select existing component**
     - User opens TomSelect dropdown for "Swap to" component
     - Dropdown shows only matching component type + "Not installed" status
     - User selects component
     - If selected component has health issues, warning banner appears
     - User reviews warning (can proceed)
   - **Path B: Create new component**
     - User checks "Create new component (copy settings from current)"
     - "Swap to" dropdown becomes disabled
     - Inline form appears with fields pre-populated from old component
     - Component type field is disabled (locked)
     - User edits component name (required) and other fields as needed
6. User reviews swap date (defaults to now, can edit)
7. User clicks "Swap components" button
8. If validation fails:
   - Validation modal (`validation_modal`) opens showing error message
   - User must dismiss validation modal and correct issues
   - Focus returns to invalid field after dismissal
9. If validation passes:
   - Quick swap modal closes
   - Loading modal (`modal_loading`) opens with spinner and "Swapping components..." message
   - Backend processes the swap operation
   - Loading modal closes automatically
   - Report modal (`modal_report`) opens showing success/failure message
   - User dismisses report modal
   - Component page refreshes to show updated states

**Edge Case:** No available components to swap to
- "Swap to" dropdown shows message: "No available components of this type"
- User must use "Create new component" option
- Guidance text appears: "Create a new component to complete the swap"

---

### Workflow 2: Quick Swap from Bike Details Page

**Trigger:** User clicks "Quick swap" button next to installed component in bike's component table

**Steps:**
Same as Workflow 1, with these differences:
- Old component dropdown is filtered to show only components installed on THIS bike
- Bike context banner shows the specific bike name: "Swapping component on: [Bike Name]"
- After user dismisses report modal, bike details page refreshes (not redirected elsewhere)

---

### Workflow 3: Quick Swap from Component Details Page

**Trigger:** User clicks "Quick swap" button in action button row at top of page

**Steps:**
Same as Workflow 1, with these differences:
- Old component is fixed (the component being viewed)
- Old component dropdown is pre-selected and disabled (cannot change)
- After user dismisses report modal, component details page refreshes (user stays on current page)

---

## Modal Specification

### Modal Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│ Quick swap                                                        [X]│
├─────────────────────────────────────────────────────────────────────┤
│ [INFO BANNER: Swapping component on: Road Bike]                    │
│                                                                     │
│ Component to swap out *                                            │
│ [🔍 Shimano 105 Brake Pads (Brake Pads) - Road Bike ▼]           │
│                                                                     │
│ Component fate *                                                    │
│ ( ) Not installed  (•) Retired                                     │
│ ℹ Defaulted to "Retired" because component has reached lifetime    │
│                                                                     │
│ ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│ Swap to existing component                                          │
│ [🔍 Select component... ▼]                                         │
│                                                                     │
│ ⚠ This component has only 250 km remaining before end of life     │
│                                                                     │
│ OR                                                                  │
│                                                                     │
│ [ ] Create new component (copy settings from current)              │
│                                                                     │
│ ─────────────────────────────────────────────────────────────────  │
│                                                                     │
│ Swap date *                                                         │
│ [2025-10-11 14:30] [🗓]                                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                           [Cancel] [Swap components]│
└─────────────────────────────────────────────────────────────────────┘
```

### Modal Properties

**Bootstrap Modal Configuration:**
- Modal class: `modal fade`
- Dialog class: `modal-dialog modal-lg` (large modal, consistent with Collections)
- Content class: `modal-content`
- Header class: `modal-header input-modal-header` (consistent with app patterns)
- Body class: `modal-body`
- Footer class: `modal-footer`

**Modal ID:** `quickSwapModal`

**Size:** Large (`modal-lg`) - provides space for TomSelect dropdowns and form fields

**Backdrop:** Static (clicking outside modal doesn't close it - prevents accidental data loss)

**Keyboard:** ESC key closes modal (with confirmation if form has changes)

---

## Form Fields Specification

### Section 1: Context Banner (Always Visible)

**Element:** Info alert banner
**Bootstrap Component:** `.alert .alert-info .mb-3`
**Content:** "Swapping component on: **[Bike Name]**"
**Icon:** 🚴 (bicycle emoji)
**Purpose:** Provides clear context for which bike the swap is happening on

**HTML Structure:**
```html
<div class="alert alert-info mb-3" role="alert">
    <strong>🚴 Swapping component on:</strong> <span id="swap-bike-name">Road Bike</span>
</div>
```

---

### Section 2: Component to Swap Out (Always Visible)

**Field:** Component selection dropdown (TomSelect)
**Label:** "Component to swap out" (bold)
**Required:** Yes (asterisk in label)
**Bootstrap Component:** TomSelect on `<select>` element

**Behavior:**
- **On Component Overview page:** Shows all installed components across all bikes
- **On Bike Details page:** Shows only components installed on the current bike
- **On Component Details page:** Pre-selected with current component, field is disabled

**TomSelect Configuration:**
```javascript
new TomSelect('#old_component_id', {
    plugins: ['remove_button'],
    maxItems: 1,
    valueField: 'value',
    labelField: 'text',
    searchField: ['text'],
    placeholder: 'Select component to swap out...'
});
```

**Option Format:**
```
[Component Name] ([Component Type]) - [Bike Name]
```

**Example Options:**
- "Shimano 105 Brake Pads (Brake Pads) - Road Bike"
- "Continental GP5000 Tire (Front Tire) - Gravel Bike"

**Validation:**
- Required field
- Must select exactly one component
- Error message: "Please select a component to swap out"

**Responsive Behavior:**
- Full width on all screen sizes
- Touch-friendly (minimum 44px tap target)

---

### Section 3: Component Fate Selection (Always Visible)

**Field:** Radio button group
**Label:** "Component fate" (bold)
**Required:** Yes (asterisk in label)
**Bootstrap Component:** `.form-check` (radio buttons)

**Options:**
1. "Not installed" - Component removed but can be re-installed
2. "Retired" - Component reached end of life, should not be re-used

**Default Selection Logic:**
```
IF component_distance >= lifetime_expected THEN
    default = "Retired"
ELSE
    default = "Not installed"
END IF
```

**Visual Treatment:**
```html
<div class="mb-3">
    <label class="form-label fw-bold">Component fate <span class="text-danger">*</span></label>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="fate" id="fate_not_installed" value="Not installed">
        <label class="form-check-label" for="fate_not_installed">
            Not installed
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="fate" id="fate_retired" value="Retired" checked>
        <label class="form-check-label" for="fate_retired">
            Retired
        </label>
    </div>
    <small class="form-text text-muted">
        ℹ Defaulted to "Retired" because component has reached expected lifetime
    </small>
</div>
```

**Info Text (conditional):**
- Show when fate is defaulted to "Retired": "ℹ Defaulted to 'Retired' because component has reached expected lifetime"
- Show when fate is defaulted to "Not installed": "ℹ Defaulted to 'Not installed' because component is within expected lifetime"
- Use Bootstrap `.form-text .text-muted` class

**Validation:**
- Required field (at least one must be selected)
- No error state needed (radio buttons always have selection)

**Responsive Behavior:**
- Radio buttons stack vertically on all screen sizes
- Touch-friendly tap targets

---

### Section 4: New Component Source Selection

This section uses progressive disclosure - show either the "Swap to existing" dropdown OR the "Create new" form, never both simultaneously.

#### Option A: Swap to Existing Component (Default View)

**Field:** Component selection dropdown (TomSelect)
**Label:** "Swap to existing component" (bold)
**Required:** Conditionally (if "Create new" is unchecked)
**Bootstrap Component:** TomSelect on `<select>` element

**Filtering Logic:**
- Show only components where:
  - `installation_status = "Not installed"`
  - `component_type` matches old component's type
- Exclude components where `installation_status = "Retired"`

**TomSelect Configuration:**
```javascript
new TomSelect('#new_component_id', {
    plugins: ['remove_button'],
    maxItems: 1,
    valueField: 'value',
    labelField: 'text',
    searchField: ['text'],
    placeholder: 'Select component...'
});
```

**Option Format:**
```
[Component Name] ([Distance] km)
```

**Example Options:**
- "Shimano Ultegra Brake Pads (250 km)"
- "SRAM Red Brake Pads (0 km)"

**Empty State:**
- If no matching components available, show: "No available components of this type"
- Placeholder text becomes: "Create new component instead"
- Dropdown appears disabled (greyed out)

**Validation:**
- Required IF "Create new component" checkbox is unchecked
- Error message: "Please select a component or create a new one"

**Responsive Behavior:**
- Full width on all screen sizes
- Touch-friendly

---

#### Option B: Create New Component (Progressive Disclosure)

**Trigger:** User checks "Create new component (copy settings from current)"

**Checkbox Specification:**
```html
<div class="form-check mb-3">
    <input class="form-check-input" type="checkbox" id="create_new_component" name="create_new_component">
    <label class="form-check-label" for="create_new_component">
        Create new component (copy settings from current)
    </label>
</div>
```

**When checked:**
1. "Swap to existing component" TomSelect becomes disabled (greyed out, cleared)
2. Inline form appears below checkbox with animation (slide down)
3. Form fields pre-populated from old component

**Inline Form Fields (2-column layout on desktop, stacked on mobile):**

**Row 1:**
- **Column 1 (col-md-6):** Component Name
  - Label: "Component name" (bold, required)
  - Input type: text
  - Bootstrap class: `.form-control`
  - Pre-filled: Old component's name
  - Editable: Yes
  - Validation: Required, max 100 characters
  - Error: "Component name is required"

- **Column 2 (col-md-6):** Component Type
  - Label: "Component type" (bold, required)
  - Input type: select (disabled)
  - Bootstrap class: `.form-select` with `disabled` attribute
  - Pre-filled: Old component's type (locked)
  - Editable: No
  - Visual: Greyed out to indicate locked state
  - Helper text: "Type must match component being replaced"

**Row 2:**
- **Column 1 (col-md-6):** Service Interval
  - Label: "Service interval (km)" (bold)
  - Input type: number
  - Bootstrap class: `.form-control`
  - Pre-filled: Old component's service_interval (can be empty)
  - Editable: Yes
  - Required: No
  - Min: 0

- **Column 2 (col-md-6):** Expected Lifetime
  - Label: "Expected lifetime (km)" (bold)
  - Input type: number
  - Bootstrap class: `.form-control`
  - Pre-filled: Old component's lifetime_expected (can be empty)
  - Editable: Yes
  - Required: No
  - Min: 0

**Row 3:**
- **Column 1 (col-md-6):** Cost
  - Label: "Cost (kr)" (bold)
  - Input type: number
  - Bootstrap class: `.form-control`
  - Pre-filled: Old component's cost (can be empty)
  - Editable: Yes
  - Required: No
  - Min: 0

- **Column 2 (col-md-6):** Notes
  - Label: "Notes" (bold)
  - Input type: textarea (1 row)
  - Bootstrap class: `.form-control`
  - Pre-filled: Old component's notes (can be empty)
  - Editable: Yes
  - Required: No

**HTML Structure:**
```html
<div id="create_new_form" style="display: none;">
    <div class="card mb-3">
        <div class="card-body">
            <h6 class="card-title mb-3">New component details</h6>
            <form class="row">
                <div class="col-md-6 mb-3">
                    <label for="new_component_name" class="form-label fw-bold">Component name <span class="text-danger">*</span></label>
                    <input type="text" class="form-control" id="new_component_name" name="new_component_name" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="new_component_type" class="form-label fw-bold">Component type <span class="text-danger">*</span></label>
                    <select class="form-select" id="new_component_type" name="new_component_type" disabled>
                        <option>Brake Pads</option>
                    </select>
                    <small class="form-text text-muted">Type must match component being replaced</small>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="new_service_interval" class="form-label fw-bold">Service interval (km)</label>
                    <input type="number" min="0" class="form-control" id="new_service_interval" name="new_service_interval">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="new_lifetime_expected" class="form-label fw-bold">Expected lifetime (km)</label>
                    <input type="number" min="0" class="form-control" id="new_lifetime_expected" name="new_lifetime_expected">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="new_cost" class="form-label fw-bold">Cost (kr)</label>
                    <input type="number" min="0" class="form-control" id="new_cost" name="new_cost">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="new_notes" class="form-label fw-bold">Notes</label>
                    <textarea class="form-control" id="new_notes" name="new_notes" rows="1"></textarea>
                </div>
            </form>
        </div>
    </div>
</div>
```

**Toggle Behavior:**
- Checking checkbox: Disable "Swap to" dropdown, clear its value, show form with slide-down animation
- Unchecking checkbox: Enable "Swap to" dropdown, hide form with slide-up animation, discard form data

**Validation:**
- Component name is required when checkbox is checked
- All other fields optional
- Type field is locked (no validation needed beyond pre-population)

**Responsive Behavior:**
- Desktop (≥768px): 2-column layout
- Mobile (<768px): Stacked fields (full width)
- Card container ensures visual grouping

---

### Section 5: Health Warnings (Conditional Visibility)

**Display Logic:**
- Only shown when user selects an existing component in "Swap to" dropdown
- Check selected component's health:
  - `lifetime_remaining <= 500` km → Show end-of-life warning
  - `service_next <= 100` km → Show service warning
  - Both conditions can be true (show both warnings)

**Warning Banner Structure:**

**End-of-Life Warning:**
```html
<div class="alert alert-warning mb-3" role="alert">
    <div class="d-flex align-items-start">
        <div class="me-2">⚠</div>
        <div>
            <strong>Low lifetime remaining:</strong> This component has only <strong>250 km</strong> remaining before end of life. Are you sure you want to install it?
        </div>
    </div>
</div>
```

**Service Warning:**
```html
<div class="alert alert-warning mb-3" role="alert">
    <div class="d-flex align-items-start">
        <div class="me-2">🔧</div>
        <div>
            <strong>Service needed soon:</strong> This component needs service in <strong>50 km</strong>. Consider servicing before installation.
        </div>
    </div>
</div>
```

**Multiple Warnings:**
- Stack vertically with spacing between
- Maintain consistent warning styling

**Behavior:**
- Non-blocking (user can proceed with swap despite warnings)
- Warnings disappear if user changes selection
- Warnings reappear if user re-selects same component

**Responsive Behavior:**
- Full width on all screen sizes
- Text wraps naturally on mobile

---

### Section 6: Swap Date (Always Visible)

**Field:** Date/time input with calendar picker
**Label:** "Swap date" (bold)
**Required:** Yes (asterisk in label)
**Bootstrap Component:** Input group with datepicker toggle

**Default Value:** Current date and time (YYYY-MM-DD HH:MM format)

**Structure:**
```html
<div class="mb-3">
    <label for="swap_date" class="form-label fw-bold">Swap date <span class="text-danger">*</span></label>
    <div class="input-group date-input-group">
        <input type="text" class="form-control datepicker-input" id="swap_date" name="swap_date" value="2025-10-11 14:30" required>
        <span class="input-group-text datepicker-toggle">🗓</span>
    </div>
    <small class="form-text text-muted">Both components will be updated with this date</small>
</div>
```

**JavaScript Behavior:**
- Use existing datepicker-input pattern from codebase (class: `.datepicker-input`)
- Date picker is automatically initialized by `initializeDatePickers()` function in main.js
- Calendar icon (🗓) toggles datepicker
- Format: YYYY-MM-DD HH:MM
- Clicking icon opens calendar overlay
- **IMPORTANT:** Call `validateDateInput(input)` function from main.js for validation

**Validation:**
- Required field
- Must be valid date format (validated by `validateDateInput()` function)
- Cannot be in the future
- Use existing date validation script from main.js:
  - Function: `validateDateInput(input)` (line 404 in main.js)
  - Automatically validates format, real dates, and ranges
  - Returns true/false and adds `.is-invalid` class on error
- If validation fails, show error in validation_modal
- Server-side validation also required

**Helper Text:**
"Both components will be updated with this date"

**Responsive Behavior:**
- Full width on all screen sizes
- Calendar picker adapts to screen size

---

## Modal Footer (Buttons)

**Layout:** Right-aligned buttons (Bootstrap `.modal-footer`)

**Buttons (left to right):**

1. **Cancel Button**
   - Text: "Cancel"
   - Bootstrap class: `.btn .btn-secondary`
   - Action: Close modal, discard changes
   - Behavior: If form has unsaved changes, show confirmation: "Discard changes?"

2. **Swap Components Button**
   - Text: "Swap components"
   - Bootstrap class: `.btn .btn-primary`
   - Action: Submit form, perform swap operation
   - Behavior:
     - Validate all fields
     - If validation fails, show inline errors and keep modal open
     - If validation passes, submit to backend API
     - Show loading spinner on button while processing
     - On success: Close modal, show success toast, refresh page/table
     - On error: Show error alert at top of modal, keep modal open

**Button States:**

**Swap Components button disabled when:**
- Form is being submitted (show spinner)
- Required fields are empty

**Button HTML:**
```html
<div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
    <button type="submit" class="btn btn-primary" id="submit_swap_btn">Swap components</button>
</div>
```

**Loading State:**
```html
<button type="submit" class="btn btn-primary" disabled>
    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
    Swapping...
</button>
```

**Responsive Behavior:**
- Desktop: Buttons stay on single row
- Mobile: Buttons may stack on very narrow screens (<350px)

---

## Access Point UI Specifications

### Access Point 1: Component Overview Page

**Location:** Action column in component table (rightmost column)

**Button Specification:**
- Button class: `.btn .btn-outline-primary .btn-sm .mb-1`
- Button text: **Icon ONLY** (♻) in table rows
- Icon: ♻ (recycling symbol) - referenced in table legend
- Data attribute: `data-component-id="[component_id]"`
- Only shown for components with `installation_status = "Installed"`

**Button HTML:**
```html
<button type="button" class="btn btn-outline-primary btn-sm mb-1 quick-swap-btn"
        data-component-id="abc-123"
        data-bs-toggle="modal"
        data-bs-target="#quickSwapModal"
        title="Quick swap">
    ♻
</button>
```

**Table Legend:**
- Add legend entry: "♻ = Quick swap"
- Place in table header or above table with other legend items

**Responsive Behavior:**
- All screen sizes: Show "♻" icon only
- Minimum button size: 44x44px (touch-friendly)
- Use `title` attribute for tooltip on hover

**JavaScript Behavior:**
- On click: Open quickSwapModal
- Pre-populate old component dropdown with clicked component
- Pre-populate bike context from component's bike_id
- Calculate default fate based on lifetime
- Reset "swap to" dropdown and "create new" checkbox

---

### Access Point 2: Bike Details Page

**Location:** Action area in component table (rightmost column or additional column)

**Button Specification:**
Same as Access Point 1:
- **Icon ONLY** (♻) in table rows
- Filtered to show only on components installed on this bike
- Button placement may differ based on bike details table layout
- Referenced in table legend

**Button HTML:** (Same as Access Point 1)

**JavaScript Behavior:**
- Same as Access Point 1, but:
- Old component dropdown filtered to show only components on this bike
- Bike context explicitly shows this bike's name

---

### Access Point 3: Component Details Page

**Location:** Action button row at top of page (alongside other action buttons)

**Button Specification:**
- Button class: `.btn .btn-outline-primary .me-2`
- Button text: **"♻ Quick swap"** (icon + text for buttons OUTSIDE tables)
- Data attribute: `data-component-id="[component_id]"`
- Disabled if `installation_status != "Installed"`

**Button HTML:**
```html
<button type="button" class="btn btn-outline-primary me-2 quick-swap-btn"
        data-bs-toggle="modal"
        data-bs-target="#quickSwapModal"
        {% if payload.bike_component_data['installation_status'] != "Installed" %}disabled{% endif %}>
    ♻ Quick swap
</button>
```

**Button Placement:** Insert after "Edit collection" button, before "Duplicate" button

**Responsive Behavior:**
- Desktop: Show full button with icon + text
- Mobile: May wrap to second row if space is constrained
- Touch-friendly (44x44px minimum)

**JavaScript Behavior:**
- On click: Open quickSwapModal
- Old component pre-selected and disabled (cannot change)
- Bike context shows component's current bike
- After successful swap: Refresh page OR redirect to component overview (TBD)

---

## Validation & Error Handling

### Client-Side Validation (Real-Time)

**Field: Component to swap out**
- Validate: Must select exactly one component
- When: On blur, on form submit
- Error display: Red border on TomSelect control
- Error message: Below field, red text: "Please select a component to swap out"

**Field: Component fate**
- Validate: Must select one radio button
- When: On form submit (always has default, no error state needed)
- **HTML field name must be:** `fate` (not `component_fate`) to match backend Form parameter

**Field: Swap to / Create new**
- Validate: Must either select existing component OR check "create new" and fill required fields
- When: On form submit
- Error display: Red border on TomSelect OR red borders on required fields in create form
- Error message: "Please select a component or create a new one"

**Field: Component name (create new)**
- Validate: Required when "create new" is checked, max 100 chars
- When: On blur, on form submit
- Error display: Red border on input, `.is-invalid` class
- Error message: Below field: "Component name is required"

**Field: Swap date**
- Validate: Required, valid date format, not in future
- When: On blur, on form submit
- Error display: Red border on input
- Error message: Below field: "Swap date cannot be in the future" or "Please enter a valid date"

### Server-Side Validation

**When backend validation fails:**
1. Quick swap modal closes
2. Loading modal closes automatically
3. Validation modal (`validation_modal`) opens showing the error message from backend
4. User dismisses validation modal by clicking "Close"
5. User corrects issues and resubmits

**Common Server Errors:**
- "Component not found" (old component deleted mid-operation)
- "Component is no longer installed" (status changed by another user)
- "Selected component is not available" (new component installed elsewhere)
- "Components must be of the same type" (data corruption or API bypass)
- "Swap date cannot be in the future" (client-side bypass)

### Validation Display Pattern

**Bootstrap Validation Classes:**
- Valid field: `.is-valid` (green border)
- Invalid field: `.is-invalid` (red border)
- Error text: `.invalid-feedback` (red text below field)

**Example:**
```html
<input type="text" class="form-control is-invalid" id="new_component_name">
<div class="invalid-feedback">
    Component name is required
</div>
```

### Success Feedback

**On successful swap (following Collections pattern EXACTLY):**
1. Quick swap modal closes
2. Loading modal (`modal_loading`) closes automatically
3. Report modal (`modal_report`) opens with success message:
   - Title: "✅ Swap complete"
   - Message: Backend success message (e.g., "Component swapped successfully: [Old Name] set to [Fate], [New Name] installed on [Bike Name]")
   - Green header styling
4. User dismisses report modal by clicking "Close"
5. Page content refreshes automatically (table updates to show new component states)

**IMPORTANT: NO toast notifications for this feature - use modal feedback ONLY**

---

## Responsive Design Specifications

### Desktop (≥992px)

**Modal:**
- Width: 800px (Bootstrap `.modal-lg`)
- Centered horizontally and vertically
- Padding: 1.5rem (Bootstrap default)

**Form Layout:**
- Old component dropdown: Full width
- Fate selection: Radio buttons inline (horizontal)
- Swap to dropdown: Full width
- Create new form: 2-column layout (col-md-6)
- Swap date: Half width or full width
- All fields have consistent spacing (mb-3)

**Buttons:**
- Quick swap buttons in tables: Icon only (♻)
- Quick swap buttons outside tables (component details page): Icon + text ("♻ Quick swap")
- Modal footer buttons: Side by side, right-aligned

### Tablet (768px - 991px)

**Modal:**
- Width: 700px (Bootstrap modal-lg adapts)
- Still centered

**Form Layout:**
- Same as desktop (2-column layout maintained)
- Old component dropdown: Full width
- Create new form: Still 2-column (col-md-6 applies)

**Buttons:**
- Quick swap buttons in tables: Icon only (♻)
- Quick swap buttons outside tables: Icon + text ("♻ Quick swap")
- Modal footer buttons: Side by side

### Mobile (< 768px)

**Modal:**
- Width: 95% of viewport width
- Margin: 0.5rem on sides
- Full screen on very narrow devices (<400px)

**Form Layout:**
- All fields stack vertically (full width)
- Create new form: Single column (col-md-6 becomes full width)
- Increased spacing between fields for touch targets
- TomSelect dropdowns have larger tap targets

**Buttons:**
- Quick swap buttons in tables: Icon only (♻)
- Quick swap buttons outside tables: Icon + text may wrap on very narrow screens
- Modal footer buttons: May stack on very narrow screens (<350px)
- Larger button height for touch (44px minimum)

**Touch Interactions:**
- All tap targets minimum 44x44px
- Increased padding around form controls
- TomSelect dropdown items have more spacing

### Breakpoint Summary

| Breakpoint | Modal Width | Form Columns | Table Button | Outside Table Button | Touch Targets |
|------------|-------------|--------------|--------------|----------------------|---------------|
| <576px (xs) | 95vw | 1 column | Icon only | Icon + text | 44px min |
| 576-767px (sm) | 540px | 1 column | Icon only | Icon + text | 44px min |
| 768-991px (md) | 700px | 2 columns | Icon only | Icon + text | 44px min |
| ≥992px (lg+) | 800px | 2 columns | Icon only | Icon + text | Standard |

---

## Accessibility Specifications

### ARIA Labels and Roles

**Modal:**
```html
<div class="modal fade" id="quickSwapModal" tabindex="-1"
     aria-labelledby="quickSwapModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="quickSwapModalLabel">Quick swap</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
            </div>
            <!-- ... -->
        </div>
    </div>
</div>
```

**Form Fields:**
- All labels associated with inputs via `for` attribute
- Required fields marked with `required` attribute AND visual asterisk
- Helper text associated via `aria-describedby`

**Example:**
```html
<label for="new_component_name" class="form-label fw-bold">
    Component name <span class="text-danger" aria-label="required">*</span>
</label>
<input type="text" class="form-control" id="new_component_name"
       aria-describedby="nameHelp" required>
<small id="nameHelp" class="form-text text-muted">Enter a unique name</small>
```

**TomSelect:**
- Maintain original select element's `id` and `name`
- Ensure TomSelect preserves `aria-label` if provided
- Screen readers can still navigate TomSelect via keyboard

**Alerts and Warnings:**
```html
<div class="alert alert-warning" role="alert" aria-live="polite">
    <strong>Low lifetime remaining:</strong> This component has only 250 km remaining...
</div>
```

### Keyboard Navigation

**Tab Order:**
1. Old component dropdown (TomSelect)
2. Fate radio button 1
3. Fate radio button 2
4. Swap to dropdown (TomSelect)
5. Create new checkbox
6. (If create new checked) New component form fields in order
7. Swap date input
8. Cancel button
9. Swap components button

**Keyboard Shortcuts:**
- `Tab` / `Shift+Tab`: Navigate between fields
- `Space`: Toggle checkboxes and radio buttons
- `Enter`: Submit form (when focus on submit button)
- `ESC`: Close modal (with confirmation if changes)
- `Arrow keys`: Navigate TomSelect options when dropdown open
- `Enter`: Select TomSelect option
- `Backspace`: Remove selected TomSelect item

**TomSelect Keyboard Support:**
- TomSelect has built-in keyboard navigation
- Users can type to search options
- Arrow keys navigate dropdown
- Enter selects option
- Backspace removes selection

**Focus Management:**
- When modal opens: Focus moves to first interactive element (old component dropdown)
- When modal closes: Focus returns to trigger button (quick swap button)
- After validation error: Focus moves to first invalid field

### Screen Reader Support

**Announcements:**
- Modal opening: "Quick swap dialog opened"
- Field errors: Error messages announced when field loses focus
- Warnings: Health warnings announced via `aria-live="polite"`
- Success: "Component swapped successfully" announced

**Labels and Descriptions:**
- All form fields have visible labels (not placeholder-only)
- Helper text provides additional context via `aria-describedby`
- Required fields clearly marked for screen readers

**State Changes:**
- When "Create new" checkbox is toggled, announce: "Create new component form visible/hidden"
- When component selected with warning, announce: "Warning: This component has low lifetime remaining"

### Color Contrast

**WCAG 2.1 AA Compliance:**
- All text meets 4.5:1 contrast ratio (7:1 for large text)
- Warning colors (yellow/orange) have sufficient contrast
- Error colors (red) have sufficient contrast
- Disabled fields clearly visually distinct

**Non-Color Indicators:**
- Don't rely on color alone for validation states
- Use icons (✓ ✗) in addition to color
- Use text labels for radio buttons, not just visual treatment

---

## TomSelect Implementation Details

### Installation & Assets

**Required Files:**
- TomSelect CSS: `tom-select.bootstrap5.min.css` (likely already in project)
- TomSelect JS: `tom-select.complete.min.js` (likely already in project)

**Include in Template:**
```html
<link href="{{ url_for('static', path='css/tom-select.bootstrap5.min.css') }}" rel="stylesheet">
<script src="{{ url_for('static', path='js/tom-select.complete.min.js') }}"></script>
```

### Initialization Pattern (from Collections Feature)

**Old Component Dropdown:**
```javascript
// Get select element
const oldComponentSelect = document.getElementById('old_component_id');

// Destroy existing TomSelect if present (for modal reuse)
if (oldComponentSelect.tomSelect || oldComponentSelect.tomselect) {
    const ts = oldComponentSelect.tomSelect || oldComponentSelect.tomselect;
    ts.destroy();
}

// Initialize TomSelect
const oldComponentTS = new TomSelect(oldComponentSelect, {
    plugins: ['remove_button'],
    maxItems: 1,  // Only one component can be swapped out
    valueField: 'value',
    labelField: 'text',
    searchField: ['text'],
    placeholder: 'Select component to swap out...',
    render: {
        option: function(data, escape) {
            return '<div>' + escape(data.text) + '</div>';
        },
        item: function(data, escape) {
            return '<div>' + escape(data.text) + '</div>';
        }
    }
});

// Store instance on element for later access
oldComponentSelect.tomSelect = oldComponentTS;

// Add change event listener
oldComponentTS.on('change', function(value) {
    // Update bike context
    // Calculate default fate
    // Filter "swap to" dropdown based on selected component's type
});
```

**New Component Dropdown (Swap To):**
```javascript
// Similar initialization, but filtered by component type
const newComponentSelect = document.getElementById('new_component_id');

// Destroy existing
if (newComponentSelect.tomSelect || newComponentSelect.tomselect) {
    const ts = newComponentSelect.tomSelect || newComponentSelect.tomselect;
    ts.destroy();
}

// Initialize
const newComponentTS = new TomSelect(newComponentSelect, {
    plugins: ['remove_button'],
    maxItems: 1,
    valueField: 'value',
    labelField: 'text',
    searchField: ['text'],
    placeholder: 'Select component...'
});

newComponentSelect.tomSelect = newComponentTS;

// Add change event to check for health warnings
newComponentTS.on('change', function(value) {
    checkComponentHealth(value);
    showWarningsIfNeeded();
});
```

### Dynamic Option Filtering

**When old component is selected, update new component options:**
```javascript
function updateNewComponentOptions(oldComponentType) {
    const newComponentSelect = document.getElementById('new_component_id');
    const tomSelect = newComponentSelect.tomSelect || newComponentSelect.tomselect;

    if (!tomSelect) return;

    // Clear existing options
    tomSelect.clearOptions();

    // Filter components: matching type, not installed, not retired
    const filteredComponents = allComponents.filter(c =>
        c.type === oldComponentType &&
        c.status === 'Not installed'
    );

    // Add filtered options
    filteredComponents.forEach(component => {
        tomSelect.addOption({
            value: component.id,
            text: `${component.name} (${component.distance} km)`
        });
    });

    // Refresh dropdown
    tomSelect.refreshOptions(false);
}
```

### Enabling/Disabling Based on Checkbox

**When "Create new component" checkbox changes:**
```javascript
const createNewCheckbox = document.getElementById('create_new_component');
const newComponentSelect = document.getElementById('new_component_id');
const createNewForm = document.getElementById('create_new_form');

createNewCheckbox.addEventListener('change', function() {
    const tomSelect = newComponentSelect.tomSelect || newComponentSelect.tomselect;

    if (this.checked) {
        // Disable and clear "swap to" dropdown
        if (tomSelect) {
            tomSelect.clear();
            tomSelect.disable();
        }

        // Show create new form
        createNewForm.style.display = 'block';

        // Populate fields from old component
        populateCreateNewForm();

    } else {
        // Enable "swap to" dropdown
        if (tomSelect) {
            tomSelect.enable();
        }

        // Hide create new form
        createNewForm.style.display = 'none';
    }
});
```

### Cleanup on Modal Close

**Important:** Prevent memory leaks by properly destroying TomSelect instances
```javascript
const quickSwapModal = document.getElementById('quickSwapModal');

quickSwapModal.addEventListener('hidden.bs.modal', function() {
    // Clean up TomSelect instances
    const oldComponentSelect = document.getElementById('old_component_id');
    const newComponentSelect = document.getElementById('new_component_id');

    [oldComponentSelect, newComponentSelect].forEach(select => {
        if (select && (select.tomSelect || select.tomselect)) {
            const ts = select.tomSelect || select.tomselect;
            ts.destroy();
            select.tomSelect = null;
            select.tomselect = null;
        }
    });

    // Reset form
    document.getElementById('quick_swap_form').reset();
    createNewForm.style.display = 'none';
});
```

---

## Component Health Warning Logic

### Warning Conditions

**End-of-Life Warning:**
```javascript
function checkEndOfLifeWarning(componentId) {
    const component = getComponentById(componentId);

    if (!component || !component.lifetime_expected) {
        return null;
    }

    const lifetimeRemaining = component.lifetime_expected - component.distance;

    if (lifetimeRemaining <= 500) {
        return {
            type: 'lifetime',
            message: `This component has only ${lifetimeRemaining} km remaining before end of life. Are you sure you want to install it?`,
            severity: lifetimeRemaining <= 0 ? 'danger' : 'warning'
        };
    }

    return null;
}
```

**Service Warning:**
```javascript
function checkServiceWarning(componentId) {
    const component = getComponentById(componentId);

    if (!component || !component.service_interval) {
        return null;
    }

    const serviceNext = calculateServiceNext(component);

    if (serviceNext <= 100) {
        return {
            type: 'service',
            message: `This component needs service in ${serviceNext} km. Consider servicing before installation.`,
            severity: serviceNext <= 0 ? 'danger' : 'warning'
        };
    }

    return null;
}
```

**Display Warnings:**
```javascript
function showComponentWarnings(componentId) {
    const warningContainer = document.getElementById('component_health_warnings');
    warningContainer.innerHTML = ''; // Clear existing warnings

    const lifetimeWarning = checkEndOfLifeWarning(componentId);
    const serviceWarning = checkServiceWarning(componentId);

    if (lifetimeWarning) {
        warningContainer.innerHTML += createWarningHTML(lifetimeWarning);
    }

    if (serviceWarning) {
        warningContainer.innerHTML += createWarningHTML(serviceWarning);
    }

    // Show or hide warning container
    warningContainer.style.display = (lifetimeWarning || serviceWarning) ? 'block' : 'none';
}

function createWarningHTML(warning) {
    const icon = warning.type === 'lifetime' ? '⚠' : '🔧';
    const alertClass = warning.severity === 'danger' ? 'alert-danger' : 'alert-warning';

    return `
        <div class="alert ${alertClass} mb-3" role="alert">
            <div class="d-flex align-items-start">
                <div class="me-2">${icon}</div>
                <div>${warning.message}</div>
            </div>
        </div>
    `;
}
```

---

## JavaScript Event Flow

### Modal Opening Sequence

1. User clicks "Quick swap" button on any of the 3 pages
2. JavaScript captures `data-component-id` from button
3. Modal opens (`show.bs.modal` event)
4. Initialize modal:
   - Fetch component data (or use pre-loaded data)
   - Populate bike context banner
   - Initialize TomSelect for old component dropdown
   - Set old component value (pre-select from context)
   - Calculate and set default fate (Retired or Not installed)
   - Initialize TomSelect for new component dropdown
   - Filter new component options by type
   - Set swap date to current date/time
   - Hide create new form
   - Clear any warnings
5. Modal fully visible (`shown.bs.modal` event)
6. Focus moves to first interactive element

### Form Interaction Sequence

**User selects old component (if not pre-selected):**
1. TomSelect `change` event fires
2. Update bike context banner
3. Calculate default fate based on component's lifetime
4. Update fate radio buttons
5. Filter "swap to" dropdown options (matching type only)
6. Clear any existing warnings

**User selects new component from dropdown:**
1. TomSelect `change` event fires
2. Check component health (lifetime, service)
3. Display warnings if needed
4. Enable submit button if all required fields valid

**User checks "Create new component":**
1. Checkbox `change` event fires
2. Disable and clear "swap to" dropdown
3. Show create new form with slide-down animation
4. Populate form fields from old component
5. Lock component type field
6. Focus moves to component name field
7. Enable submit button if all required fields valid

**User unchecks "Create new component":**
1. Checkbox `change` event fires
2. Enable "swap to" dropdown
3. Hide create new form with slide-up animation
4. Discard form data (don't save)
5. Submit button state depends on "swap to" selection

### Form Submission Sequence

**User clicks "Swap components":**
1. Validate all required fields (client-side)
2. If validation fails:
   - Show inline error messages
   - Add `.is-invalid` classes
   - Focus first invalid field
   - Stop submission
3. If validation passes:
   - Disable submit button
   - Show loading spinner
   - Collect form data
   - Build request payload
   - Submit AJAX request to backend API
4. If backend returns error:
   - Re-enable submit button
   - Remove loading spinner
   - Show error alert at top of modal
   - Keep modal open
   - User can retry
5. If backend returns success:
   - Close modal
   - Show success toast
   - Refresh page content (table data)
   - Clean up TomSelect instances

### Modal Closing Sequence

1. User clicks "Cancel" or "X" or presses ESC
2. If form has unsaved changes:
   - Show confirmation: "Discard changes?"
   - If user confirms: proceed to close
   - If user cancels: keep modal open
3. Modal begins closing (`hide.bs.modal` event)
4. Clean up:
   - Destroy TomSelect instances
   - Reset form fields
   - Clear warnings
   - Remove error alerts
5. Modal fully closed (`hidden.bs.modal` event)
6. Focus returns to trigger button

---

## Data Requirements (Backend API)

### API Endpoint

**Endpoint:** `POST /quick_swap` (per architect's handover - simplified naming)

**Request Payload (Form data, not JSON):**
```
old_component_id=abc-123
fate=Retired
swap_date=2025-10-11 14:30
new_component_id=def-456              // Present if swapping to existing

OR (if creating new):

old_component_id=abc-123
fate=Retired
swap_date=2025-10-11 14:30
create_new=true
new_component_name=Shimano Ultegra Brake Pads
new_component_type=Brake Pads
new_service_interval=2000
new_lifetime_expected=2500
new_cost=450
new_notes=Front brake pads
```

**Note:** Backend expects Form data (application/x-www-form-urlencoded), NOT JSON. Refer to architect's handover line 124-141 for exact parameter names and structure.

**IMPORTANT - Parameter Name Mapping:**
Frontend form field names MUST match backend Form parameter names exactly:
- HTML field: `name="old_component_id"` → Backend: `old_component_id: str = Form(...)`
- HTML field: `name="fate"` → Backend: `fate: str = Form(...)`
- HTML field: `name="swap_date"` → Backend: `swap_date: str = Form(...)`
- HTML field: `name="new_component_id"` → Backend: `new_component_id: Optional[str] = Form(None)`
- HTML field: `name="create_new"` → Backend: `create_new: Optional[str] = Form(None)` (value="true" when checked)
- HTML field: `name="new_component_name"` → Backend: `new_component_name: Optional[str] = Form(None)`
- HTML field: `name="new_component_type"` → Backend: `new_component_type: Optional[str] = Form(None)`
- HTML field: `name="new_service_interval"` → Backend: `new_service_interval: Optional[str] = Form(None)`
- HTML field: `name="new_lifetime_expected"` → Backend: `new_lifetime_expected: Optional[str] = Form(None)`
- HTML field: `name="new_cost"` → Backend: `new_cost: Optional[str] = Form(None)`
- HTML field: `name="new_notes"` → Backend: `new_notes: Optional[str] = Form(None)`

**Response (Success):**
```json
{
  "success": true,
  "message": "Component swapped successfully: Old component [Old Name] set to [Fate], new component [New Name] installed on [Bike Name]"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Component is no longer installed. Please refresh and try again."
}
```

**Note:** Response format matches architecture specification (lines 172-186 in architect handover). Both success and error responses use the same structure: `success` (boolean) and `message` (string).

### Data Needed for Modal Initialization

**When modal opens, frontend needs:**

1. **Old component data** (from context or API):
   - component_id
   - component_name
   - component_type
   - component_distance
   - lifetime_expected
   - service_interval
   - bike_id
   - bike_name
   - installation_status

2. **Available components for "swap to" dropdown** (filtered by backend or frontend):
   - List of components where:
     - `installation_status = "Not installed"`
     - `component_type` matches old component (if filtered on backend)
   - For each component:
     - component_id
     - component_name
     - component_distance
     - lifetime_remaining (calculated)
     - service_next (calculated)
     - component_type

3. **Bike context:**
   - bike_id
   - bike_name

**Suggested Approach:**
- Pre-load all necessary data when rendering the page (embed in JavaScript)
- OR: Make AJAX call when modal opens to fetch data
- Recommendation: Pre-load for better performance (avoid API delay on modal open)

---

## Wireframes

### Desktop View - Modal (Initial State)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Quick swap                                                                [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ℹ 🚴 Swapping component on: Road Bike                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component to swap out *                                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Shimano 105 Brake Pads (Brake Pads) - Road Bike              [×] ▼│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component fate *                                                           │
│  ○ Not installed     ● Retired                                             │
│  ℹ Defaulted to "Retired" because component has reached expected lifetime  │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap to existing component                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Select component...                                             ▼│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  OR                                                                         │
│                                                                             │
│  ☐ Create new component (copy settings from current)                       │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap date *                                                                │
│  ┌─────────────────────────────────────┬─────┐                             │
│  │ 2025-10-11 14:30                    │ 🗓 │                             │
│  └─────────────────────────────────────┴─────┘                             │
│  Both components will be updated with this date                             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                          [ Cancel ]  [ Swap components ]    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Desktop View - With Component Selected and Warning

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Quick swap                                                                [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ℹ 🚴 Swapping component on: Road Bike                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component to swap out *                                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Shimano 105 Brake Pads (Brake Pads) - Road Bike              [×] ▼│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component fate *                                                           │
│  ○ Not installed     ● Retired                                             │
│  ℹ Defaulted to "Retired" because component has reached expected lifetime  │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap to existing component                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Shimano Ultegra Brake Pads (250 km)                          [×] ▼│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ⚠ Low lifetime remaining: This component has only 250 km remaining   │  │
│  │   before end of life. Are you sure you want to install it?            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  OR                                                                         │
│                                                                             │
│  ☐ Create new component (copy settings from current)                       │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap date *                                                                │
│  ┌─────────────────────────────────────┬─────┐                             │
│  │ 2025-10-11 14:30                    │ 🗓 │                             │
│  └─────────────────────────────────────┴─────┘                             │
│  Both components will be updated with this date                             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                          [ Cancel ]  [ Swap components ]    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Desktop View - Create New Component Form Expanded

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Quick swap                                                                [X]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ℹ 🚴 Swapping component on: Road Bike                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component to swap out *                                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Shimano 105 Brake Pads (Brake Pads) - Road Bike              [×] ▼│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Component fate *                                                           │
│  ○ Not installed     ● Retired                                             │
│  ℹ Defaulted to "Retired" because component has reached expected lifetime  │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap to existing component                                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Select component...                                             ▼│  │ (disabled)
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  OR                                                                         │
│                                                                             │
│  ☑ Create new component (copy settings from current)                       │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ New component details                                                 │  │
│  │                                                                       │  │
│  │  Component name *                    Component type *                │  │
│  │  ┌────────────────────────────┐      ┌────────────────────────────┐  │  │
│  │  │ Shimano 105 Brake Pads     │      │ Brake Pads             ▼│  │  │ (disabled)
│  │  └────────────────────────────┘      └────────────────────────────┘  │  │
│  │                                       Type must match component      │  │
│  │                                       being replaced                  │  │
│  │  Service interval (km)               Expected lifetime (km)          │  │
│  │  ┌────────────────────────────┐      ┌────────────────────────────┐  │  │
│  │  │ 2000                       │      │ 2500                       │  │  │
│  │  └────────────────────────────┘      └────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  Cost (kr)                           Notes                           │  │
│  │  ┌────────────────────────────┐      ┌────────────────────────────┐  │  │
│  │  │ 450                        │      │ Front brake pads           │  │  │
│  │  └────────────────────────────┘      └────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Swap date *                                                                │
│  ┌─────────────────────────────────────┬─────┐                             │
│  │ 2025-10-11 14:30                    │ 🗓 │                             │
│  └─────────────────────────────────────┴─────┘                             │
│  Both components will be updated with this date                             │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                          [ Cancel ]  [ Swap components ]    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Mobile View (< 768px)

```
┌─────────────────────────────────────┐
│ Quick swap                        [X]│
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ℹ Swapping component on:        │ │
│ │   Road Bike                     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Component to swap out *             │
│ ┌─────────────────────────────────┐ │
│ │ 🔍 Shimano 105 Brake...    [×]▼│ │
│ └─────────────────────────────────┘ │
│                                     │
│ Component fate *                    │
│ ○ Not installed                     │
│ ● Retired                           │
│ ℹ Defaulted to "Retired"           │
│                                     │
│ ───────────────────────────────────  │
│                                     │
│ Swap to existing component          │
│ ┌─────────────────────────────────┐ │
│ │ 🔍 Select component...       ▼│ │
│ └─────────────────────────────────┘ │
│                                     │
│ OR                                  │
│                                     │
│ ☐ Create new component              │
│                                     │
│ ───────────────────────────────────  │
│                                     │
│ Swap date *                         │
│ ┌──────────────────────┬──────┐    │
│ │ 2025-10-11 14:30     │ 🗓  │    │
│ └──────────────────────┴──────┘    │
│                                     │
├─────────────────────────────────────┤
│            [ Cancel ]               │
│        [ Swap components ]          │
└─────────────────────────────────────┘
```

### Component Overview Page - Quick Swap Button Placement

```
Component Overview Table (Desktop):

┌────────────────┬────────┬──────────┬────────┬────────────┬──────────┐
│ Component      │ Type   │ Distance │ Status │ Lifetime   │ Actions  │
├────────────────┼────────┼──────────┼────────┼────────────┼──────────┤
│ Chain A        │ Chain  │ 1500 km  │ ⚡ Ins │ 🟢         │ [♻]     │
│ Brake Pads     │ Brakes │ 2500 km  │ ⚡ Ins │ 🟡         │ [♻]     │
│ Front Tire     │ Tire   │ 4500 km  │ ⚡ Ins │ 🔴         │ [♻]     │
│ Saddle         │ Saddle │ 500 km   │ 💤 Not│ -          │ [🗑]     │
└────────────────┴────────┴──────────┴────────┴────────────┴──────────┘

Legend: ♻ = Quick swap | 🗑 = Delete

Note: Quick swap button (♻) only shows for installed components
Note: Button is icon-only in table, referenced in legend
```

### Component Details Page - Quick Swap Button Placement

```
Action Button Row (Desktop):

[🚴 View bike] [📦 Edit collection] [♻ Quick swap] [⛓ Duplicate]
[🧑‍🔧 New service] [📝 New workplan] [🚨 New incident]

Note: Quick swap button has text ("♻ Quick swap") when OUTSIDE tables
Note: Button inserted after "Edit collection", before "Duplicate"
```

---

## Decisions Made

### 1. Modal Size: Large (modal-lg)
**Rationale:** The form requires significant space for TomSelect dropdowns, the "create new" form (2-column layout), and warning banners. Large modal provides comfortable spacing without scrolling on desktop. Collections feature uses same size successfully.

### 2. TomSelect for All Component Dropdowns
**Rationale:**
- Requirement explicitly specifies TomSelect
- Provides search functionality for large component lists
- Consistent with Collections, Incidents, and Workplans features
- Supports keyboard navigation and accessibility

### 3. Progressive Disclosure for "Create New" Form
**Rationale:**
- Reduces cognitive load by showing only relevant fields
- Clear visual separation between "select existing" and "create new" paths
- Prevents user confusion about which option is active
- Follows principle of progressive disclosure in UX design

### 4. Non-Blocking Warnings
**Rationale:**
- Users may have valid reasons to install components with low lifetime (e.g., temporary fix)
- Warning provides guidance without restricting user choice
- Consistent with requirements: "Warning does NOT block the swap"
- Uses Bootstrap alert component for clear visual treatment

### 5. Smart Default for Fate Selection
**Rationale:**
- Reduces manual decision-making for common scenario (worn components)
- Prevents accidental re-use of end-of-life components
- Follows requirement: "Default selection logic based on lifetime"
- User can always override if needed

### 6. Locked Component Type in Create New Form
**Rationale:**
- Enforces requirement: "Component type matching is strictly enforced"
- Visual disabled state communicates constraint clearly
- Prevents user error and simplifies validation
- Helper text explains why field is locked

### 7. Single Date for Both Operations
**Rationale:**
- Requirement specifies: "Both operations use the SAME date/time"
- Simplifies UX (one date picker instead of two)
- Represents the atomic nature of the swap operation
- Default to "now" covers 90% of use cases

### 8. Sentence Case for "Quick swap" UI Text
**Rationale:**
- Requirement explicitly states: "Use 'Quick swap' (not 'Quick Swap')"
- Consistent with app's existing UI patterns (checked other features)
- Follows sentence case convention for UI elements

### 9. Icon Selection: ♻ (Recycling Symbol)
**Rationale:**
- Represents the concept of "swapping" or "replacing"
- Visually distinct from other action icons
- Universal symbol, no localization concerns
- Fits within existing icon style (emoji-based)

### 10. Mobile-First Responsive Design
**Rationale:**
- Requirement specifies mobile-first approach
- Modern web best practice
- Ensures touch-friendly interactions (44px tap targets)
- Stacked layout on mobile prevents horizontal scrolling

---

## Next Steps for Fullstack Developer

### 1. Review Architecture Handover
- Check `.handovers/architecture/` for architect's API design
- Understand backend endpoint structure for `POST /api/swap_component`
- Note any technical constraints or data structure requirements
- Coordinate if there are differences between UX and architecture specs

### 2. Create Modal HTML Template
- Create new file: `frontend/templates/modal_quick_swap.html`
- Implement Bootstrap modal structure per specification above
- Include all form fields with proper classes and attributes
- Add ARIA labels and accessibility attributes
- Ensure responsive classes are applied (col-md-6, etc.)

### 3. Include Modal in Templates
- Add `{% include "modal_quick_swap.html" %}` to:
  - `frontend/templates/component_overview.html`
  - `frontend/templates/bike_details.html`
  - `frontend/templates/component_details.html`
- Consider using Jinja2 context to pass necessary data

### 4. Add Quick Swap Buttons to Tables
- **Component Overview:** Add button column in component table
- **Bike Details:** Add button column in bike's component table
- **Component Details:** Add button to action button row
- Apply responsive classes for icon-only on mobile
- Set proper `data-component-id` attributes

### 5. Implement JavaScript (in main.js)
Follow Collections feature pattern:

**a. Modal Initialization:**
- Initialize TomSelect for both dropdowns on modal open
- Populate old component dropdown from page context
- Filter new component dropdown by type
- Set default fate based on lifetime
- Update bike context banner

**b. Form Interactions:**
- Handle old component selection change
- Handle new component selection change (check health warnings)
- Handle "create new" checkbox toggle
- Handle fate radio button change
- Validate form on submit

**c. Warning Display:**
- Implement `checkEndOfLifeWarning()` function
- Implement `checkServiceWarning()` function
- Show/hide warning banners dynamically

**d. Form Submission (FOLLOW COLLECTIONS PATTERN EXACTLY):**
- Validate all required fields using `validateDateInput()` for dates
- If validation fails: Show `validation_modal` with error message, stop submission
- Build FormData payload (handle both "existing" and "create new" paths)

**FormData Construction Example:**
```javascript
const formData = new FormData();
formData.append('old_component_id', oldComponentId);
formData.append('fate', selectedFate);  // "Not installed" or "Retired"
formData.append('swap_date', swapDate);  // "YYYY-MM-DD HH:MM"

if (createNewChecked) {
    // Creating new component
    formData.append('create_new', 'true');
    formData.append('new_component_name', document.getElementById('new_component_name').value);
    formData.append('new_component_type', document.getElementById('new_component_type').value);
    formData.append('new_service_interval', document.getElementById('new_service_interval').value || '');
    formData.append('new_lifetime_expected', document.getElementById('new_lifetime_expected').value || '');
    formData.append('new_cost', document.getElementById('new_cost').value || '');
    formData.append('new_notes', document.getElementById('new_notes').value || '');
} else {
    // Swapping to existing component
    formData.append('new_component_id', newComponentId);
}
```

- Close quick swap modal
- Show `modal_loading` with message "Swapping components..."
- Submit AJAX POST to `/quick_swap` using FormData (not JSON)
- When response received:
  - Close `modal_loading` using `forceCloseLoadingModal()`
  - After 500ms delay, show `modal_report` with success/error message using `showReportModal()`
  - When user dismisses report modal, refresh page using `window.location.reload()`
- **IMPORTANT:** NO toast notifications - ALL feedback via modals only
- Reference: Collections pattern in main.js lines 1966-2046

**e. Cleanup:**
- Destroy TomSelect instances on modal close (`hidden.bs.modal` event)
- Reset form state
- Clear warnings
- Prevent memory leaks
- Reference: Existing TomSelect cleanup patterns in main.js

### 6. Backend API Endpoint
(Coordinate with @architect - see architecture handover)

- Implement `POST /quick_swap` endpoint (per architect's specification)
- Validate request payload
- Perform atomic transaction:
  - Update old component (change status, update date)
  - Create/update new component (install, set bike_id)
  - Create two history records
- Return success/error response
- Handle edge cases (concurrency, validation failures)

### 7. Data Layer
(Coordinate with @database-expert if schema changes needed)

- No schema changes required (use existing tables)
- Ensure proper transaction handling
- Create history records correctly
- Update component statuses atomically

### 8. Testing
- Test all 3 access points (overview, bike details, component details)
- Test both paths (select existing, create new)
- Test validation (client and server-side)
- Test warnings display
- Test edge cases:
  - No available components to swap to
  - Component status changes mid-operation
  - Concurrent swaps to same component
- Test responsive behavior (desktop, tablet, mobile)
- Test keyboard navigation
- Test screen reader compatibility

### 9. Error Handling
- Implement all validation rules per specification
- Display inline errors for form fields
- Display alert for server errors
- Handle network failures gracefully

### 10. Documentation
- Update user documentation if needed
- Add comments to JavaScript code
- Document API endpoint (if not already done by @architect)

---

## Dependencies & Requirements

### Frontend Dependencies (Likely Already Present)
- Bootstrap 5 (CSS and JS)
- TomSelect CSS: `tom-select.bootstrap5.min.css`
- TomSelect JS: `tom-select.complete.min.js`
- jQuery or vanilla JS for AJAX (use existing pattern)
- Datepicker library (existing in project)

### Backend Dependencies
- FastAPI (existing)
- Peewee ORM (existing)
- Database transaction support (existing)

### Data Requirements
- Component data (all fields from database)
- Bike data (bike_id, bike_name)
- Component type matching logic
- Health calculation logic (lifetime_remaining, service_next)

### Coordination Requirements
- **With @architect:**
  - Confirm API endpoint path and request/response schema
  - Confirm transaction approach
  - Resolve any UX/architecture conflicts
- **With @database-expert:**
  - Confirm no schema changes needed (feature uses existing tables)
  - Confirm history record structure
  - Confirm transaction isolation level

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript required (feature cannot work without JS)
- No IE11 support needed (assumption - verify with stakeholders)

---

## Questions / Blockers

### Resolved (Design Decisions Made)
- ✓ Modal size: Large (modal-lg)
- ✓ Component type enforcement: Locked field in create new form
- ✓ Warning display: Non-blocking alerts
- ✓ Default fate: Based on lifetime logic
- ✓ Button icon: ♻ (recycling symbol)
- ✓ Button text: "Quick swap" (sentence case)

### Resolved Questions (Based on Architecture Handover and Stakeholder Feedback)
- ✓ **API endpoint path:** `/quick_swap` (confirmed by architect)
- ✓ **Request format:** Form data with specific parameters (see architect handover lines 124-141)
- ✓ **Response format:** JSON with `success` and `message` fields (see architect handover lines 167-183)
- ✓ **Post-swap behavior:** Refresh current page (no redirect)
- ✓ **Success feedback:** Modal only (NO toast) - follow Collections pattern EXACTLY
- ✓ **Validation feedback:** Use `validation_modal` for all validation errors
- ✓ **Loading feedback:** Use `modal_loading` during operation
- ✓ **Result feedback:** Use `modal_report` (showReportModal) for final result

### Open Questions for @fullstack-developer
- [ ] **Data pre-loading:** Should we:
  - Embed all component data in page JS on initial load?
  - Make AJAX call when modal opens?
  - **Recommendation:** Pre-load for better performance

### Potential Blockers
- **TomSelect version compatibility:** Ensure TomSelect version supports all specified features
- **Datepicker conflicts:** If modal opens within another modal, datepicker may have z-index issues
- **Mobile testing:** Need access to physical mobile devices or reliable emulators

---

## Architecture Interactions

### Architecture Constraints Noted
- **Architecture handover reviewed:** `.handovers/architecture/component-quick-swap-architect-handover.md`
- **Endpoint:** `POST /quick_swap` (simplified naming, not `/api/quick_swap`)
- **Request format:** Form data (application/x-www-form-urlencoded), NOT JSON
- **Response format:** JSON with `success` and `message` fields
- **Modal feedback pattern:** MUST follow Collections feature EXACTLY - NO toast notifications
- **Validation errors:** Show in `validation_modal`
- **Loading state:** Show `modal_loading`
- **Results:** Show in `modal_report` using `showReportModal()` function

### UX Requirements That May Affect Architecture
1. **TomSelect Dynamic Filtering:**
   - Frontend needs to filter "swap to" dropdown by component type
   - Can be done client-side (if all components loaded) or server-side (API endpoint filters)
   - **Recommendation:** Client-side filtering for performance (avoid extra API call)

2. **Atomic Transaction Required:**
   - Swap operation must be all-or-nothing
   - Both history records must be created together
   - Architect must ensure transaction isolation

3. **Health Check Calculations:**
   - Frontend needs `lifetime_remaining` and `service_next` for each component
   - Can be calculated client-side or provided by backend
   - **Recommendation:** Backend calculates and provides in initial page load

4. **Data Validation:**
   - Component type matching must be enforced on backend (security)
   - Frontend validation is UX enhancement, not security
   - Backend must re-validate all constraints

5. **Concurrency Handling:**
   - If two users swap to same component simultaneously, one must fail
   - Backend must handle with proper locking or transaction isolation

### Cross-Feature Dependencies
- **Collections Feature:** Similar TomSelect patterns, reference for consistency
- **Component Status Update:** Quick swap creates history records like status changes
- **Component Creation:** "Create new" path reuses component creation logic

---

## References

### Requirements Document
- `.handovers/requirements/component-quick-swap-requirements.md`

### Existing UI Patterns (Primary References)
- **Collections Feature:** `frontend/templates/modal_collection.html`
  - TomSelect usage pattern
  - Modal structure and layout
  - Warning banner design
  - Form validation display
- **Create Component Modal:** `frontend/templates/modal_create_component.html`
  - Form field layout
  - Datepicker pattern
  - Field validation
- **Component Overview:** `frontend/templates/component_overview.html`
  - Table structure
  - Button placement in action column
  - Filter patterns
- **Bike Details:** `frontend/templates/bike_details.html`
  - Component table on bike page
  - Button placement
- **Component Details:** `frontend/templates/component_details.html`
  - Action button row
  - Button styling and placement

### JavaScript Patterns
- **TomSelect Implementation:** `frontend/static/js/main.js`
  - Lines 1130-1170: TomSelect initialization for Collections
  - Lines 3413-3466: TomSelect initialization for Incidents
  - Lines 4172-4225: TomSelect initialization for Workplans
  - Consistent pattern for destroy, initialize, populate

### Bootstrap Documentation
- Modal: https://getbootstrap.com/docs/5.3/components/modal/
- Forms: https://getbootstrap.com/docs/5.3/forms/overview/
- Alerts: https://getbootstrap.com/docs/5.3/components/alerts/
- Grid: https://getbootstrap.com/docs/5.3/layout/grid/

### TomSelect Documentation
- https://tom-select.js.org/
- Plugins: https://tom-select.js.org/plugins/
- Examples: https://tom-select.js.org/examples/

### Accessibility Guidelines
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

---

## Additional Notes

### Design Consistency Checklist
- ✓ Modal structure follows Collections pattern
- ✓ TomSelect configuration matches existing usage
- ✓ Button styles consistent with app (btn-outline-primary)
- ✓ Form field layout consistent with create component modal
- ✓ Warning banners use Bootstrap alert components
- ✓ Datepicker pattern matches existing modals
- ✓ Emoji icons consistent with app style
- ✓ Responsive classes consistent with other templates

### Performance Considerations
- TomSelect can handle large lists (1000+ components) efficiently
- Pre-loading component data recommended for fast modal opening
- Debounce search input in TomSelect (built-in feature)
- Lazy-load modal content if data size is very large

### Future Enhancements (Out of Scope for MVP)
- Bulk swap operations (multiple components at once)
- Swap preview (side-by-side comparison of old vs new)
- Undo swap operation
- Cross-bike component transfer
- Swap history/analytics
- Component health score visualization

### Testing Recommendations
- Test on actual mobile devices (not just browser emulation)
- Test with slow network (simulate API delays)
- Test with screen reader (NVDA or JAWS)
- Test keyboard-only navigation
- Test edge cases listed in requirements

---

**Handover Status:** Complete - Ready for @fullstack-developer

**Next Agent:** @fullstack-developer

**Action Required:** Implement complete quick swap feature (frontend + backend) following this UX specification and architect's technical design.

**Estimated Implementation Time:** 8-12 hours (assuming no major blockers)
