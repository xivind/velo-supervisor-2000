# UX Designer Handover (v2.1 - Quick Swap Addition)

**Feature:** Component Status Refinement with Hybrid Time + Distance Tracking
**Date:** 2025-10-25 (Updated: 2025-10-30 - v2.1 quick swap modal addition)
**Status:** Complete - Aligned with Architecture (v2.1)
**Prepared by:** @ux-designer
**Ready for:** @database-expert and @fullstack-developer

---

## Context

This is the **final UX design (v2)** for the Component Status Refinement feature, aligned with architectural constraints. This design incorporates:

1. **Requirements document:** `.handovers/requirements/component-status-refinement-requirements.md`
2. **Initial UX design (v1):** Created 2025-10-25 with comprehensive UI specifications
3. **Architecture handover:** `.handovers/architecture/component-status-refinement-architect-handover.md` - reviewed 2025-10-29
4. **Architectural constraints:** 8 constraints addressed (see "Architectural Alignment" section below)

### Changes from v1 to v2 to v2.1

**v1 to v2 (2025-10-29):**
- **Added retired component indicator** to component detail page (constraint #7)
- **Confirmed validation error display pattern** uses existing toast notifications (constraint #4)
- **Confirmed progress bar capping behavior** at 100% maximum (constraint #5)
- **No other UX changes required** - v1 design already aligned with architecture

**v2 to v2.1 (2025-10-30):**
- **Added Section 8: Quick Swap Modal** - Missing specifications for 4 new fields in quick swap modal
- **Completed UX specifications** - All architect-required frontend elements now documented

### Design Approach

This design transforms the existing distance-only component tracking into a hybrid time + distance system while:
- Maintaining familiar Bootstrap 5 UI patterns already used throughout the application
- Ensuring mobile-first responsive design
- Supporting the new simplified 4-level status system (OK / Due / Exceeded / Not defined)
- Always showing BOTH time and distance fields (even when NULL/unused)
- Distinguishing between lifetime_status and service_status on detail pages
- Showing worst-case status in overview tables

---

## Deliverables

This handover includes UX specifications for:

1. **Component Creation/Edit Forms** - 6-field layout design
2. **Component Detail Page** - Dual progress bars, status display, and retired component alert (NEW in v2)
3. **Component Overview Table** - Single status column with triggers
4. **Bike Details Component Table** - Status display pattern
5. **ComponentType Management Forms** - Default configuration
6. **Status Indicator System** - Visual design for color + trigger indicators
7. **Mobile Responsive Designs** - Breakpoint specifications
8. **Quick Swap Modal** - 4 new fields for "Create new component" section (NEW in v2.1)
9. **Architectural Alignment Documentation** (NEW in v2) - How UX addresses 8 architectural constraints

---

## UX Specifications

### 1. Component Creation/Edit Forms

#### 1.1 Form Layout (6 New Fields)

**Current fields (existing):**
- Name, Type, Bike, Cost, Offset, Notes
- Expected lifetime (km), Service interval (km)

**NEW fields to add:**
- Expected lifetime (days)
- Service interval (days)
- Status threshold (km)
- Status threshold (days)

**Form Grid Structure (Bootstrap responsive grid):**

```
Row 1 (existing):
[Date (3 cols)] [Name (3 cols)] [Type (2 cols)] [Bike (2 cols)] [Cost (1 col)] [Offset (1 col)]

Row 2 (ENHANCED - distance):
[Lifetime Expected (km) (3 cols)] [Service Interval (km) (3 cols)] [Threshold (km) (3 cols)] [padding (3 cols)]

Row 3 (NEW - time):
[Lifetime Expected (days) (3 cols)] [Service Interval (days) (3 cols)] [Threshold (days) (3 cols)] [padding (3 cols)]

Row 4 (existing):
[Notes (12 cols - full width textarea)]
```

**Responsive breakpoints:**
- **md and up**: 3-column layout for interval/threshold fields as shown above
- **sm**: Stack to 2 columns (6 cols each)
- **xs**: Stack to 1 column (12 cols full width)

#### 1.2 Field Specifications

**Distance-based interval fields (Row 2):**

```html
<div class="col-md-3 mb-3">
    <label for="expected_lifetime" class="form-label fw-bold">
        Lifetime expected (km)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Total distance this component is expected to last">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="expected_lifetime" name="expected_lifetime"
           placeholder="e.g., 3000" value="">
    <div class="form-text small text-muted">Leave blank if time-based only</div>
</div>

<div class="col-md-3 mb-3">
    <label for="service_interval" class="form-label fw-bold">
        Service interval (km)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Distance between maintenance services">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="service_interval" name="service_interval"
           placeholder="e.g., 250" value="">
    <div class="form-text small text-muted">Leave blank if time-based only</div>
</div>

<div class="col-md-3 mb-3">
    <label for="threshold_km" class="form-label fw-bold">
        Threshold (km)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Warning triggers when remaining km drops below this value">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="threshold_km" name="threshold_km"
           placeholder="e.g., 300" value="">
    <div class="form-text small text-muted">Required if km intervals set</div>
</div>
```

**Time-based interval fields (Row 3 - NEW):**

```html
<div class="col-md-3 mb-3">
    <label for="lifetime_expected_days" class="form-label fw-bold">
        Lifetime expected (days)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Total time this component is expected to last from first installation">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="lifetime_expected_days" name="lifetime_expected_days"
           placeholder="e.g., 730" value="">
    <div class="form-text small text-muted">Leave blank if distance-based only</div>
</div>

<div class="col-md-3 mb-3">
    <label for="service_interval_days" class="form-label fw-bold">
        Service interval (days)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Time between maintenance services (resets on service)">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="service_interval_days" name="service_interval_days"
           placeholder="e.g., 180" value="">
    <div class="form-text small text-muted">Leave blank if distance-based only</div>
</div>

<div class="col-md-3 mb-3">
    <label for="threshold_days" class="form-label fw-bold">
        Threshold (days)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Warning triggers when remaining days drops below this value">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="threshold_days" name="threshold_days"
           placeholder="e.g., 30" value="">
    <div class="form-text small text-muted">Required if day intervals set</div>
</div>
```

#### 1.3 Form Validation & Feedback

**Client-side validation (JavaScript):**
- If `expected_lifetime` OR `service_interval` is filled → `threshold_km` becomes REQUIRED
- If `lifetime_expected_days` OR `service_interval_days` is filled → `threshold_days` becomes REQUIRED
- Threshold must be > 0 when required
- Threshold validation: `threshold_km` must be <= MIN(service_interval, lifetime_expected) when both defined
- Threshold validation: `threshold_days` must be <= MIN(service_interval_days, lifetime_expected_days) when both defined

**Validation error display:**
```html
<!-- Show below the threshold field if validation fails -->
<div class="invalid-feedback d-block">
    Threshold (300 km) must be less than or equal to the shortest interval (250 km).
</div>
```

**Inherited values indicator (for component detail form only):**

When a value is inherited from ComponentType (not manually overridden):

```html
<div class="col-md-3 mb-3">
    <label for="threshold_km" class="form-label fw-bold">
        Threshold (km)
        <span class="badge bg-info-subtle text-info-emphasis ms-1"
              data-bs-toggle="tooltip"
              title="Inherited from component type 'Chain'">Inherited</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="threshold_km" name="threshold_km" value="200">
    <button type="button" class="btn btn-sm btn-link text-decoration-none p-0 mt-1"
            onclick="resetToTypeDefault(this, 'threshold_km')">
        Reset to type default
    </button>
</div>
```

#### 1.4 Modal Size

**Component creation modal:** Keep existing `modal-xl` (extra large) to accommodate new fields
**Component details edit modal:** Keep existing size

---

### 2. Component Detail Page

#### 2.1 Status Card Header (Existing - Enhanced)

**Current design:** Card header shows component name with color based on worst-case status

**NEW color mapping:**
```jinja
<div class="card-header h5 fw-bold text-bg-
    {%- if lifetime_status == 'Not defined' and service_status == 'Not defined' -%}
        secondary
    {%- elif lifetime_status == 'Lifetime exceeded' or service_status == 'Service exceeded' -%}
        danger
    {%- elif lifetime_status == 'Due for replacement' or service_status == 'Due for service' -%}
        warning
    {%- else -%}
        success
    {%- endif -%}">
    {{ component_name }}
</div>
```

**Color mapping changes:**
- `text-bg-purple` → REMOVED (no longer used)
- `text-bg-danger` → Used for "Exceeded" statuses (was used for "Due")
- `text-bg-warning` → Used for "Due" statuses (was used for "Approaching")
- `text-bg-success` → Used for "OK" statuses (unchanged)
- `text-bg-secondary` → Used for "Not defined" status (unchanged)

#### 2.2 Retired Component Alert (NEW - v2)

**When component installation_status == "Retired"**, display alert at top of card body:

```html
<div class="alert alert-secondary mb-3" role="alert">
    <strong>⛔ This component was retired on {{ component.updated_date|format_date }}.</strong>
    <p class="mb-0 small">Time-based values are frozen as of retirement date.</p>
</div>
```

**Placement:** Immediately after card body opening tag, before mileage display.

**Rationale:** Clear indicator that time-based calculations are frozen (architectural constraint #7).

#### 2.3 Component Age & Mileage Display (Enhanced)

**Current display:**
```
📍 Mileage 2800 km
📅 Installed 180 days ago
🔧 Last serviced 45 days ago
```

**NEW display (enhanced with component age):**
```html
<span class="fw-bold">📍 Mileage {{ component_distance }} km</span>

<h6 class="card-title mt-2">
    📅 {% if component_age_days %}
        Component age: {{ component_age_days }} days
    {% else %}
        Component age: Not yet installed
    {% endif %}
</h6>

<h6 class="card-title mt-2">
    📅 {% if days_since_install %}
        Installed {{ days_since_install }} days ago
    {% else %}
        Not currently installed
    {% endif %}
</h6>

<h6 class="card-title mt-2">
    🔧 {% if days_since_service %}
        Last serviced {{ days_since_service }} days ago
    {% else %}
        Never serviced
    {% endif %}
</h6>
```

**Layout note:** Component age is DIFFERENT from days since install (age continues even when uninstalled, install date resets on each installation)

#### 2.4 Lifetime Status Section (Enhanced with Time + Distance)

**Wireframe:**
```
┌─────────────────────────────────────────────────────────────┐
│ 🚳 Lifetime reached in 200 km (Distance) 🟡 📍              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░│ │ (93% - yellow/warning)
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ 🚳 Lifetime reached in 80 days (Time) 🟢                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │████████████████████████████████████████████░░░░░░░░░░░░│ │ (89% - green/ok)
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ Final Status: Due for replacement 🟡 📍                      │
│ (Distance triggered - 200km remaining < 300km threshold)     │
└─────────────────────────────────────────────────────────────┘
```

**HTML Structure:**

```html
<span class="fw-bold">
    🚳 {% if lifetime_status_distance == 'Not defined' %}
        Expected lifetime (km) not defined
    {% elif lifetime_remaining_km <= 0 %}
        Lifetime exceeded by {{ lifetime_remaining_km * -1 }} km
    {% else %}
        Lifetime reached in {{ lifetime_remaining_km }} km
    {% endif %}

    {% if lifetime_status_distance != 'Not defined' %}
        <!-- Distance status indicator -->
        {% if lifetime_status_distance == 'OK' %}🟢
        {% elif lifetime_status_distance == 'Due for replacement' %}🟡
        {% elif lifetime_status_distance == 'Lifetime exceeded' %}🔴
        {% endif %}
    {% endif %}
</span>

<!-- Distance progress bar -->
{% if lifetime_expected %}
<div class="progress mt-2" role="progressbar" aria-label="Lifetime distance bar">
    <div class="progress-bar progress-bar-striped
        {% if lifetime_status_distance == 'Not defined' %}bg-secondary-subtle
        {% elif lifetime_status_distance == 'OK' %}bg-success
        {% elif lifetime_status_distance == 'Due for replacement' %}bg-warning
        {% else %}bg-danger
        {% endif %}"
        style="width: {{ lifetime_percentage_km }}%">
    </div>
</div>
{% endif %}

<hr/>

<!-- TIME-BASED LIFETIME (NEW) -->
<span class="fw-bold">
    🚳 {% if lifetime_status_time == 'Not defined' %}
        Expected lifetime (days) not defined
    {% elif lifetime_remaining_days <= 0 %}
        Lifetime exceeded by {{ lifetime_remaining_days * -1 }} days
    {% else %}
        Lifetime reached in {{ lifetime_remaining_days }} days
    {% endif %}

    {% if lifetime_status_time != 'Not defined' %}
        <!-- Time status indicator -->
        {% if lifetime_status_time == 'OK' %}🟢
        {% elif lifetime_status_time == 'Due for replacement' %}🟡
        {% elif lifetime_status_time == 'Lifetime exceeded' %}🔴
        {% endif %}
    {% endif %}
</span>

<!-- Time progress bar -->
{% if lifetime_expected_days %}
<div class="progress mt-2" role="progressbar" aria-label="Lifetime time bar">
    <div class="progress-bar progress-bar-striped
        {% if lifetime_status_time == 'Not defined' %}bg-secondary-subtle
        {% elif lifetime_status_time == 'OK' %}bg-success
        {% elif lifetime_status_time == 'Due for replacement' %}bg-warning
        {% else %}bg-danger
        {% endif %}"
        style="width: {{ lifetime_percentage_days }}%">
    </div>
</div>
{% endif %}

<hr/>

<!-- FINAL LIFETIME STATUS (Worst Case) -->
<div class="alert
    {% if lifetime_status == 'OK' %}alert-success
    {% elif lifetime_status == 'Due for replacement' %}alert-warning
    {% elif lifetime_status == 'Lifetime exceeded' %}alert-danger
    {% else %}alert-secondary
    {% endif %}
    mb-0 mt-2" role="alert">
    <strong>Lifetime Status: {{ lifetime_status }}</strong>

    {% if lifetime_status != 'Not defined' and lifetime_status != 'OK' %}
        <!-- Trigger indicator -->
        {% if lifetime_trigger == 'distance' %}
            📍 <small>(Distance triggered: {{ lifetime_remaining_km }} km < {{ threshold_km }} km threshold)</small>
        {% elif lifetime_trigger == 'time' %}
            📅 <small>(Time triggered: {{ lifetime_remaining_days }} days < {{ threshold_days }} days threshold)</small>
        {% elif lifetime_trigger == 'both' %}
            📍📅 <small>(Both triggered: {{ lifetime_remaining_km }} km < {{ threshold_km }} km AND {{ lifetime_remaining_days }} days < {{ threshold_days }} days)</small>
        {% endif %}
    {% endif %}
</div>
```

#### 2.5 Service Status Section (Enhanced with Time + Distance)

**Same pattern as lifetime section above**, but for service intervals:

```html
<!-- DISTANCE-BASED SERVICE -->
<span class="fw-bold">
    🧑‍🔧 {% if service_status_distance == 'Not defined' %}
        Service interval (km) not defined
    {% elif service_next_km <= 0 %}
        Service interval exceeded by {{ service_next_km * -1 }} km
    {% else %}
        Next service in {{ service_next_km }} km
    {% endif %}

    {% if service_status_distance != 'Not defined' %}
        {% if service_status_distance == 'OK' %}🟢
        {% elif service_status_distance == 'Due for service' %}🟡
        {% elif service_status_distance == 'Service exceeded' %}🔴
        {% endif %}
    {% endif %}
</span>

<!-- Distance progress bar (existing pattern) -->
{% if service_interval %}
<div class="progress mt-2" role="progressbar">
    <div class="progress-bar progress-bar-striped
        {% if service_status_distance == 'Not defined' %}bg-secondary-subtle
        {% elif service_status_distance == 'OK' %}bg-success
        {% elif service_status_distance == 'Due for service' %}bg-warning
        {% else %}bg-danger
        {% endif %}"
        style="width: {{ service_percentage_km }}%">
    </div>
</div>
{% endif %}

<hr/>

<!-- TIME-BASED SERVICE (NEW) -->
<span class="fw-bold">
    🧑‍🔧 {% if service_status_time == 'Not defined' %}
        Service interval (days) not defined
    {% elif service_next_days <= 0 %}
        Service interval exceeded by {{ service_next_days * -1 }} days
    {% else %}
        Next service in {{ service_next_days }} days
    {% endif %}

    {% if service_status_time != 'Not defined' %}
        {% if service_status_time == 'OK' %}🟢
        {% elif service_status_time == 'Due for service' %}🟡
        {% elif service_status_time == 'Service exceeded' %}🔴
        {% endif %}
    {% endif %}
</span>

<!-- Time progress bar (NEW) -->
{% if service_interval_days %}
<div class="progress mt-2" role="progressbar">
    <div class="progress-bar progress-bar-striped
        {% if service_status_time == 'Not defined' %}bg-secondary-subtle
        {% elif service_status_time == 'OK' %}bg-success
        {% elif service_status_time == 'Due for service' %}bg-warning
        {% else %}bg-danger
        {% endif %}"
        style="width: {{ service_percentage_days }}%">
    </div>
</div>
{% endif %}

<hr/>

<!-- FINAL SERVICE STATUS (Worst Case) -->
<div class="alert
    {% if service_status == 'OK' %}alert-success
    {% elif service_status == 'Due for service' %}alert-warning
    {% elif service_status == 'Service exceeded' %}alert-danger
    {% else %}alert-secondary
    {% endif %}
    mb-0 mt-2" role="alert">
    <strong>Service Status: {{ service_status }}</strong>

    {% if service_status != 'Not defined' and service_status != 'OK' %}
        {% if service_trigger == 'distance' %}
            📍 <small>(Distance triggered: {{ service_next_km }} km < {{ threshold_km }} km threshold)</small>
        {% elif service_trigger == 'time' %}
            📅 <small>(Time triggered: {{ service_next_days }} days < {{ threshold_days }} days threshold)</small>
        {% elif service_trigger == 'both' %}
            📍📅 <small>(Both triggered: {{ service_next_km }} km < {{ threshold_km }} km AND {{ service_next_days }} days < {{ threshold_days }} days)</small>
        {% endif %}
    {% endif %}
</div>
```

#### 2.6 Mobile Responsiveness

**Breakpoints:**
- **md and up (≥768px):** Side-by-side layout (component info card | details card)
- **sm and below (<768px):** Stacked layout (full width cards)

**Progress bar behavior:**
- All progress bars remain visible on mobile
- Progress bar labels may stack to 2 lines on narrow screens
- Alert boxes for final status remain full width

---

### 3. Component Overview Table

#### 3.1 Table Structure (Enhanced)

**Current columns:**
- Component, Collection, Type, Distance, Status, Lifetime, Service, Bike

**CHANGED columns:**
- **"Lifetime" column:** Now shows emoji + trigger (🟢, 🟡 📍, 🔴 📅, etc.)
- **"Service" column:** Now shows emoji + trigger (🟢, 🟡 📍, 🔴 📅, etc.)

**Emoji + Trigger Display Pattern:**

```html
<td class="text-center">
    <!-- Lifetime status emoji -->
    {% if lifetime_status == 'OK' %}🟢
    {% elif lifetime_status == 'Due for replacement' %}🟡
    {% elif lifetime_status == 'Lifetime exceeded' %}🔴
    {% elif lifetime_status == 'Not defined' %}⚪
    {% endif %}

    <!-- Trigger indicator (only if not OK or Not defined) -->
    {% if lifetime_status != 'OK' and lifetime_status != 'Not defined' %}
        {% if lifetime_trigger == 'distance' %}📍
        {% elif lifetime_trigger == 'time' %}📅
        {% elif lifetime_trigger == 'both' %}📍📅
        {% endif %}
    {% endif %}
</td>

<td class="text-center">
    <!-- Service status emoji -->
    {% if service_status == 'OK' %}🟢
    {% elif service_status == 'Due for service' %}🟡
    {% elif service_status == 'Service exceeded' %}🔴
    {% elif service_status == 'Not defined' %}⚪
    {% endif %}

    <!-- Trigger indicator (only if not OK or Not defined) -->
    {% if service_status != 'OK' and service_status != 'Not defined' %}
        {% if service_trigger == 'distance' %}📍
        {% elif service_trigger == 'time' %}📅
        {% elif service_trigger == 'both' %}📍📅
        {% endif %}
    {% endif %}
</td>
```

**Visual examples:**
- `🟢` - OK status (no trigger needed)
- `🟡 📍` - Due (distance triggered only)
- `🟡 📅` - Due (time triggered only)
- `🟡 📍📅` - Due (both distance AND time triggered)
- `🔴 📍` - Exceeded (distance triggered only)
- `🔴 📅` - Exceeded (time triggered only)
- `🔴 📍📅` - Exceeded (both triggered)
- `⚪` - Not defined (no intervals configured)

#### 3.2 Tooltip on Hover

Add Bootstrap tooltip to emoji + trigger cells:

```html
<td class="text-center"
    data-bs-toggle="tooltip"
    title="Due for replacement: 200 km remaining (< 300 km threshold)">
    🟡 📍
</td>

<td class="text-center"
    data-bs-toggle="tooltip"
    title="Due for service: 25 days remaining (< 30 days threshold)">
    🟡 📅
</td>

<td class="text-center"
    data-bs-toggle="tooltip"
    title="Lifetime exceeded: -50 km (exceeded by 50 km)">
    🔴 📍
</td>
```

#### 3.3 Statistics Section Updates

**Current statistics (at bottom of page):**
```
Lifetime statistics installed components:
🟢 Lifetime OK: 15
🟡 End of life approaching: 3
🔴 Due for replacement: 2
🟣 Lifetime exceeded: 1
⚪ Lifetime not defined: 5
```

**NEW statistics (simplified):**
```html
<div class="row">
    <p class="card-text text-center">
        <span class="fw-bold text-secondary">Lifetime statistics (installed components)</span>
    </p>
    <div class="col"><span>🟢 OK: {{ count_lifetime_status_ok }}</span></div>
    <div class="col"><span>🟡 Due for replacement: {{ count_lifetime_status_due }}</span></div>
    <div class="col"><span>🔴 Exceeded: {{ count_lifetime_status_exceeded }}</span></div>
    <div class="col"><span>⚪ Not defined: {{ count_lifetime_status_not_defined }}</span></div>
</div>

<hr/>

<div class="row">
    <p class="card-text text-center">
        <span class="fw-bold text-secondary">Service statistics (installed components)</span>
    </p>
    <div class="col"><span>🟢 OK: {{ count_service_status_ok }}</span></div>
    <div class="col"><span>🟡 Due for service: {{ count_service_status_due }}</span></div>
    <div class="col"><span>🔴 Exceeded: {{ count_service_status_exceeded }}</span></div>
    <div class="col"><span>⚪ Not defined: {{ count_service_status_not_defined }}</span></div>
</div>
```

**Note:** Statistics now use 4 levels (was 5 levels with "approaching" states)

#### 3.4 Mobile Responsiveness

**On mobile/tablet (<768px):**
- Table may require horizontal scrolling (maintain all columns)
- Consider hiding "Collection" column on xs breakpoint (show on sm+)
- Statistics: Stack to 2 columns instead of 4 or 5

---

### 4. Bike Details Component Table

#### 4.1 Component Table (Same as Overview)

**Apply same pattern as Component Overview Table:**
- Lifetime column: emoji + trigger (🟢, 🟡 📍, 🔴 📅, etc.)
- Service column: emoji + trigger
- Tooltips on hover

#### 4.2 Summary Card Updates

**Current summary card (left sidebar):**
```
Summary components
⚡ Installed: 12
⛔ Retired: 3

🟢 Lifetime OK: 8
🟡 End of life approaching: 2
🔴 Due for replacement: 1
🟣 Lifetime exceeded: 1
⚪ Lifetime not defined: 0

🟢 Service OK: 7
🟡 Service approaching: 3
🔴 Due for service: 1
🟣 Service interval exceeded: 1
⚪ Service interval not defined: 0
```

**NEW summary card (simplified status levels):**
```html
<div class="card shadow mb-4">
    <div class="card-body">
        <h5 class="card-title">Summary components</h5>
        <hr/>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>⚡ Installed:</span><span class="fw-bold">{{ count_installed }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>⛔ Retired:</span><span class="fw-bold">{{ count_retired }}</span>
        </p>
        <hr/>

        <!-- Lifetime statistics (4 levels) -->
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🟢 Lifetime OK</span><span class="fw-bold">{{ count_lifetime_ok }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🟡 Due for replacement</span><span class="fw-bold">{{ count_lifetime_due }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🔴 Lifetime exceeded</span><span class="fw-bold">{{ count_lifetime_exceeded }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>⚪ Lifetime not defined</span><span class="fw-bold">{{ count_lifetime_not_defined }}</span>
        </p>
        <hr/>

        <!-- Service statistics (4 levels) -->
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🟢 Service OK</span><span class="fw-bold">{{ count_service_ok }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🟡 Due for service</span><span class="fw-bold">{{ count_service_due }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>🔴 Service exceeded</span><span class="fw-bold">{{ count_service_exceeded }}</span>
        </p>
        <p class="card-text d-flex justify-content-between align-items-center">
            <span>⚪ Service not defined</span><span class="fw-bold">{{ count_service_not_defined }}</span>
        </p>
        <hr/>

        <p class="card-text d-flex justify-content-between align-items-center">
            <span>💰 Expected cost next service</span>
            <span class="fw-bold">{{ sum_cost }}</span>
        </p>
    </div>
</div>
```

---

### 5. ComponentType Management Forms

#### 5.1 Form Layout (Enhanced)

**Current fields:**
- Type name, Max per bike, Mandatory
- Expected lifetime (km), Service interval (km)
- Service interval (days) - currently disabled with "N/A"

**NEW form (enable time + thresholds):**

```html
<div class="modal-body">
    <div class="row">
        <!-- Row 1: Basic settings -->
        <div class="col-md-4 mb-3">
            <label for="component_type" class="form-label fw-bold">Type name</label>
            <input type="text" class="form-control" id="component_type" name="component_type" required>
        </div>
        <div class="col-md-4 mb-3">
            <label for="max_quantity" class="form-label fw-bold">Max per bike</label>
            <input type="number" min="0" step="1" class="form-control" id="max_quantity" name="max_quantity">
        </div>
        <div class="col-md-4 mb-3">
            <label class="form-label fw-bold d-block">Mandatory</label>
            <div class="form-check form-check-inline mt-2">
                <input class="form-check-input" type="radio" name="mandatory" id="mandatory_yes" value="Yes">
                <label class="form-check-label" for="mandatory_yes">Yes</label>
            </div>
            <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="mandatory" id="mandatory_no" value="No" checked>
                <label class="form-check-label" for="mandatory_no">No</label>
            </div>
        </div>

        <!-- Row 2: Distance-based defaults -->
        <div class="col-md-4 mb-3">
            <label for="expected_lifetime" class="form-label fw-bold">
                Default lifetime (km)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components of this type will inherit this value">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="expected_lifetime" name="expected_lifetime" placeholder="e.g., 3000">
        </div>
        <div class="col-md-4 mb-3">
            <label for="service_interval" class="form-label fw-bold">
                Default service int. (km)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components of this type will inherit this value">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="service_interval" name="service_interval" placeholder="e.g., 250">
        </div>
        <div class="col-md-4 mb-3">
            <label for="threshold_km" class="form-label fw-bold">
                Default threshold (km)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components will warn when remaining km drops below this">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="threshold_km" name="threshold_km" placeholder="e.g., 200">
        </div>

        <!-- Row 3: Time-based defaults (NEW - enable these fields) -->
        <div class="col-md-4 mb-3">
            <label for="lifetime_expected_days" class="form-label fw-bold">
                Default lifetime (days)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components of this type will inherit this value">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="lifetime_expected_days" name="lifetime_expected_days" placeholder="e.g., 730">
        </div>
        <div class="col-md-4 mb-3">
            <label for="service_interval_days" class="form-label fw-bold">
                Default service int. (days)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components of this type will inherit this value">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="service_interval_days" name="service_interval_days" placeholder="e.g., 180">
        </div>
        <div class="col-md-4 mb-3">
            <label for="threshold_days" class="form-label fw-bold">
                Default threshold (days)
                <span class="text-muted small" data-bs-toggle="tooltip"
                      title="New components will warn when remaining days drops below this">ⓘ</span>
            </label>
            <input type="number" min="0" step="1" class="form-control"
                   id="threshold_days" name="threshold_days" placeholder="e.g., 30">
        </div>
    </div>
</div>
```

#### 5.2 Help Text / Explainer

Add an info alert at top of modal body:

```html
<div class="alert alert-info mb-3" role="alert">
    <strong>ⓘ Component Type Defaults</strong>
    <p class="mb-0 small">
        These values serve as defaults for new components of this type.
        Changing these values will NOT update existing components - only new components created after this change.
        Leave fields blank if this component type doesn't use that tracking method.
    </p>
</div>
```

---

### 6. Status Indicator System (Visual Design)

#### 6.1 Color Indicators

**Emoji-based color system:**
- 🟢 **Green circle** = "OK" status (healthy, no action needed)
- 🟡 **Yellow circle** = "Due" status (action recommended soon)
- 🔴 **Red circle** = "Exceeded" status (action overdue)
- ⚪ **White circle** = "Not defined" status (no intervals configured)

**Bootstrap class mappings:**
- `text-bg-success` or `bg-success` → Green states
- `text-bg-warning` or `bg-warning` → Yellow states
- `text-bg-danger` or `bg-danger` → Red states
- `text-bg-secondary` or `bg-secondary-subtle` → Gray/white states

**Progress bar colors:**
- `progress-bar bg-success` → Green (OK)
- `progress-bar bg-warning` → Yellow (Due)
- `progress-bar bg-danger` → Red (Exceeded)
- `progress-bar bg-secondary-subtle` → Gray (Not defined)

#### 6.2 Trigger Indicators

**Emoji-based trigger indicators:**
- 📍 **Location pin** = Distance-triggered
- 📅 **Calendar** = Time-triggered
- 📍📅 **Pin + Calendar** = Both triggered simultaneously

**Display rules:**
- Show trigger ONLY when status is "Due" or "Exceeded" (not for "OK" or "Not defined")
- Always show trigger indicator AFTER the color emoji
- If BOTH time and distance are below their thresholds → show 📍📅
- If ONLY distance below threshold → show 📍
- If ONLY time below threshold → show 📅

**Example combinations:**
- `🟢` - OK, no trigger
- `🟡 📍` - Due, distance triggered
- `🟡 📅` - Due, time triggered
- `🟡 📍📅` - Due, both triggered
- `🔴 📍` - Exceeded, distance triggered
- `🔴 📅` - Exceeded, time triggered
- `🔴 📍📅` - Exceeded, both triggered
- `⚪` - Not defined, no trigger

#### 6.3 Legend / Help Documentation

Add a collapsible help section to Component Overview page:

```html
<div class="card shadow mb-3">
    <div class="card-header">
        <button class="btn btn-link text-decoration-none p-0 w-100 text-start"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#statusLegend">
            <span class="fw-bold">ⓘ Status Indicators Guide</span>
            <span class="float-end">▼</span>
        </button>
    </div>
    <div id="statusLegend" class="collapse">
        <div class="card-body">
            <h6 class="fw-bold">Color Indicators:</h6>
            <ul class="mb-3">
                <li>🟢 <strong>Green (OK)</strong> - Component is healthy, no action needed</li>
                <li>🟡 <strong>Yellow (Due)</strong> - Service or replacement recommended soon</li>
                <li>🔴 <strong>Red (Exceeded)</strong> - Service or replacement overdue</li>
                <li>⚪ <strong>White (Not defined)</strong> - No maintenance intervals configured</li>
            </ul>

            <h6 class="fw-bold">Trigger Indicators:</h6>
            <ul class="mb-3">
                <li>📍 <strong>Distance-triggered</strong> - Warning based on remaining kilometers</li>
                <li>📅 <strong>Time-triggered</strong> - Warning based on remaining days</li>
                <li>📍📅 <strong>Both triggered</strong> - Both distance AND time below thresholds</li>
            </ul>

            <h6 class="fw-bold">Examples:</h6>
            <ul class="mb-0">
                <li>🟢 - Component OK</li>
                <li>🟡 📍 - Due for service/replacement (200 km remaining < 300 km threshold)</li>
                <li>🟡 📅 - Due for service/replacement (25 days remaining < 30 days threshold)</li>
                <li>🟡 📍📅 - Due (BOTH distance and time below thresholds)</li>
                <li>🔴 📍 - Exceeded (negative km remaining)</li>
                <li>🔴 📅 - Exceeded (negative days remaining)</li>
            </ul>
        </div>
    </div>
</div>
```

---

### 7. Mobile Responsive Design

#### 7.1 Breakpoint Strategy

**Bootstrap 5 breakpoints used:**
- **xs (<576px):** Extra small phones - single column layout
- **sm (≥576px):** Small phones/tablets - 2 column forms
- **md (≥768px):** Tablets - 3 column forms, side-by-side cards
- **lg (≥992px):** Desktop - full layout
- **xl (≥1200px):** Large desktop - full layout
- **xxl (≥1400px):** Extra large desktop - full layout

#### 7.2 Component Detail Page (Mobile)

**On md and below (<768px):**
- Stack all cards vertically (full width)
- Component info card → full width
- Component details card → full width (below info card)
- Service history table → horizontal scroll if needed
- Installation history table → horizontal scroll if needed

#### 7.3 Forms (Mobile)

**Create/Edit Component Modal on mobile:**
- **md and up:** 3-column layout for interval/threshold fields
- **sm (576-768px):** 2-column layout (6 cols each)
- **xs (<576px):** Single column (12 cols full width, stack all fields)

**Field order on mobile (xs):**
1. Date
2. Name
3. Type
4. Bike
5. Cost
6. Offset
7. Lifetime expected (km)
8. Service interval (km)
9. Threshold (km)
10. Lifetime expected (days)
11. Service interval (days)
12. Threshold (days)
13. Notes

#### 7.4 Tables (Mobile)

**Component Overview Table on mobile:**
- Enable horizontal scrolling (wrap table in `.table-responsive`)
- Consider hiding less critical columns on xs:
  - Hide "Collection" column on xs (show on sm+)
  - Keep: Component, Type, Distance, Lifetime, Service, Bike
  - Action buttons remain visible

**Bike Details Component Table:**
- Same horizontal scroll pattern
- All columns remain visible (table is already compact)

#### 7.5 Statistics Cards (Mobile)

**Statistics section on mobile:**
- **md and up:** 4-5 columns per row
- **sm:** 2 columns per row
- **xs:** 1 column per row (stack vertically)

#### 7.6 Progress Bars (Mobile)

**Progress bars remain full width on all breakpoints:**
- Labels may wrap to 2 lines on narrow screens
- Progress bar itself remains horizontal (never vertical)
- Percentage width calculation unchanged

#### 7.7 Touch Targets

**All interactive elements meet accessibility standards:**
- Minimum tap target: 44x44px
- Buttons: Bootstrap default sizing ensures adequate touch targets
- Form inputs: Bootstrap form-control class provides adequate height
- Table rows: Clickable rows have adequate height (Bootstrap default)

---

### 8. Quick Swap Modal

**Context:** Quick swap allows users to quickly swap out an installed component with either an existing component OR a newly created component. When creating a new component during quick swap, the modal needs to collect the same time/distance interval configuration fields as the standard component creation form.

**Architectural reference:** Architecture handover lines 457-470 and 596-599.

#### 8.1 Modal Structure and Context

**File:** `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_quick_swap.html`

**Current behavior:**
- User selects bike and component position to swap
- Modal presents two radio options:
  1. "Swap with existing component" (select from dropdown)
  2. "Create new component" (inline creation form)

**Enhancement needed:** Add 4 new fields to "Create new component" form section.

#### 8.2 "Create New Component" Form Fields

**NEW fields to add when "Create new component" radio is selected:**

The quick swap modal's "Create new component" section should include the SAME 6 new fields as the standard component creation form:

**Distance-based intervals (existing row enhanced):**
- Lifetime expected (km)
- Service interval (km)
- **Threshold (km)** - NEW

**Time-based intervals (new row):**
- **Lifetime expected (days)** - NEW
- **Service interval (days)** - NEW
- **Threshold (days)** - NEW

#### 8.3 Field Specifications

**Important differences from Component Creation Modal:**
- **NO "Inherited" badge** - Component is being created fresh, no type inheritance UI needed
- **NO "Reset to type default" button** - Not applicable during creation
- **Fields start EMPTY** - No pre-populated values to show inheritance

**Otherwise, specifications are IDENTICAL to Section 1.2 (Component Creation/Edit Forms).**

**Distance threshold field (add to existing row):**
```html
<div class="col-md-4 mb-3">
    <label for="new_threshold_km" class="form-label fw-bold">
        Threshold (km)
        <span class="text-muted small" data-bs-toggle="tooltip"
              title="Warning triggers when remaining km drops below this value">ⓘ</span>
    </label>
    <input type="number" min="0" step="1" class="form-control"
           id="new_threshold_km" name="new_threshold_km"
           placeholder="e.g., 300" value="">
    <div class="form-text small text-muted">Required if km intervals set</div>
</div>
```

**Time-based interval fields (new row):**
```html
<!-- Row: Time-based intervals -->
<div class="row">
    <div class="col-md-4 mb-3">
        <label for="new_lifetime_expected_days" class="form-label fw-bold">
            Lifetime expected (days)
            <span class="text-muted small" data-bs-toggle="tooltip"
                  title="Total time this component is expected to last from first installation">ⓘ</span>
        </label>
        <input type="number" min="0" step="1" class="form-control"
               id="new_lifetime_expected_days" name="new_lifetime_expected_days"
               placeholder="e.g., 730" value="">
        <div class="form-text small text-muted">Leave blank if distance-based only</div>
    </div>

    <div class="col-md-4 mb-3">
        <label for="new_service_interval_days" class="form-label fw-bold">
            Service interval (days)
            <span class="text-muted small" data-bs-toggle="tooltip"
                  title="Time between maintenance services (resets on service)">ⓘ</span>
        </label>
        <input type="number" min="0" step="1" class="form-control"
               id="new_service_interval_days" name="new_service_interval_days"
               placeholder="e.g., 180" value="">
        <div class="form-text small text-muted">Leave blank if distance-based only</div>
    </div>

    <div class="col-md-4 mb-3">
        <label for="new_threshold_days" class="form-label fw-bold">
            Threshold (days)
            <span class="text-muted small" data-bs-toggle="tooltip"
                  title="Warning triggers when remaining days drops below this value">ⓘ</span>
        </label>
        <input type="number" min="0" step="1" class="form-control"
               id="new_threshold_days" name="new_threshold_days"
               placeholder="e.g., 30" value="">
        <div class="form-text small text-muted">Required if day intervals set</div>
    </div>
</div>
```

**Field name prefix:** All new fields use `new_` prefix (e.g., `new_threshold_km`, `new_service_interval_days`) to distinguish them from the component being swapped out.

#### 8.4 Validation Behavior

**Client-side validation:** Apply the SAME `validateComponentThresholds()` JavaScript function to the quick swap form (Architecture handover line 599).

**Validation rules (identical to component creation):**
- If `new_expected_lifetime` OR `new_service_interval` is filled → `new_threshold_km` becomes REQUIRED
- If `new_lifetime_expected_days` OR `new_service_interval_days` is filled → `new_threshold_days` becomes REQUIRED
- Threshold must be > 0 when required
- `new_threshold_km` must be <= MIN(new_service_interval, new_expected_lifetime) when both defined
- `new_threshold_days` must be <= MIN(new_service_interval_days, new_lifetime_expected_days) when both defined

**Server-side validation:** Same validation logic in business_logic.py applies when processing quick swap (Architecture handover lines 467-469).

**Error display:** Same pattern as component creation - inline validation errors below threshold fields, server-side errors use toast pattern.

#### 8.5 Differences from Component Creation Modal

**Key differences to note:**

| Aspect | Component Creation Modal | Quick Swap Modal |
|--------|-------------------------|------------------|
| **Field inheritance** | Shows "Inherited" badge for type defaults | NO inheritance UI - fresh component |
| **Field pre-population** | May show inherited values from ComponentType | Always starts empty |
| **Reset button** | "Reset to type default" button shown | NO reset button |
| **Field name prefix** | Standard names (e.g., `threshold_km`) | `new_` prefix (e.g., `new_threshold_km`) |
| **Context** | Standalone component creation | Creating while swapping existing component |
| **Validation** | Identical rules | Identical rules |
| **Layout** | Same grid structure | Same grid structure |

**Modal size:** Keep existing quick swap modal size (likely `modal-lg` or `modal-xl`).

**Responsive behavior:** Same as component creation form - fields stack on smaller screens (see Section 7 for breakpoint specs).

**Form submission:** POST to `/quick_swap` endpoint with all `new_` prefixed fields included in payload (Architecture handover lines 460-465).

---

## Decisions Made

### 1. Always Show Both Time and Distance Fields
**Rationale:** Consistent UI regardless of component type. User doesn't need to learn different interfaces for time-only vs. distance-only vs. hybrid components.

### 2. Dual Progress Bars on Detail Page
**Rationale:** Clear visual distinction between time-based and distance-based wear. User can see at a glance which factor is closer to threshold. Follows existing pattern (already show separate lifetime and service progress bars).

### 3. Single Status Column in Overview Tables
**Rationale:** Conserve horizontal space. Tables already have many columns. Worst-case status with trigger indicator provides sufficient information. User can click through to detail page for full breakdown.

### 4. Emoji-Based Indicators (Not Text Badges)
**Rationale:** Emojis are:
- Universal (no translation needed)
- Visually distinct (easier to scan)
- Compact (save space in tables)
- Accessible (can have aria-labels and tooltips)
- Consistent with existing bike status emoji usage (⚡💤⛔)

### 5. Trigger Indicators Only for "Due" and "Exceeded" States
**Rationale:** When status is "OK" or "Not defined", the trigger is irrelevant. Reduces visual noise. User only needs to know WHY a warning triggered when there IS a warning.

### 6. Simplified 4-Level Status System
**Rationale:** Requirements specify removing intermediate "approaching" states. Clearer decision points for users: OK (do nothing), Due (plan action), Exceeded (take action now), Not defined (configure intervals).

### 7. Threshold Fields Required Only When Intervals Configured
**Rationale:** Flexible system allows pure time-only, pure distance-only, or hybrid components. Validation ensures thresholds are configured where needed, but doesn't force thresholds when intervals aren't used.

### 8. Inherited Value Indicator for Component Detail Form
**Rationale:** User needs to understand which values come from ComponentType defaults vs. manual overrides. "Inherited" badge with reset button provides clear mental model and easy way to revert to type defaults.

### 9. ComponentType Form Shows "Default" Label
**Rationale:** Clarify that changing type defaults doesn't affect existing components. Prevents user confusion when they change a type default and wonder why existing components didn't update.

### 10. Progress Bar Color Matches Final Status
**Rationale:** Visual consistency. If final status is "Due" (yellow), both progress bars that contribute to that status should show yellow. Makes it clear which interval is causing the warning.

---

## Architectural Alignment (v2)

This section documents how the v2 UX design addresses the 8 architectural constraints from @architect's handover (`.handovers/architecture/component-status-refinement-architect-handover.md`, lines 611-663).

### Constraint #1: Time-Based Fields Stored in Database, Updated by Scheduler

**Architecture constraint:** `lifetime_remaining_days` and `service_next_days` stored in DB, updated nightly at 3:00 AM via APScheduler.

**UX impact:** ✅ **NO IMPACT** - Values available in template context as designed. May be up to 24 hours stale, which is acceptable for day-granularity tracking.

**UX confirmation:** No changes needed to v1 design. Template displays values from database as specified.

### Constraint #2: Trigger Indicators NOT Stored in Database

**Architecture constraint:** `lifetime_trigger` and `service_trigger` calculated on-demand when rendering pages, not stored in DB.

**UX impact:** ✅ **NO IMPACT** - Values still available in template context.

**UX confirmation:** No changes needed to v1 design. Template displays calculated values as specified.

### Constraint #3: Field Inheritance Implementation

**Architecture constraint:** Implemented via value comparison in Jinja2 template, not database flag. ComponentType data included in modal context.

**UX impact:** ✅ **NO CHANGES NEEDED** - "Inherited" badge logic as designed in v1 will work correctly.

**UX confirmation:** Section 1.3 "Inherited values indicator" already specifies template-based comparison. No changes required.

### Constraint #4: Validation Error Display

**Architecture constraint:** Server-side validation uses existing toast pattern (redirect with query parameters `?success=false&message=...`).

**UX impact:** ✅ **CONFIRMED PATTERN** - Existing validation display mechanism confirmed for use.

**UX alignment decision:**
- Client-side validation shows inline errors below threshold fields (as designed in v1, section 1.3)
- Server-side validation returns `(success, message, component_id)` tuple
- API redirects with query parameters if validation fails
- Frontend displays toast notification via existing DOMContentLoaded handler

**UX confirmation:** Section 1.3 "Validation error display" already shows inline errors. Add note that server-side errors use existing toast pattern.

### Constraint #5: Progress Bar Capping

**Architecture constraint:** Backend can return negative remaining values when exceeded. Backend returns uncapped percentage.

**UX impact:** ✅ **CONFIRMED CAPPING BEHAVIOR** - Template caps display at 100% maximum.

**UX alignment decision:**
- Backend returns raw percentage values (may exceed 100% or go negative)
- Template caps `style="width: ..."` at 100% maximum for visual consistency
- Label text shows "exceeded by X km/days" when negative

**Template implementation note:**
```jinja
{% set progress_width = [lifetime_percentage_km, 100]|min %}
<div class="progress-bar" style="width: {{ progress_width }}%"></div>
```

**UX confirmation:** Section 2.4 and 2.5 already specify "Lifetime exceeded by X km" label text. Add template-level capping logic.

### Constraint #6: Scheduler Performance Characteristics

**Architecture constraint:** Scheduler runs at 3:00 AM system time (UTC in Docker). Non-blocking async execution.

**UX impact:** ✅ **NO IMPACT** - Job runs during low-activity window. Users won't notice scheduled updates.

**UX confirmation:** No changes needed. Time-based values may be up to 24 hours stale, which is acceptable for day-granularity.

### Constraint #7: Retired Component Time Freeze

**Architecture constraint:** Time calculations freeze at retirement `updated_date`. Only retired components have frozen time-based values.

**UX impact:** ✅ **NEW UI ELEMENT ADDED** - Retired component alert box added to component detail page.

**UX alignment changes (v2):**
- **Added section 2.2 "Retired Component Alert"** with Bootstrap `alert-secondary` box
- Alert displays: "⛔ This component was retired on [date]. Time-based values are frozen as of retirement date."
- Placement: Top of card body, before mileage display
- Visible only when `component.installation_status == "Retired"`

**Rationale:** Users need clear indication that time-based values are frozen and why. Prevents confusion about why component age isn't advancing.

### Constraint #8: Null Handling in Templates

**Architecture constraint:** All new fields nullable (threshold_km, threshold_days, lifetime_expected_days, service_interval_days, lifetime_remaining_days, service_next_days).

**UX impact:** ✅ **CONFIRMED DESIGN** - v1 design already handles NULL values appropriately.

**UX confirmation:** Existing NULL handling patterns:
- Form fields show empty/placeholder when NULL (section 1.2)
- Status displays show "Not defined" when intervals are NULL (sections 2.4, 2.5)
- Help text says "Leave blank if time-based only" or "Leave blank if distance-based only"
- Progress bars don't render when interval field is NULL

No changes needed to v1 design.

---

### Summary: v1 to v2 to v2.1 Changes

**v1 to v2 (2025-10-29):**

**Added:**
1. Section 2.2 - Retired component alert box for component detail page

**Confirmed/Clarified:**
1. Validation error display uses existing toast pattern (constraint #4)
2. Progress bar capping at 100% in template (constraint #5)
3. Time-based values updated nightly, acceptable staleness (constraint #1)
4. All other v1 specifications remain unchanged and aligned with architecture

**v2 to v2.1 (2025-10-30):**

**Added:**
1. Section 8 - Quick Swap Modal specifications (4 new fields: service_interval_days, lifetime_expected_days, threshold_km, threshold_days)
2. Complete field specifications with HTML examples matching component creation form pattern
3. Validation rules and error handling for quick swap
4. Comparison table highlighting differences from component creation modal

**Rationale:** Quick swap modal was missing from v2 handover but required by architect (lines 457-470, 596-599 of architecture handover). This addition completes the UX specifications for all frontend elements.

---

## Next Steps for @database-expert and @fullstack-developer (v2.1)

### For @database-expert

**Now that UX v2.1 is complete (including quick swap modal) and aligned with architecture**, you should:

1. **Read all handovers:**
   - Requirements: `.handovers/requirements/component-status-refinement-requirements.md`
   - UX v2.1 (this document): `.handovers/ux/component-status-refinement-ux-designer-handover.md`
   - Architecture: `.handovers/architecture/component-status-refinement-architect-handover.md`

2. **Design database migration** for:
   - 4 new fields in ComponentTypes table
   - 6 new fields in Components table (4 config + 2 stored calculated fields)
   - Migration script with NULL defaults
   - Populate `threshold_km` = 200 for existing components with distance intervals

3. **Create database handover** in `.handovers/database/component-status-refinement-database-handover.md`

4. **Handoff to @fullstack-developer** after migration plan complete

### For @fullstack-developer (after database handover)

1. **Implement backend changes:**
   - Create scheduler.py with APScheduler integration
   - Refactor status calculation methods in business_logic.py
   - Extend API endpoints for new fields
   - Add validation logic to component creation/editing
   - Implement nightly scheduler job for time-based field updates

2. **Implement frontend changes:**
   - Update component detail page with dual progress bars and retired alert
   - Update component overview table with trigger indicators
   - Add 6 new form fields to component modals with validation
   - Add client-side validation JavaScript
   - Update bike details page component tables

3. **Reference UX specifications:**
   - Section 1: Form layouts and fields
   - Section 2: Component detail page with retired alert (NEW in v2)
   - Section 3: Component overview table
   - Section 4: Bike details page
   - Section 5: ComponentType management
   - Section 6: Status indicator system
   - Section 7: Mobile responsiveness
   - Section 8: Quick swap modal (NEW in v2.1)

4. **Create fullstack handover** when implementation complete

---

## Dependencies & Requirements

### Required for Architecture Phase

**Backend (@architect to review):**
- `/home/xivind/code/velo-supervisor-2000/backend/main.py` - Routing and payload structures
- `/home/xivind/code/velo-supervisor-2000/backend/business_logic.py` - Status calculation functions
- `/home/xivind/code/velo-supervisor-2000/backend/database_manager.py` - Query functions for ComponentHistory
- `/home/xivind/code/velo-supervisor-2000/backend/database_model.py` - Schema definitions

**Frontend templates (this UX design references):**
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_details.html` - Detail page layout
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_create_component.html` - Form layout
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_overview.html` - Table layout
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/bike_details.html` - Summary card layout
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_component_type.html` - Type form layout

### Data Flow Requirements

**Component Detail Page needs:**
- `component_age_days` (calculated: days since first installation)
- `lifetime_remaining_km` (calculated: lifetime_expected - component_distance)
- `lifetime_remaining_days` (calculated: lifetime_expected_days - component_age_days)
- `service_next_km` (calculated: service_interval - km_since_last_service)
- `service_next_days` (calculated: service_interval_days - days_since_last_service)
- `lifetime_status_distance` (calculated: OK/Due/Exceeded based on km)
- `lifetime_status_time` (calculated: OK/Due/Exceeded based on days)
- `service_status_distance` (calculated: OK/Due/Exceeded based on km)
- `service_status_time` (calculated: OK/Due/Exceeded based on days)
- `lifetime_status` (calculated: worst case of distance vs. time)
- `service_status` (calculated: worst case of distance vs. time)
- `lifetime_trigger` (calculated: 'distance'/'time'/'both'/'none')
- `service_trigger` (calculated: 'distance'/'time'/'both'/'none')
- `lifetime_percentage_km` (calculated: for progress bar width)
- `lifetime_percentage_days` (calculated: for progress bar width)
- `service_percentage_km` (calculated: for progress bar width)
- `service_percentage_days` (calculated: for progress bar width)

**Component Overview Table needs:**
- `lifetime_status` (final, worst case)
- `service_status` (final, worst case)
- `lifetime_trigger` (distance/time/both/none)
- `service_trigger` (distance/time/both/none)

**Component Forms need to accept:**
- `expected_lifetime` (nullable)
- `service_interval` (nullable)
- `lifetime_expected_days` (nullable)
- `service_interval_days` (nullable)
- `threshold_km` (nullable, validated when km intervals exist)
- `threshold_days` (nullable, validated when day intervals exist)

---

## Ambiguities & Blockers

**All ambiguities have been resolved through user decisions. Implementation details left to @architect.**

### [DECISION] Retired Component Time Calculation
**Decision:** Time-based calculations FREEZE at retirement date.

**Rationale:** Retired components are no longer actively deteriorating. Continuing time calculations would give false "exceeded" warnings for components no longer in use.

**Example:** Component retired on 2024-10-01 with component_age_days = 365. On 2024-11-01, still show 365 days (not 396 days).

**For architect to implement:**
- Determine if `component_age_days` should be stored as static value on retirement or calculated with retirement date cap
- Ensure status calculations handle retired components appropriately
- Optionally add "as of [retirement date]" indicator in UI

---

### [DECISION] Progress Bar Percentage Calculation Edge Cases
**Decision:** Cap progress bar at 100% maximum, even when exceeded. Show "exceeded by X km/days" in label text.

**Scenarios:**
1. Component at exactly 3,000 km (0 km remaining, 0% remaining) → Progress bar 100%
2. Component at 3,100 km (-100 km remaining, -3.3% remaining) → Progress bar 100% with label "Lifetime exceeded by 100 km"

**Rationale:** Progress bar going past 100% is visually confusing. Label text clearly communicates the exceeded state.

**For architect to implement:**
- Decide whether backend returns capped percentage (100% max) or frontend template handles capping (implementation detail)

---

### [DECISION] Threshold Validation Logic
**Decision:** Implement validation on BOTH client-side and server-side (backend).

**Client-side validation:**
- JavaScript checks threshold <= MIN(intervals) before form submission
- Shows inline error message immediately
- Prevents form submission until corrected

**Server-side validation:**
- FastAPI endpoint validates before database write
- Returns 400 error with validation message
- Frontend displays error alert if client-side validation bypassed

**Rationale:** Client-side provides immediate user feedback. Server-side ensures security and data integrity (client-side can be bypassed).

**For architect to implement:**
- Extend existing validation functions in `business_logic.py` module for threshold validation
- Define error response format from API
- Design how server-side validation errors are displayed in modal

---

### [DECISION] "Inherited" Value Detection
**Decision:** Use Option B - compare component value to component type value in frontend template.

**Approach:**
- ComponentType data is already available in modal context when creating/editing components
- Frontend template compares component's field value to ComponentType's default value
- If values match → display "Inherited" badge
- If values differ (or component value is NULL when type has value) → no badge

**Scenarios:**
1. New component created → all values match type defaults → show "Inherited" badges
2. User edits component, changes threshold_km from 200 to 300 → values differ → no badge
3. User edits component, doesn't touch threshold_km field → value still matches type → show "Inherited" badge

**Rationale:** ComponentType data is likely already loaded in modal context for dropdown population. No additional database fields needed. Simple comparison logic.

**For architect to implement:**
- Ensure ComponentType data is included in component edit/create modal context
- "Reset to type default" button logic: set component field value to match type default value
- Determine NULL handling (component NULL vs. type has value → inherited or not?)

---

### [DECISION] First Installation Date Query Performance
**Decision:** Computation strategy depends on whether value is stored in database or only used for display.

**Strategy:**
1. **If `component_age_days` is stored in database OR used to compute other stored fields:**
   - Compute nightly via scheduled batch job
   - Update stored values in Components table
   - Page load uses pre-computed values

2. **If `component_age_days` is only needed for display purposes:**
   - Compute lazily on page load (when component detail page is requested)
   - No storage needed, calculate from ComponentHistory on-the-fly
   - Acceptable performance for MVP

**Rationale:** Distinguishes between persistent data (needs batch computation) vs. display-only data (lazy calculation acceptable). Gives architect flexibility to choose appropriate strategy based on actual usage.

**For architect to implement:**
- Determine if `component_age_days` needs to be stored in database (for status calculations, aggregations, etc.)
- If lazy calculation: ensure ComponentHistory queries are efficient (consider indexes on component_id + updated_date)
- If batch computation: design nightly job to update time-based fields
- Consider hybrid approach: cache first_installation_date in Components table for faster lookups

---

**Blockers preventing completion:**

None identified at this stage. This is an initial UX design (v1). Architecture design can proceed.

---

## Questions / Recommendations for @architect

### Decisions Already Made (See Ambiguities & Blockers section for details)

✅ **Time-based field update strategy:** Conditional - batch if stored in DB, lazy if display-only
✅ **Validation logic:** Both client-side and server-side
✅ **Inherited value tracking:** Compare component value to type value in frontend template
✅ **Retired component handling:** Freeze time calculations at retirement date
✅ **Progress bar capping:** Cap at 100% maximum
✅ **First installation date caching:** Conditional - batch if needed for DB, lazy if display-only

### Remaining Questions for Architect

1. **Trigger indicator storage:** Calculate on-the-fly or store in database? (Implementation detail)
2. **Validation error format:** How should API return validation errors to frontend?
3. **ComponentType data availability:** Confirm ComponentType data is in modal context for inheritance comparison

### UX Recommendations

1. **Mobile-first validation:** Ensure validation error messages are clearly visible on small screens
2. **Loading states:** Add spinner/loading indicator for forms while calculating status (if calculation is slow)
3. **Empty states:** Clear messaging when component has no intervals configured ("Configure intervals to enable status tracking")
4. **Tooltip consistency:** All ⓘ icons should have consistent tooltip styling and behavior
5. **Form autosave:** Consider autosaving form values to localStorage to prevent data loss on accidental modal close
6. **Accessibility:** Ensure all color indicators have ARIA labels for screen readers (color alone should not convey meaning)
7. **Help documentation:** Include link to Help page in status indicators guide

---

## References

**Handover documents:**
- `.handovers/requirements/component-status-refinement-requirements.md` - Comprehensive requirements with user stories
- `.handovers/architecture/component-status-refinement-architect-handover.md` - Architecture design with 8 UX constraints (v2 input)

**Existing UI templates reviewed:**
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_details.html` - Current component detail page layout
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_create_component.html` - Current create component form
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_overview.html` - Current overview table
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/bike_details.html` - Current bike summary card
- `/home/xivind/code/velo-supervisor-2000/frontend/templates/modal_component_type.html` - Current component type form

**Project documentation:**
- `/home/xivind/code/velo-supervisor-2000/CLAUDE.md` - Project structure, Bootstrap 5 usage patterns
- `/home/xivind/code/velo-supervisor-2000/.handovers/TEMPLATE.md` - Handover template
- `/home/xivind/code/velo-supervisor-2000/.handovers/CLAUDE.md` - Handover workflow instructions

---

## Handover Checklist

**For all agents:**
- [x] All sections of template filled with specific information
- [x] File paths include line numbers where relevant (referenced templates)
- [x] Status field accurately reflects work state (v2 - Complete, Aligned with Architecture)
- [x] Next agents identified and tagged (@database-expert and @fullstack-developer)
- [x] All ambiguities resolved with [DECISION] tags (5 decisions in v1, architectural alignment in v2)
- [x] All blockers flagged with [BLOCKED BY] (none at this stage)
- [x] References include specific file paths and architecture handover

**@ux-designer:**
- [x] Wireframes or mockups referenced (ASCII wireframes and detailed HTML examples included)
- [x] Mobile responsiveness addressed (Section 7 with breakpoint specifications)
- [x] Bootstrap components specified (Progress bars, cards, forms, badges, alerts, tooltips, modals)
- [x] User interactions documented (Form validation, tooltips, collapsible legend, inherited value indicators)
- [x] Architectural constraints reviewed and addressed (8 constraints documented in "Architectural Alignment" section)
- [x] v2 updates clearly marked (retired component alert, validation/progress bar confirmations)

---

**Handover Created:** `.handovers/ux/component-status-refinement-ux-designer-handover.md` (v2.1 - complete)

**Next Agents:**
- **@database-expert** - Design migration for 10 new database fields (4 ComponentTypes, 6 Components)
- **@fullstack-developer** - Implement backend + frontend after database migration complete

**Action Required:**
- @database-expert: Create migration plan based on architecture and UX specifications
- @fullstack-developer: Implement feature using architecture plan, database schema, and this UX design (including quick swap modal)

**Workflow Note:** Version history:
- v1 created 2025-10-25 (initial UX design)
- v2 created 2025-10-29 (aligned with architecture, added retired component alert)
- v2.1 created 2025-10-30 (added missing quick swap modal specifications)
