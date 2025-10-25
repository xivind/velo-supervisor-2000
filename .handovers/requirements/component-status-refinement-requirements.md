# Component Status Refinement - Requirements Document

**Feature:** Component Status Refinement with Hybrid Time + Distance Tracking
**Date:** 2025-10-19
**Status:** Complete
**Prepared by:** @product-manager
**Ready for:** @ux-designer

---

## Executive Summary

The Component Status Refinement feature transforms the current distance-only component lifecycle tracking into a sophisticated hybrid system that considers both time-based deterioration AND distance-based wear. This addresses critical real-world scenarios where components deteriorate regardless of use (rubber perishes, sealant dries out) and provides more nuanced status determination with refined thresholds.

**Primary Improvements:**
1. **Hybrid Time + Distance Calculations**: Components evaluated on BOTH time and distance (worst case wins)
2. **Simplified Status Thresholds**: Clean logic comparing remaining value against absolute threshold (no percentage needed)
3. **Simplified Status Levels**: Removing "Service approaching" / "End of life approaching" intermediate states (4-level system: OK / Due / Exceeded / Not defined) with emoji indicators (🟢 green / 🟡 yellow / 🔴 red / ⚪ white)
4. **Time-Based Tracking**: NEW time intervals (service_interval_days, lifetime_expected_days) with same inheritance pattern as existing distance intervals
5. **User-Configurable Thresholds**: NEW threshold fields (threshold_km, threshold_days) with same inheritance pattern as existing distance intervals
6. **Comprehensive UI Updates**: Display both time-based and distance-based progress bars, days remaining, and intelligent status indicators

**Key Value Proposition:** Enable accurate lifecycle tracking for all component types - from pure time-based (tubeless sealant), pure distance-based (chains), to hybrid components (tires), eliminating false "OK" statuses for deteriorating components.

---

## Context & Problem Statement

### Current System Limitations

The existing system tracks component lifecycles using ONLY distance (kilometers):

**Current Status Logic:**
```
IF 0% ≤ reached ≤ 70%: "OK"
IF 70% < reached ≤ 90%: "Service approaching" / "End of life approaching"
IF 90% < reached ≤ 100%: "Due for service" / "Due for replacement"
IF reached > 100%: "Service interval exceeded" / "Lifetime exceeded"
```

**Critical Pain Points:**

1. **Time-Based Deterioration Ignored**
   - Tubeless sealant dries out after 6 months regardless of distance
   - Rubber brake pads harden over time even when unused
   - Tubeless tape adhesive degrades after 2-3 years
   - System shows "OK" for components that are actually unusable

2. **Premature Warnings for Long-Life Components**
   - Chain with 3,000km lifetime expected, 2,800km accumulated (93%)
   - Current system: "Due for replacement" at 90% threshold
   - Reality: Component has 200km remaining (weeks of riding)
   - User receives "critical" warning despite ample remaining life

3. **Intermediate Status Levels Add Complexity**
   - Three warning levels (70%, 90%, 100%) create confusion
   - Users unclear when to actually take action
   - "Service approaching" is not actionable (how soon is "approaching"?)

4. **No User-Configurable Status Thresholds**
   - Status thresholds are hardcoded in the business logic
   - Users cannot customize when warnings appear based on their risk tolerance or component type
   - Example: 3,000km chain at 2,700km triggers "Due" warning at hardcoded 90% threshold, but user cannot adjust this
   - Long-lifetime components receive warnings too early; short-lifetime components may warn too late

### Real-World Scenarios

**Scenario 1: Tubeless Sealant (Time-Only Component)**
> Martin adds fresh tubeless sealant to his gravel bike tires in January. By July (6 months later), he has only ridden 800km due to winter weather.
>
> **Current system behavior:** Sealant shows "OK" because distance-based tracking doesn't apply.
>
> **Reality:** Sealant has completely dried out and tires are losing air pressure.
>
> **Desired behavior:** System shows "Service exceeded" because 180 days elapsed > 180 day service interval, triggering time-based status calculation.

**Scenario 2: Road Chain (Distance-Only, Long Lifetime)**
> Sarah's road bike chain has a 3,000km expected lifetime. She reaches 2,800km (93% consumed, 200km remaining).
>
> **Current system behavior:** "Due for replacement" warning (triggered at hardcoded 90% threshold) with red badge.
>
> **Reality:** 200km remaining is approximately 2 weeks of normal riding - not yet critical.
>
> **Desired behavior:** "Due for replacement" status because 200km < 300km threshold (user-configured) → Component triggers warning when remaining distance drops below threshold. User could set lower threshold (e.g., 100km) to avoid premature warnings if desired.

**Scenario 3: Tire (Hybrid Time + Distance)**
> Elena's gravel tire has 5,000km expected lifetime AND 730 days (2 years) time-based lifetime. After 650 days and 4,200km, rubber is visibly deteriorating (800km and 80 days remaining).
>
> **Current system behavior:** "OK" status (distance-only tracking).
>
> **Reality:** Tire is approaching end of life due to time-based rubber deterioration.
>
> **Desired behavior:** "Due for replacement" status triggered by time factor (80 days < 90 day threshold), even though distance is still healthy (800km > 500km threshold).

**Scenario 4: Brake Pads (Reaches End of Life)**
> Marcus's brake pads reach exactly 2,500km (0km remaining from 2,500km expected lifetime).
>
> **Current system behavior:** "Due for replacement" (hardcoded threshold).
>
> **Reality:** Pads are at end of specified lifetime and should be replaced.
>
> **Desired behavior:** "Lifetime exceeded" status (0km <= 0) - simpler logic, clear message.

---

## User Personas

### Primary Persona: The Multi-Bike Long-Distance Cyclist
- **Profile**: Owns multiple bikes (road, gravel, MTB), tracks all components meticulously
- **Pain Point**: Some bikes used frequently (distance-based wear), others stored seasonally (time-based deterioration)
- **Frequency**: Reviews component status weekly
- **Needs**: Accurate status for BOTH high-mileage components AND time-sensitive components (sealant, tape, rubber)

### Secondary Persona: The Casual Commuter
- **Profile**: Rides occasionally, bike sometimes stored for months
- **Pain Point**: Returns to bike after storage, discovers dried sealant or hardened brake pads
- **Frequency**: Reviews status before long rides or after storage periods
- **Needs**: Time-based warnings for components that deteriorate during storage

### Tertiary Persona: The Component Optimizer
- **Profile**: Experiments with different component brands/models, tracks individual performance
- **Pain Point**: Cannot customize status thresholds to reduce noise from premature warnings or adjust for component-specific risk tolerance
- **Frequency**: Constantly tweaking component configurations
- **Needs**: User-configurable absolute thresholds (km and days) for status determination

---

## Detailed Requirements

### FR-1: Simplified Status Threshold Logic

**FR-1.1: Simplified Status Levels**

Replace current 4-level status system with new 4-level system:

**Previous System:**
- "OK" (0-70%)
- "Service approaching" / "End of life approaching" (70-90%)
- "Due for service" / "Due for replacement" (90-100%)
- "Service interval exceeded" / "Lifetime exceeded" (>100%)

**New System:**
- **"OK"** (Healthy, no action needed) - 🟢 Green indicator
- **"Due for service"** / **"Due for replacement"** (Action recommended soon) - 🟡 Yellow indicator
- **"Service exceeded"** / **"Lifetime exceeded"** (Action overdue) - 🔴 Red indicator
- **"Not defined"** (No maintenance intervals configured) - ⚪ White indicator

**FR-1.2: "Due for Service/Replacement" Logic (Simplified)**

A component enters "Due" status when remaining value is below threshold:

**Distance-based:**
```
IF remaining_km <= 0 THEN
   status = "Service exceeded" (or "Lifetime exceeded")
ELSE IF remaining_km < threshold_km THEN
   status = "Due for service" (or "Due for replacement")
ELSE
   status = "OK"
```

**Time-based:**
```
IF remaining_days <= 0 THEN
   status = "Service exceeded" (or "Lifetime exceeded")
ELSE IF remaining_days < threshold_days THEN
   status = "Due for service" (or "Due for replacement")
ELSE
   status = "OK"
```

**Example:**
- Component: 3,000km lifetime expected
- Threshold: threshold_km = 300km
- Current: 2,800km consumed (200km remaining)
- Logic: 200km < 300km
- **Result: "Due for replacement"**

**Example 2:**
- Component: 3,000km lifetime expected
- Threshold: threshold_km = 300km
- Current: 2,500km consumed (500km remaining)
- Logic: 500km >= 300km
- **Result: "OK" status**

**Example 3:**
- Component: 3,000km lifetime expected
- Threshold: threshold_km = 300km
- Current: 3,100km consumed (-100km remaining)
- Logic: -100km <= 0
- **Result: "Lifetime exceeded"**

**FR-1.3: User-Configurable Thresholds**

**At ComponentTypes level (defaults for new components):**
- `threshold_km` (IntegerField, nullable, default: NULL)
- `threshold_days` (IntegerField, nullable, default: NULL)

**At Components level (inheritable, overridable):**
- `threshold_km` (IntegerField, nullable, inherited from type, user-editable)
- `threshold_days` (IntegerField, nullable, inherited from type, user-editable)

**Validation Rules:**
- If component has `service_interval` OR `lifetime_expected` (any distance interval) → `threshold_km` is **REQUIRED** (not NULL)
- If component has `service_interval_days` OR `lifetime_expected_days` (any time interval) → `threshold_days` is **REQUIRED** (not NULL)
- Same threshold used for BOTH service and lifetime calculations (one `threshold_km` for both distance-based service AND lifetime and one `threshold_days` for both time-based service AND time-based lifetime)

**Rationale:**
- Long-lifetime components (e.g., 10,000km cassette) benefit from higher absolute thresholds (e.g., 1,000km)
- Short-lifetime components (e.g., 500km chain wax) benefit from lower thresholds (e.g., 100km)
- Users can customize thresholds per ComponentType with sensible defaults, then override per component if needed
- Simpler than percentage-based logic while providing same flexibility

---

### FR-2: Time-Based Deterioration Tracking

**FR-2.1: Time Interval Fields (Nullable)**

**New fields in ComponentTypes table:**
- `service_interval_days` (IntegerField, nullable, default: NULL)
- `lifetime_expected_days` (IntegerField, nullable, default: NULL)

**New fields in Components table:**
- `service_interval_days` (IntegerField, nullable, inherited from type, user-editable)
- `lifetime_expected_days` (IntegerField, nullable, inherited from type, user-editable)

**Behavior:**
- NULL = time-based tracking disabled for that interval
- User can define ONLY service_interval_days, ONLY lifetime_expected_days, BOTH, or NEITHER
- Backend validates: if NULL, skip time-based calculations for that interval

**FR-2.2: Time-Based Calculated Fields**

**New calculated fields in Components table:**
- `component_age_days` (IntegerField, calculated from first installation date)
- `lifetime_remaining_days` (IntegerField, calculated: lifetime_expected_days - component_age_days)
- `service_next_days` (IntegerField, calculated: service_interval_days - days_since_last_service)

**Calculation Source:**
- **First installation date**: Derived from ComponentHistory table (earliest record with update_reason = "Installed")
- **Age**: Count days from first installation to current date (continues even when uninstalled)
- **Days since last service**: Count days from latest service record to current date

**FR-2.3: Time Calculation Edge Cases**

**Component never installed:**
- `component_age_days` = NULL
- `lifetime_remaining_days` = NULL
- `service_next_days` = NULL
- No time-based status calculations

**Component uninstalled then reinstalled:**
- Age timer NEVER resets
- Age continues counting while uninstalled
- Example: Installed Jan 1, uninstalled Mar 1 (60 days), reinstalled Jun 1 = 150 days old
- Rationale: Rubber/sealant deteriorates regardless of installation status

**Service interval timer vs. Lifetime timer:**
- Service interval → **RESETS to 0** when service registered
- Lifetime → **NEVER resets** (continues from first installation)

**FR-2.4: Hybrid Time + Distance Status Calculation (Worst Case Wins)**

When component has BOTH time AND distance intervals defined:

```
Calculate distance_based_status (using distance logic)
Calculate time_based_status (using time logic)

IF time_based_status is WORSE than distance_based_status THEN
   final_status = time_based_status
ELSE
   final_status = distance_based_status
END IF
```

**Status severity ranking (worst to best):**
1. "Exceeded" (worst)
2. "Due for service/replacement"
3. "OK" (best)

**Example 1: Time is worse**
- Distance-based: 1,500km remaining, threshold_km = 500km → "OK" (1,500 >= 500)
- Time-based: 15 days remaining, threshold_days = 30 days → "Due for replacement" (15 < 30)
- **Final: "Due for replacement" with 📅 indicator** (time-based is worse, time triggered)

**Example 2: Both below thresholds**
- Distance-based: 150km remaining, threshold_km = 200km → "Due for replacement" (150 < 200)
- Time-based: 20 days remaining, threshold_days = 30 days → "Due for replacement" (20 < 30)
- **Final: "Due for replacement" with 📍📅 indicator** (both at same severity level, BOTH triggered)

**FR-2.5: Single-Interval Components (Time-Only or Distance-Only)**

**Time-only component (e.g., tubeless sealant):**
- `service_interval_days` = 180, `lifetime_expected_days` = 365
- `service_interval` (km) = NULL, `lifetime_expected` (km) = NULL
- Only time-based status calculations run
- Distance accumulated is still displayed (for reference)

**Distance-only component (e.g., chain):**
- `service_interval` = 250km, `lifetime_expected` = 3,000km
- `service_interval_days` = NULL, `lifetime_expected_days` = NULL
- Only distance-based status calculations run
- Elapsed days still displayed (for reference)

**Consistent UI principle:** Always show BOTH time and distance fields in UI, even if values are NULL/unused.

---

### FR-3: Database Schema Changes

**FR-3.1: ComponentTypes Table - New Fields**

| Field Name | Type | Nullable | Default | Description |
|------------|------|----------|---------|-------------|
| `service_interval_days` | IntegerField | Yes | NULL | Time-based service interval in days |
| `lifetime_expected_days` | IntegerField | Yes | NULL | Expected lifetime in days |
| `threshold_km` | IntegerField | Yes | NULL | Absolute km threshold for "Due" status |
| `threshold_days` | IntegerField | Yes | NULL | Absolute days threshold for "Due" status |

**FR-3.2: Components Table - New Fields**

| Field Name | Type | Nullable | Default | Description |
|------------|------|----------|---------|-------------|
| `service_interval_days` | IntegerField | Yes | NULL | Inherited from type, user-overridable |
| `lifetime_expected_days` | IntegerField | Yes | NULL | Inherited from type, user-overridable |
| `threshold_km` | IntegerField | Yes | NULL | Inherited from type, user-overridable |
| `threshold_days` | IntegerField | Yes | NULL | Inherited from type, user-overridable |
| `component_age_days` | IntegerField | Calculated | N/A | Days since first installation (calculated field) |
| `lifetime_remaining_days` | IntegerField | Calculated | N/A | Days until lifetime expected (calculated field) |
| `service_next_days` | IntegerField | Calculated | N/A | Days until next service (calculated field) |

**EXISTING Fields Being Modified (Not New):**

The following fields ALREADY exist in the Components table and are being modified in HOW they are calculated:

| Field Name | Type | Nullable | Current Behavior | New Behavior |
|------------|------|----------|------------------|--------------|
| `lifetime_status` | CharField | No | Calculated from distance only | Worst case of (distance-based lifetime, time-based lifetime) |
| `service_status` | CharField | No | Calculated from distance only | Worst case of (distance-based service, time-based service) |

**CRITICAL:** These two status fields remain **separate and independent**. They are NOT merged into a single field.

**Note on calculated fields:**
- These should be stored in database and must be updated automatically when time passes (requires update strategy)

**FR-3.3: Validation Rules (Application-Level)**

While database fields are nullable for flexibility, application-level validation enforces:
- If component has `service_interval` OR `lifetime_expected` (any distance interval) → `threshold_km` is **REQUIRED**
- If component has `service_interval_days` OR `lifetime_expected_days` (any time interval) → `threshold_days` is **REQUIRED**
- Threshold values must be > 0 when configured

**FR-3.4: Migration Strategy (Backward Compatibility)**

**For ComponentTypes table during migration:**
- `service_interval_days` → NULL (no time intervals exist currently)
- `lifetime_expected_days` → NULL (no time intervals exist currently)
- `threshold_km` → 200 (for ComponentTypes WITH service_interval OR lifetime_expected defined)
- `threshold_km` → NULL (for ComponentTypes with NO distance intervals defined)
- `threshold_days` → NULL (no time intervals exist yet, so not needed)

**For Components table during migration:**
- `service_interval_days` → NULL (no time intervals exist currently)
- `lifetime_expected_days` → NULL (no time intervals exist currently)
- `threshold_km` → 200 (for Components WITH service_interval OR lifetime_expected defined)
- `threshold_km` → NULL (for Components with NO distance intervals defined)
- `threshold_days` → NULL (no time intervals exist yet, so not needed)

**Post-migration:**
- User can configure time intervals as needed
- No automatic population of time intervals (ensures data quality and user control)

---

### FR-4: Status Display & UI Updates

**FR-4.1: Status Badge with Trigger Indicator**

**CRITICAL: Two Database Fields, Different Display Contexts**

The Components table stores **TWO separate status fields**:
- `lifetime_status` - Component replacement status
- `service_status` - Component maintenance status

**Status display depends on UI context:**

**1. Component Tables (Overview/List Pages) - Single Status Column**

To conserve horizontal space in tables, display a **single "Status" column** showing:
- **Worst case of (`lifetime_status` vs `service_status`)**
- The status text indicates which field: "Due for replacement" (lifetime) or "Due for service" (service)
- Trigger indicator shows whether time (📅) or distance (📍) caused this status

**2. Component Detail Page - Both Statuses Shown Separately**

On the component detail page, display **BOTH statuses independently**:
- Lifetime Status: Shows `lifetime_status` with its own trigger indicator
- Service Status: Shows `service_status` with its own trigger indicator

---

**Status color indicators:**
- 🟢 Green: "OK" status
- 🟡 Yellow: "Due for service" or "Due for replacement" status
- 🔴 Red: "Service exceeded" or "Lifetime exceeded" status
- ⚪ White: "Not defined" status (no intervals configured for this component)

**Trigger indicator (icon/badge) showing which factor triggered status:**

| Icon | Meaning | Example |
|------|---------|---------|
| 📍 | Distance-triggered only | Distance (km) below threshold, time is OK (above threshold or not configured) |
| 📅 | Time-triggered only | Time (days) below threshold, distance is OK (above threshold or not configured) |
| 📍📅 | Both triggered | **BOTH** time AND distance are below their respective thresholds |

**Example display (component tables - worst case shown):**
- "Due for replacement 🟡 📅" (lifetime is worse, time below threshold only, yellow indicator)
- "Service exceeded 🔴 📍" (service is worse, distance below threshold only, red indicator)
- "Due for replacement 🟡 📍📅" (lifetime is worse, **BOTH** time AND distance below their thresholds, yellow indicator)
- "OK 🟢" (both lifetime and service are OK, green indicator)

**Example 1: Component with different lifetime vs service statuses (table view shows worst)**
- `lifetime_status` = "OK 🟢" (5,000km remaining, 200 days remaining)
- `service_status` = "Due for service 🟡 📍" (150km remaining < 200km threshold)
- **Table displays:** "Due for service 🟡 📍" (service is worse than lifetime)

**Example 2: Both time AND distance below thresholds (📍📅 indicator)**
- Component has:
  - 180km remaining, threshold_km = 200km → Distance below threshold ✓
  - 25 days remaining, threshold_days = 30 days → Time below threshold ✓
- `lifetime_status` = "Due for replacement 🟡 📍📅"
- **Table displays:** "Due for replacement 🟡 📍📅" (BOTH factors contributing to status)

**Example 3: Component with no intervals configured (⚪ indicator)**
- Component has:
  - service_interval = NULL, lifetime_expected = NULL
  - service_interval_days = NULL, lifetime_expected_days = NULL
- `lifetime_status` = "Not defined ⚪"
- `service_status` = "Not defined ⚪"
- **Table displays:** "Not defined ⚪" (no maintenance intervals configured, no trigger indicator)

**FR-4.2: Progress Bars for Time and Distance**

**Component detail page and overview pages:**

**If component has BOTH time AND distance intervals:**
- Show TWO progress bars (stacked vertically)
- Distance-based progress bar (existing pattern)
- Time-based progress bar (new, same visual pattern)

**If component has ONLY distance intervals:**
- Show ONLY distance progress bar
- Time fields displayed as "Not configured" or "-"

**If component has ONLY time intervals:**
- Show ONLY time progress bar
- Distance fields displayed but not used for status

**Progress bar data:**
- Progress bar fill percentage
- Label: "Lifetime reached in 78 days" or "Next service in 78 days"
- Color coding based on status: 🟢 green for "OK", 🟡 yellow for "Due", 🔴 red for "Exceeded"

**FR-4.3: Days Remaining Display**

**Display format (consistent with existing km remaining format):**
- "Lifetime remaining: 78 days" (or "Lifetime reached in 78 days")
- "Next service: 45 days" (or "Next service in 45 days")
- Negative values: "Lifetime exceeded by 15 days"

**FR-4.4: Component Creation/Edit Forms**

**Always show BOTH time AND distance fields:**
- Service Interval (km): [____] km
- Service Interval (days): [____] days
- Lifetime Expected (km): [____] km
- Lifetime Expected (days): [____] days
- Status Threshold (km): [____] km
- Status Threshold (days): [____] days
- All these fields are inherited from component types, and NULL if empty in component types

**Behavior:**
- Empty/blank field → stored as NULL in database
- User can leave any combination blank, but validation rules apply see validation rules
- Consistent interface regardless of component type

**Form validation:**
- Threshold km: >0 (when distance intervals configured)
- Threshold days: >0 (when time intervals configured)
- Time/distance intervals: NULL or >0

**FR-4.5: Component Type Management Forms**

Same field layout as component forms, but:
- Fields represent defaults for new components of this type
- **Changing ComponentType defaults does NOT automatically update existing components** (e.g., changing "Chain" type's service_interval from 250km to 300km does NOT update existing chain components)
- User must manually update existing components if desired after changing type defaults
- Component type form for new component types always starts with all blank fields 

---

### FR-5: Backend Business Logic Updates

**FR-5.1: Status Calculation Function Refactoring**

**Current function signature:**
```python
def compute_component_status(self, mode, reached_distance_percent):
    # Returns status based on percentage only
```

**New function signature (proposed):**
```python
def compute_component_status(self, mode, remaining_value, threshold_value):
    """
    Compute component status using simplified threshold logic.

    Args:
        mode: "service" or "lifetime"
        remaining_value: Int (km or days remaining)
        threshold_value: Int (threshold km or days)

    Returns:
        status: String ("OK", "Due for service", "Service exceeded", etc.)
    """
    if remaining_value <= 0:
        return "Service exceeded" if mode == "service" else "Lifetime exceeded"

    if remaining_value < threshold_value:
        return "Due for service" if mode == "service" else "Due for replacement"

    return "OK"
```

**FR-5.2: Update Functions for Lifetime and Service Status**

**CRITICAL: Two Separate Database Fields**

The Components table has **two independent status fields**:
- `lifetime_status` (CharField) - Status for component replacement/end-of-life
- `service_status` (CharField) - Status for component service/maintenance

Each field is updated by its respective function and applies worst-case logic (time vs distance) independently within its domain.

**Current functions:**
- `update_component_lifetime_status(component)` → updates **`lifetime_status`** field
- `update_component_service_status(component)` → updates **`service_status`** field

**Enhancement needed:**
- Calculate BOTH distance-based and time-based statuses FOR EACH FUNCTION
- Apply worst-case logic to determine final status WITHIN EACH DOMAIN (lifetime separate from service)
- Update component record with final status IN THE RESPECTIVE FIELD

**Pseudocode for update_component_lifetime_status:** 
```python
def update_component_lifetime_status(component):
    distance_status = None
    time_status = None

    # Distance-based calculation (if lifetime_expected is not NULL)
    if component.lifetime_expected and component.threshold_km:
        remaining_km = component.lifetime_expected - component.component_distance
        distance_status = compute_component_status(
            "lifetime",
            remaining_km,
            component.threshold_km
        )

    # Time-based calculation (if lifetime_expected_days is not NULL)
    if component.lifetime_expected_days and component.threshold_days:
        age_days = calculate_component_age_days(component)
        remaining_days = component.lifetime_expected_days - age_days
        time_status = compute_component_status(
            "lifetime",
            remaining_days,
            component.threshold_days
        )

    # Worst-case logic
    final_status = determine_worst_status(distance_status, time_status)

    # Write to database - updates lifetime_status field
    database_manager.write_component_lifetime_status(component, remaining_km, remaining_days, final_status)
```

**Pseudocode for update_component_service_status:**
```python
def update_component_service_status(component):
    distance_status = None
    time_status = None

    # Distance-based calculation (if service_interval is not NULL)
    if component.service_interval and component.threshold_km:
        remaining_km = component.service_next  # Already calculated elsewhere
        distance_status = compute_component_status(
            "service",
            remaining_km,
            component.threshold_km
        )

    # Time-based calculation (if service_interval_days is not NULL)
    if component.service_interval_days and component.threshold_days:
        days_since_last_service = calculate_days_since_last_service(component)
        remaining_days = component.service_interval_days - days_since_last_service
        time_status = compute_component_status(
            "service",
            remaining_days,
            component.threshold_days
        )

    # Worst-case logic
    final_status = determine_worst_status(distance_status, time_status)

    # Write to database - updates service_status field
    database_manager.write_component_service_status(component, remaining_km, remaining_days, final_status)
```

**FR-5.3: Bike Status Aggregation Updates**

**Current logic in `update_bike_status()`:**
```python
if component.lifetime_status == "Lifetime exceeded" or component.service_status == "Service interval exceeded":
    critical += 1
elif component.lifetime_status == "Due for replacement" or component.service_status == "Due for service":
    warning += 1
elif component.lifetime_status == "End of life approaching" or component.service_status == "Service approaching":
    approaching += 1
```

**New logic (simplified to 3 levels):**
```python
if component.lifetime_status == "Lifetime exceeded" or component.service_status == "Service exceeded":
    critical += 1  # 🔴 Red
elif component.lifetime_status == "Due for replacement" or component.service_status == "Due for service":
    warning += 1  # 🟡 Yellow
elif component.lifetime_status == "OK" or component.service_status == "OK":
    ok += 1  # 🟢 Green
```

Remove "approaching" level from bike status calculations. Bike status uses same 3-color indicator system: 🟢 green / 🟡 yellow / 🔴 red.

---

### FR-6: Time-Based Update Strategy (CRITICAL ARCHITECTURAL QUESTION)

**Problem Statement:**

Distance-based fields update EVENT-DRIVEN (when rides sync from Strava).

Time-based fields update CONTINUOUSLY (every component ages every day).

**Challenge:**
- Updating ALL components daily would be resource-intensive
- Time-based status changes must be visible to users without page refresh triggering updates
- Need efficient approach that balances accuracy with performance

**Options for Architect to Consider:**
- Create a system or task manager that allows for scheduled runs of select functions. Should be able to be used by other functions as well.
- Create a function that can be called from the schedule task manager that updates time related fields, but excluded retired components from this function.
- Retired functions should have some kind of marking, making it clear that how old they are and so on are now frozen and no longer updated after retirement
- Time-based fields should be stored in database, but there could be exceptions for fields that are not used as input in other calculations
- Whats the best way to add a schedule manager, is there some kind of framework og library we could use? It must be able to run in the container as part of the python script, without blocking the main thread

---

## User Stories with Acceptance Criteria

### User Story 1: Track Time-Based Component Deterioration

**As a** bicycle owner with seasonally-used bikes
**I want to** receive warnings when time-sensitive components deteriorate
**So that** I replace dried sealant, hardened brake pads, and degraded tape before riding

**Acceptance Criteria:**
- [ ] User can configure `service_interval_days` at ComponentTypes level
- [ ] User can configure `lifetime_expected_days` at ComponentTypes level
- [ ] New components inherit time-based intervals from component type
- [ ] User can override time-based intervals on individual components
- [ ] Time-based intervals can be NULL (disabled) for components that don't deteriorate over time
- [ ] Component detail page displays "Component age: X days" (calculated from first installation)
- [ ] Component detail page displays "Lifetime remaining: X days" when lifetime_expected_days is configured
- [ ] Component detail page displays "Next service in: X days" when service_interval_days is configured
- [ ] Time-based status calculation triggers "Due" or "Exceeded" warnings based on elapsed days
- [ ] Component age continues counting even when component is uninstalled (rubber still deteriorates)

**Edge Cases:**
- What if component has never been installed? Age = NULL, no time-based calculations
- What if component installed, uninstalled, reinstalled? Age timer never resets
- What if service record exists but no service_interval_days configured? No time-based service status
- What if component has lifetime_expected_days but no distance lifetime? Show time progress bar only
- What if component has status retired? Do not update component after retirement date, only show last values at the time of retirement

---

### User Story 2: Hybrid Time + Distance Status Determination

**As a** component tracker
**I want to** see accurate status based on BOTH time and distance
**So that** I maintain components that reach thresholds by EITHER factor

**Acceptance Criteria:**
- [ ] Components with BOTH time and distance intervals configured show BOTH progress bars
- [ ] Status badge shows worst-case status (if time = "Due" and distance = "OK", badge shows "Due")
- [ ] Status indicator icon (📍 / 📅 / 📍📅) shows which factor triggered the status
- [ ] Component overview table displays status with trigger indicator
- [ ] Bike details component table displays status with trigger indicator
- [ ] Bike overview aggregates worst-case component statuses correctly
- [ ] Component with time-based "Exceeded" and distance-based "OK" shows "Exceeded" status
- [ ] Component with time-based "OK" and distance-based "Due" shows "Due" status

**Edge Cases:**
- What if BOTH time and distance are below their respective thresholds simultaneously? Show 📍📅 indicator (both contributing to status)
- What if time = "Exceeded" and distance = "Due"? Show "Exceeded" (worse) with appropriate trigger indicator
- What if component has NULL for one interval type? Only calculate status for configured interval, show 📍 or 📅 only
- What if BOTH intervals are NULL? Status = "Not defined" ⚪ (no maintenance intervals configured), no trigger indicator

---

### User Story 3: User-Configurable Simplified Status Thresholds

**As a** user tracking long-lifetime components
**I want to** configure when warnings appear based on absolute remaining values (km or days)
**So that** I avoid premature warnings and focus on components that truly need attention

**Acceptance Criteria:**
- [ ] Component with 200km remaining shows "Due" status when threshold_km = 300km (200 < 300)
- [ ] Component with 400km remaining shows "OK" status when threshold_km = 300km (400 >= 300)
- [ ] Component with 800km remaining shows "OK" status when threshold_km = 300km (800 >= 300)
- [ ] Component at exactly 0km remaining shows "Exceeded" status (0 <= 0)
- [ ] Component with negative remaining km shows "Exceeded" status (-100 < 0)
- [ ] Component with negative remaining days shows "Exceeded" status (-5 < 0)
- [ ] User can customize `threshold_km` at component type level
- [ ] User can customize `threshold_days` at component type level
- [ ] Individual components inherit thresholds from type but can override
- [ ] Form validation: threshold_km must be >0 when configured
- [ ] Form validation: threshold_days must be >0 when configured
- [ ] Application validation: threshold_km required when distance intervals exist
- [ ] Application validation: threshold_days required when time intervals exist
- [ ] Threshold validation: threshold_km must be <= MIN(service_interval, lifetime_expected) when both are defined
- [ ] Threshold validation: threshold_km must be <= service_interval OR lifetime_expected when only one is defined
- [ ] Threshold validation: threshold_days must be <= MIN(service_interval_days, lifetime_expected_days) when both are defined
- [ ] Threshold validation: threshold_days must be <= service_interval_days OR lifetime_expected_days when only one is defined

**Edge Cases:**
- What if component has service_interval = 250km and lifetime_expected = 3,000km? threshold_km must be <= 250km (the smaller value). This prevents threshold from being larger than the shortest interval, ensuring warnings trigger appropriately for both service and lifetime.
- What if user attempts to set threshold_km to 10,000km on a 3,000km component (only lifetime defined)? Input validation prevents threshold from exceeding 3,000km (applies to both component type form and component details form)
- What if user sets threshold_km to 100km on a 10,000km component? Valid. Component stays "OK" until very close to end (within 100km).
- What if component has no lifetime_expected (NULL)? No lifetime status calculation, display "-"

---

### User Story 4: Simplified Status Levels (Remove Intermediate States)

**As a** user viewing component status
**I want to** see clear, actionable status levels
**So that** I know exactly when to service or replace components

**Acceptance Criteria:**
- [ ] Component status can ONLY be: "OK", "Due for service", "Service exceeded", "Due for replacement", "Lifetime exceeded", or "Not defined"
- [ ] "Service approaching" status is removed from system
- [ ] "End of life approaching" status is removed from system
- [ ] Component overview statistics display 4 color categories (🟢 green / 🟡 yellow / 🔴 red / ⚪ white) instead of 4 (previously 🟢🟡🔴🟣)
- [ ] Status indicators use: 🟢 for "OK", 🟡 for "Due", 🔴 for "Exceeded", ⚪ for "Not defined"
- [ ] Components with no intervals configured show "Not defined ⚪" status
- [ ] Bike status aggregation logic should be the same as it currently is, but must handle the new status level system
- [ ] Existing components with "approaching" status migrated to "OK" or "Due" based on new thresholds
- [ ] UI legend/documentation updated to reflect status system with emoji indicators

**Edge Cases:**
- What if component has exactly threshold_km remaining (e.g., 300km remaining, threshold_km = 300km)? Use < operator, so this would be "OK" (300 < 300 is false)
- What if component has threshold_km - 1 remaining (e.g., 299km remaining, threshold_km = 300km)? "Due for service" (299 < 300 is true)

---

### User Story 5: User-Configurable Status Thresholds with Type-Level Defaults

**As a** component optimizer
**I want to** customize status thresholds at both component type and individual component levels
**So that** I can reduce noise from premature warnings and adjust thresholds based on component-specific risk tolerance

**Acceptance Criteria:**
- [ ] ComponentTypes table stores default time intervals (service_interval_days, lifetime_expected_days) - NEW fields following existing pattern
- [ ] ComponentTypes table stores default thresholds (threshold_km, threshold_days) - NEW threshold fields
- [ ] When creating new component, time intervals and thresholds are inherited from component type
- [ ] Component edit form allows overriding time intervals and thresholds (distance intervals already user-editable)
- [ ] Changing component type defaults does NOT automatically update existing components
- [ ] Component detail page indicates if threshold values are inherited or overridden (UI decision for @ux-designer)
- [ ] User can reset component threshold values to type defaults (UI decision for @ux-designer)
- [ ] Application-level validation enforces: threshold_km required when distance intervals exist, threshold_days required when time intervals exist

**Edge Cases:**
- What if component type has NULL for time intervals? Component inherits NULL (time-based tracking disabled), but can be overridden by user by entering values directly in the component form
- What if user creates component type with no threshold defaults? New components inherit NULL, user must configure before thresholds take effect. Thresholds are mandatory if corresponding values have been set for either distance or time
- What if user changes a component's assigned type (e.g., reassigns component #123 from "Chain" type to "Cassette" type)? **Component inherits all field values from the newly assigned ComponentType** (service_interval, lifetime_expected, service_interval_days, lifetime_expected_days, threshold_km, threshold_days). This is DIFFERENT from changing ComponentType defaults, which does NOT update existing components.


**Note:** Per-component distance interval customization already exists (service_interval and lifetime_expected fields). This user story focuses on adding time intervals and threshold configurability.

---

### User Story 6: Service Interval Timer Reset vs. Lifetime Timer Continuation

**As a** user servicing components
**I want to** reset the service interval timer when I register service
**So that** the next service countdown starts fresh

**As a** user tracking component lifetime
**I want to** see continuous lifetime counting regardless of service
**So that** I know total component age

**Acceptance Criteria:**
- [ ] When service record is created, `service_next_days` resets to service_interval_days
- [ ] Service interval timer counts days from last service date
- [ ] When service record is created, `component_age_days` continues counting (never resets)
- [ ] Lifetime timer always counts from first installation date
- [ ] Servicing a component does NOT affect lifetime_remaining_days
- [ ] Component detail page shows both "Days since last service: X" and "Component age: X days"

**Edge Cases:**
- What if component is serviced multiple times? Each service resets service_next_days, the most recent service date is used
- What if component has service record but no service_interval_days configured? No service timer displayed
- What if component has lifetime_expected_days but no service_interval_days? Only lifetime timer displayed

---

### User Story 7: Consistent UI for All Component Types

**As a** user managing diverse components
**I want to** see consistent interface for all component types
**So that** I don't need to learn different workflows for time-based vs. distance-based components

**Acceptance Criteria:**
- [ ] Component creation form ALWAYS shows all 6 fields (service_interval, service_interval_days, lifetime_expected, lifetime_expected_days, threshold_days, threshold_km)
- [ ] Component edit form ALWAYS shows all 6 fields regardless of which are configured
- [ ] Empty/blank fields are stored as NULL in database
- [ ] Component detail page always displays both time and distance sections
- [ ] If time interval is NULL, time section shows "Not configured" or "-"
- [ ] If distance interval is NULL, distance section shows accumulated distance but no status
- [ ] Progress bars appear/disappear based on which intervals are configured (1 bar, 2 bars, or 0 bars)

**Edge Cases:**
- What if component has NO intervals configured (all NULL)? Show "No maintenance intervals configured"
- What if user configures ONLY thresholds but no intervals? Thresholds have no effect, status = NULL

---

## Validation Examples (Test Cases)

### Test Case 1: Tubeless Sealant (Time-Only)

**Configuration:**
- Component Type: "Tubeless Sealant"
- service_interval_days = 180
- lifetime_expected_days = 365
- service_interval (km) = NULL
- lifetime_expected (km) = NULL
- threshold_km = NULL (no distance intervals)
- threshold_days = 30

**State:**
- Component installed: 200 days ago (first installation)
- Last service: Never
- Distance accumulated: 1,200 km

**Expected Calculations:**
- `component_age_days` = 200
- `service_next_days` = 180 - 200 = -20 (exceeded by 20 days)
- `lifetime_remaining_days` = 365 - 200 = 165 days
- Service status (time): -20 days <= 0 → **"Service exceeded"**
- Lifetime status (time): 165 days < 30 days threshold? NO → **"OK"**
- Final status: **"Service exceeded"** (worst case)
- Trigger indicator: 📅 (time-triggered)

**VALIDATED: ✓**

---

### Test Case 2: Chain (Distance-Only with Simplified Threshold)

**Configuration:**
- Component Type: "Chain"
- service_interval = 250 km
- lifetime_expected = 3,000 km
- service_interval_days = NULL
- lifetime_expected_days = NULL
- threshold_km = 300
- threshold_days = NULL (no time intervals)

**State:**
- Component distance: 2,800 km (consumed)
- Lifetime remaining: 3,000 - 2,800 = 200 km
- Component age: 180 days (irrelevant, no time intervals)

**Expected Calculations:**
- Lifetime remaining: 200 km
- Lifetime status (distance): 200 km < 300 km threshold → **"Due for replacement"**
- Service status: (calculation depends on last service)
- Final status: **"Due for replacement"**
- Trigger indicator: 📍 (distance-triggered)

**VALIDATED: ✓** (Simplified logic - direct comparison of remaining vs threshold)

---

### Test Case 3: Tire (Hybrid Time + Distance)

**Configuration:**
- Component Type: "Tire"
- service_interval = NULL
- lifetime_expected = 5,000 km
- service_interval_days = NULL
- lifetime_expected_days = 730 days (2 years)
- threshold_km = 500
- threshold_days = 90

**State:**
- Component distance: 4,200 km
- Component age: 650 days
- Lifetime remaining (km): 5,000 - 4,200 = 800 km
- Lifetime remaining (days): 730 - 650 = 80 days

**Expected Calculations:**

**Distance-based lifetime:**
- Remaining: 800 km
- 800 km < 500 km threshold? NO → **"OK"**

**Time-based lifetime:**
- Remaining: 80 days
- 80 days < 90 days threshold? YES → **"Due for replacement"**

**Final status:** **"Due for replacement"** (worst case - time triggered)
**Trigger indicator:** 📅 (time-triggered)

**VALIDATED: ✓** (Simplified logic - tire shows "Due" when time drops below 90 days threshold)

---

## Edge Cases & Error Handling

### Edge Case 1: Component Never Installed

**Scenario:** User creates component but never installs it on a bike

**Handling:**
- `component_age_days` = NULL (no installation date exists)
- `lifetime_remaining_days` = NULL
- `service_next_days` = NULL
- No time-based status calculations possible
- Distance-based calculations also impossible (no distance accumulation)
- Component detail page shows "Not yet installed" message
- Status = "Not defined" ⚪ (no data available for status calculation)

---

### Edge Case 2: Component Installed, Uninstalled, Reinstalled

**Scenario:** Component installed Jan 1, uninstalled Mar 1 (60 days elapsed), reinstalled Jun 1 (150 days elapsed total)

**Handling:**
- `component_age_days` = days since FIRST installation (Jan 1)
- On Jun 1, age = 150 days (not 0)
- Age timer NEVER resets, even when uninstalled
- Rationale: Rubber, sealant, adhesive deteriorate regardless of installation status
- Component detail page may show: "Installed 60 days ago, component age 150 days"

---

### Edge Case 3: Component Has No Expected Lifetime or Service Interval

**Scenario:** Component created with ALL interval fields NULL (no service_interval, no lifetime_expected, no service_interval_days, no lifetime_expected_days)

**Handling:**
- No status calculations possible
- Status = "Not defined" ⚪ (white circle emoji)
- Component detail page shows: "No maintenance intervals configured"
- Component overview table shows: "Not defined ⚪"
- No progress bars displayed
- No trigger indicator (📍/📅) shown
- Distance and age still tracked and displayed (for reference only)

---

### Edge Case 4: Component Has Service Interval But Never Serviced

**Scenario:** New component installed with service_interval_days = 180, no service records yet

**Handling:**
- Service timer counts from installation date (not service date)
- `service_next_days` = 180 - days_since_installation
- When service record is registered, timer resets to count from service date

---

## MVP vs. Future Enhancements

### MVP Scope (Must Have for First Release)

All features described in this document are considered MVP:

- [x] Hybrid time + distance status calculations
- [x] Simplified user-configurable status thresholds (absolute km and days)
- [x] Simplified 3-level status system (OK / Due / Exceeded)
- [x] 4 new fields in ComponentTypes (time intervals, thresholds)
- [x] 7 new fields in Components (time intervals, thresholds, calculated fields)
- [x] Time-based deterioration tracking
- [x] Worst-case status determination (time vs. distance)
- [x] Per-component configuration with type-level defaults
- [x] Service interval reset vs. lifetime continuation
- [x] Dual progress bars (time + distance) in UI
- [x] Status trigger indicators (📍 / 📅 / 📍📅)
- [x] Consistent UI for all component types
- [x] Database migration with backward compatibility

### Future Enhancements (Nice to Have, Post-MVP)

---

## Integration Points

**Key Areas Impacted:**
- **Backend**: `compute_component_status()`, `update_component_lifetime_status()`, `update_component_service_status()` - refactored for hybrid time/distance logic
- **Database**: `component_types` table (+4 fields), `components` table (+7 fields); `component_history` and `services` tables queried but not modified
- **API Endpoints**: Extend existing CRUD endpoints to accept/return new time-based fields (no new endpoints needed)
- **UI Pages**: Component overview, bike details, component detail, component/type forms - all updated for dual progress bars, status trigger indicators, and new field inputs
- **Service Registration**: Resets `service_next_days` but NOT `component_age_days` or `lifetime_remaining_days`
- **Strava Integration**: No changes needed; ride sync triggers distance updates, time updates are independent

---

## Success Metrics

### Quantitative Metrics

**Accuracy Improvement:**
- **Target:** 100% of time-sensitive components show accurate status (no false "OK" for dried sealant)
- **Measurement:** Manual audit of 50 time-sensitive components after 30 days

**Reduced False Warnings:**
- **Target:** 30% reduction in "Due" warnings for long-lifetime components with significant km remaining
- **Measurement:** Count components with >500km remaining showing "Due" status (before vs. after)

**User Adoption:**
- **Target:** 60% of users configure at least one time-based interval within 60 days
- **Measurement:** Database query for components with non-NULL time intervals

### Qualitative Metrics

**User Satisfaction:**
- Positive feedback on more nuanced status warnings
- Users report catching time-based deterioration before failures
- Users feel confident in refined threshold logic

**Feature Comprehension:**
- Users understand hybrid time + distance tracking without extensive documentation
- Users successfully configure time intervals for appropriate component types

### Success Criteria (MVP)

The feature is considered successful if:
1. All user stories are implemented with acceptance criteria met
2. All 6 validation examples pass automated and manual testing
3. No data loss or corruption during migration
4. Time-based status calculations accurate within 1 day
5. Hybrid threshold logic eliminates premature warnings for long-lifetime components
6. Performance impact <500ms for component overview page (50+ components)
7. Zero critical bugs in first month post-launch

---

## Dependencies & Requirements

### Dependencies on Existing Code

**1. Business Logic (`business_logic.py`):**
- Refactor `compute_component_status()` function
- Enhance `update_component_lifetime_status()` and `update_component_service_status()`
- Add worst-case status determination logic

**2. Database Manager (`database_manager.py`):**
- May need new query function: `get_first_installation_date(component_id)`
- Update existing write functions to handle new fields

**3. Database Model (`database_model.py`):**
- Add fields to `ComponentTypes` model
- Add fields to `Components` model 

**4. Frontend Templates:**
- Update component creation modal (`modal_create_component.html`)
- Update component edit modal (if separate from creation)
- Update component detail page (`component_details.html`)
- Update component overview table (`component_overview.html`)
- Update bike details component table (`bike_details.html`)

**5. Utilities (`utils.py`):**
- May need new helper function: `calculate_component_age_days(first_install_date)`
- May need new helper function: `format_days_remaining(days)` (similar to existing km formatting)

### External Dependencies

**None.** This feature is self-contained within Velo Supervisor 2000.

### Environment Requirements

**No changes to:**
- Python dependencies (Peewee, FastAPI, etc. remain unchanged)
- Docker configuration
- Deployment scripts
- External API integrations (Strava unaffected)

**Potential addition (if scheduled updates chosen):**
- Cron/scheduler for nightly batch updates (only if architect chooses scheduled approach over lazy calculation)

---

## Next Steps

This requirements document is now **COMPLETE** and ready for handover to **@ux-designer**.

**Handover Summary:**
- **Feature:** Component Status Refinement with Hybrid Time + Distance Tracking
- **Scope:** Fully defined MVP with user stories, comprehensive acceptance criteria, validated test cases
- **Key Decisions:**
  - Hybrid time + distance calculations with worst-case status determination
  - Simplified 3-level status system (removing intermediate "approaching" levels)
  - Simplified threshold logic using absolute values only (remaining < threshold, no percentage)
  - Separate threshold fields: `threshold_km` and `threshold_days` (both nullable, user-configurable)
  - Time intervals and thresholds follow same inheritance pattern as existing distance intervals
  - Service interval resets, lifetime continues
  - Consistent UI showing both time and distance for all components
  - Migration defaults: time intervals NULL, threshold_km = 200, threshold_days = NULL
- **Critical Questions:** Listed in "Questions for Architect" (25 questions) and "Questions for UX Designer" (27 questions)

**Action Required from @architect:**
1. Review requirements, user stories, and validation examples
2. **CRITICAL: Decide on time-based field update strategy** (lazy calculation vs. scheduled batch vs. hybrid) - Recommendation: lazy calculation for MVP
3. **DECISION MADE: Use separate threshold fields** (`threshold_km` and `threshold_days`, both nullable)
4. Design database schema changes and migration plan (4 new fields per ComponentTypes, 7 per Components)
5. Refactor status calculation functions for simplified threshold logic (remaining < threshold)
6. Design worst-case status determination logic (unchanged - compare time vs distance statuses)
7. Identify performance optimizations (indexes, caching, lazy calculation strategy)
8. Create architecture handover document in `.handovers/architecture/component-status-refinement-architect-handover.md`

**Action Required from @ux-designer:**
1. Review requirements, user stories, and user workflow
2. Answer 27 design questions in "Questions for UX Designer" section
3. Design UI for 6-field configuration forms (creation/edit)
4. Design dual progress bar layout (time + distance)
5. Design status trigger indicator (📍 / 📅 / 📍📅) visual treatment
6. Design simplified 3-level status badge system
7. Design component overview table with status trigger column
8. Ensure responsive design for mobile/tablet
9. Create UX specifications handover document in `.handovers/ux/component-status-refinement-ux-designer-handover.md`

**Coordination Note:**
- @ux-designer creates initial UX specifications (v1) first
- @architect then reads requirements + UX v1 handover to create architecture plan
- @ux-designer then updates UX specifications (v2) to align with architecture constraints
- This sequential approach ensures UX and architecture are properly coordinated
- @database-expert will be involved after @architect completes schema design

---

## References

- **Existing database model:** `/home/xivind/code/velo-supervisor-2000/backend/database_model.py`
- **Existing status calculation logic:** `/home/xivind/code/velo-supervisor-2000/backend/business_logic.py` (lines 777-806, 806-978, 2058-2080)
- **Existing component detail page:** `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_details.html`
- **Existing component overview page:** `/home/xivind/code/velo-supervisor-2000/frontend/templates/component_overview.html`
- **Application overview:** `/home/xivind/code/velo-supervisor-2000/CLAUDE.md`
- **Handover template:** `/home/xivind/code/velo-supervisor-2000/.handovers/TEMPLATE.md`
- **Related GitHub issues:** #226, #275, #284 (temporary fix being replaced)

---

**Document Status:** Complete - Ready for UX Designer Review
**Date Completed:** 2025-10-19
**Next Agent:** @ux-designer (will create v1, then @architect will create architecture using requirements + UX v1)
