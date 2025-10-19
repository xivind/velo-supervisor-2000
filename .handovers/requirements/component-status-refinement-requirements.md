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
3. **Simplified Status Levels**: Removing "Service approaching" / "End of life approaching" intermediate states (3-level system: OK / Due / Exceeded)
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
> **Desired behavior:** "OK" status because 200km >= 300km threshold (user-configured) → Stays "OK" until closer to end.

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

Replace current 4-level status system with 3 levels:

**Previous System:**
- "OK" (0-70%)
- "Service approaching" / "End of life approaching" (70-90%)
- "Due for service" / "Due for replacement" (90-100%)
- "Service interval exceeded" / "Lifetime exceeded" (>100%)

**New System:**
- **"OK"** (Healthy, no action needed)
- **"Due for service"** / **"Due for replacement"** (Action recommended soon)
- **"Service exceeded"** / **"Lifetime exceeded"** (Action overdue)

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
- Same threshold used for BOTH service and lifetime calculations (one `threshold_km` for both distance-based service AND lifetime)

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

**Example:**
- Distance-based: 1,500km remaining, threshold_km = 500km → "OK" (1,500 >= 500)
- Time-based: 15 days remaining, threshold_days = 30 days → "Due for replacement" (15 < 30)
- **Final: "Due for replacement"** (time-based is worse)

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

**Note on calculated fields:**
- These may be stored in database OR calculated on-the-fly (architect to decide based on performance)
- If stored: must be updated when time passes (requires update strategy)
- If calculated: no storage, computed during query (may impact performance)

**FR-3.3: Validation Rules (Application-Level)**

While database fields are nullable for flexibility, application-level validation enforces:
- If component has `service_interval` OR `lifetime_expected` (any distance interval) → `threshold_km` is **REQUIRED**
- If component has `service_interval_days` OR `lifetime_expected_days` (any time interval) → `threshold_days` is **REQUIRED**
- Threshold values must be > 0 when configured

**FR-3.4: Migration Strategy (Backward Compatibility)**

**Existing components during migration:**
- Set all new fields as follows:
  - `service_interval_days` → NULL (no time intervals exist currently)
  - `lifetime_expected_days` → NULL (no time intervals exist currently)
  - `threshold_km` → 200 (all existing components have distance intervals, so this is required)
  - `threshold_days` → NULL (no time intervals exist yet, so not needed)
- User can configure time intervals as needed post-migration
- No automatic population of time intervals (ensures data quality and user control)

**Default behavior for new components (post-migration):**
- Inherit NULL for time intervals (user opts in by configuring ComponentType)
- Inherit threshold values from ComponentType (user configures sensible defaults per type)

**Status calculations during transition:**
- Components with NULL time intervals → distance-only calculations (existing behavior preserved)
- Components with configured time intervals → hybrid time + distance calculations (new behavior)

---

### FR-4: Status Display & UI Updates

**FR-4.1: Status Badge with Trigger Indicator**

**Single "Status" column** in component tables shows worst case of time vs. distance.

**Visual indicator (icon/badge) showing which factor triggered status:**

| Icon | Meaning | Example |
|------|---------|---------|
| 📍 | Distance-triggered | Distance reached "Due" threshold, time is OK |
| 📅 | Time-triggered | Time reached "Due" threshold, distance is OK |
| 📍📅 | Both triggered | Both time AND distance at same status level |

**Example display:**
- "Due for replacement 📅" (time-triggered)
- "Service exceeded 📍" (distance-triggered)
- "Due for replacement 📍📅" (both at "Due" level)

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
- Color coding (green/yellow/red based on status)

**FR-4.3: Days Remaining Display**

**Display format (consistent with existing km remaining format):**
- "Lifetime remaining: 78 days" (or "Lifetime reached in 78 days")
- "Service next: 45 days" (or "Next service in 45 days")
- Negative values: "Lifetime exceeded by 15 days"

**FR-4.4: Component Creation/Edit Forms**

**Always show BOTH time AND distance fields:**
- Service Interval (km): [____] km
- Service Interval (days): [____] days
- Lifetime Expected (km): [____] km
- Lifetime Expected (days): [____] days
- Status Threshold (%): [90] % (default 90, editable)
- Status Threshold (km): [500] km (default 500, editable)

**Behavior:**
- Empty/blank field → stored as NULL in database
- User can leave any combination blank
- Consistent interface regardless of component type

**Form validation:**
- Threshold km: >0 (when distance intervals configured)
- Threshold days: >0 (when time intervals configured)
- Time/distance intervals: NULL or >0

**FR-4.5: Component Type Management Forms**

Same field layout as component forms, but:
- Fields represent defaults for new components of this type
- Existing components NOT automatically updated when type defaults change
- User must manually update components if desired

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
def compute_component_status(mode, remaining_value, threshold_value):
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

**Current functions:**
- `update_component_lifetime_status(component)`
- `update_component_service_status(component)`

**Enhancement needed:**
- Calculate BOTH distance-based and time-based statuses
- Apply worst-case logic to determine final status
- Update component record with final status

**Pseudocode:**
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

    # Write to database
    database_manager.write_component_lifetime_status(component, remaining_km, remaining_days, final_status)
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
    critical += 1
elif component.lifetime_status == "Due for replacement" or component.service_status == "Due for service":
    warning += 1
elif component.lifetime_status == "OK" or component.service_status == "OK":
    ok += 1
```

Remove "approaching" level from bike status calculations.

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

**Option A: Lazy Calculation (On-Demand)**
- Time-based fields calculated during query/display
- No stored values for `component_age_days`, `lifetime_remaining_days`, `service_next_days`
- Pro: No scheduled tasks, always accurate
- Con: Calculation overhead on EVERY component view

**Option B: Scheduled Batch Update**
- Nightly cron job updates all components' time-based fields
- Pro: Pre-computed, fast queries
- Con: Stale data (up to 24 hours old), requires scheduling infrastructure

**Option C: Hybrid Lazy + Cached**
- Calculate on first access each day, cache until next day
- Store `last_time_calculation_date` per component
- Pro: Balance of accuracy and performance
- Con: More complex logic

**Option D: User-Triggered Refresh**
- Time-based fields updated when user views component or bike page
- "Last updated: 2 hours ago" indicator
- Pro: User-controlled, no background tasks
- Con: May feel stale if user doesn't refresh frequently

**Questions for @architect:**
1. Which approach best fits the existing application architecture?
2. Are there performance implications for lazy calculation across 100+ components?
3. Should time-based fields be stored in database or calculated on-the-fly?
4. How to handle staleness in component overview pages (showing 50+ components)?
5. Is there existing infrastructure for scheduled tasks (cron, celery, etc.)?

---

### FR-7: Status Threshold Configuration (CRITICAL DESIGN QUESTION)

**Question for @architect:**

Should we use SEPARATE threshold fields for time vs. distance, or SHARED threshold field?

**Option A: Shared Threshold (Current Proposal)**
- Single `status_threshold_percentage` field (e.g., 90%)
- Applied to BOTH time and distance calculations
- Single `status_threshold_km` field (e.g., 500km)
- **Question: How to interpret "500km" threshold for time-based status?**
  - Convert to days based on interval? (e.g., 500 days if lifetime is 3650 days)
  - Use percentage only for time, absolute only for distance?

**Option B: Separate Thresholds**
- `status_threshold_percentage` (shared, used for both)
- `status_threshold_km` (distance only)
- `status_threshold_days` (time only)
- Example: 90% AND <500km for distance, 90% AND <30 days for time
- Pro: Maximum flexibility
- Con: More fields, more complexity

**Example to clarify:**

Component with 365 day lifetime:
- Current age: 328 days (89.8%, 37 days remaining)
- Threshold: 90%

**Using shared percentage + absolute km threshold:**
- Percentage check: 89.8% > 90% (FALSE)
- Absolute check: 37 days < ??? (Need threshold in days)
- **How to define absolute day threshold?**

**Proposed resolution:**
- Use `status_threshold_percentage` for BOTH time and distance (shared)
- Use `status_threshold_km` for distance calculations ONLY
- Add `status_threshold_days` for time calculations ONLY
- Default `status_threshold_days` = 30 days (similar logic to 500km)

**Architect to decide:**
- Is separate threshold necessary?
- Or can we derive day threshold from percentage alone (e.g., 90% of 365 days = 328 days → threshold is "remaining < 37 days")?

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

**Out of Scope (Future Enhancements):**
- Automatic notifications when components reach time-based thresholds
- Pausing time-based aging when bike is marked as "in storage"
- Different deterioration rates for different storage conditions

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
- What if BOTH time and distance are at "Due" level simultaneously? Show 📍📅 indicator
- What if time = "Exceeded" and distance = "Due"? Show "Exceeded" (worse)
- What if component has NULL for one interval type? Only calculate status for configured interval
- What if BOTH intervals are NULL? Status = NULL (no maintenance defined)

**Out of Scope (Future Enhancements):**
- Configurable weighting (e.g., prioritize time over distance)
- Separate status badges for time vs. distance (showing both simultaneously)

---

### User Story 3: User-Configurable Simplified Status Thresholds

**As a** user tracking long-lifetime components
**I want to** configure when warnings appear based on absolute remaining values (km or days)
**So that** I avoid premature warnings and focus on components that truly need attention

**Acceptance Criteria:**
- [ ] Component with 200km remaining shows "OK" status when threshold_km = 300km (200 >= 300 is false, so not "Due")
- [ ] Component with 200km remaining shows "Due" status when threshold_km = 300km (200 < 300)
- [ ] Component with 800km remaining shows "OK" status when threshold_km = 300km (800 >= 300)
- [ ] Component at exactly 0km remaining shows "Exceeded" status (0 <= 0)
- [ ] Component with negative remaining km shows "Exceeded" status (-100 < 0)
- [ ] User can customize `threshold_km` at component type level
- [ ] User can customize `threshold_days` at component type level
- [ ] Individual components inherit thresholds from type but can override
- [ ] Form validation: threshold_km must be >0 when configured
- [ ] Form validation: threshold_days must be >0 when configured
- [ ] Application validation: threshold_km required when distance intervals exist
- [ ] Application validation: threshold_days required when time intervals exist

**Edge Cases:**
- What if user sets threshold_km to 10,000km on a 3,000km component? Component shows "Due" immediately when created (remaining 3,000 < 10,000)
- What if user sets threshold_km to 100km on a 10,000km component? Component stays "OK" until very close to end
- What if component has no lifetime_expected (NULL)? No status calculation, display "-"

**Out of Scope (Future Enhancements):**
- Different thresholds for service vs. lifetime (currently uses same threshold for both)
- Dynamic thresholds based on component health or service history
- Threshold recommendations based on component type

---

### User Story 4: Simplified Status Levels (Remove Intermediate States)

**As a** user viewing component status
**I want to** see clear, actionable status levels
**So that** I know exactly when to service or replace components

**Acceptance Criteria:**
- [ ] Component status can ONLY be: "OK", "Due for service", "Service exceeded", "Due for replacement", "Lifetime exceeded", or NULL
- [ ] "Service approaching" status is removed from system
- [ ] "End of life approaching" status is removed from system
- [ ] Component overview statistics display 3 color categories (green/yellow/red) instead of 4
- [ ] Bike status aggregation logic updated to reflect 3 levels (OK / Warning / Critical)
- [ ] Existing components with "approaching" status migrated to "OK" or "Due" based on new thresholds
- [ ] UI legend/documentation updated to reflect 3-level system

**Edge Cases:**
- What if component has exactly threshold_km remaining (e.g., 300km remaining, threshold_km = 300km)? Use < operator, so this would be "OK" (300 < 300 is false)
- What if component has threshold_km - 1 remaining (e.g., 299km remaining, threshold_km = 300km)? "Due for service" (299 < 300 is true)

**Out of Scope (Future Enhancements):**
- User-configurable status level names (e.g., "Needs attention" instead of "Due for service")
- More granular status levels (5+ levels)

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
- What if component type has NULL for time intervals? Component inherits NULL (time-based tracking disabled)
- What if user creates component type with no threshold defaults? New components inherit NULL, user must configure before thresholds take effect
- What if user changes component type of existing component? Threshold and time interval values are NOT automatically updated (preserve user customizations)

**Out of Scope (Future Enhancements):**
- Bulk update all components to match type defaults
- Templates for common component configurations
- Import/export component configurations

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
- What if component is serviced multiple times? Each service resets service_next_days
- What if component has service record but no service_interval_days configured? No service timer displayed
- What if component has lifetime_expected_days but no service_interval_days? Only lifetime timer displayed

**Out of Scope (Future Enhancements):**
- Resetting lifetime timer (components are never "reborn")
- Manual adjustment of component age

---

### User Story 7: Consistent UI for All Component Types

**As a** user managing diverse components
**I want to** see consistent interface for all component types
**So that** I don't need to learn different workflows for time-based vs. distance-based components

**Acceptance Criteria:**
- [ ] Component creation form ALWAYS shows all 6 fields (service_interval, service_interval_days, lifetime_expected, lifetime_expected_days, threshold_%, threshold_km)
- [ ] Component edit form ALWAYS shows all 6 fields regardless of which are configured
- [ ] Empty/blank fields are stored as NULL in database
- [ ] Component detail page always displays both time and distance sections
- [ ] If time interval is NULL, time section shows "Not configured" or "-"
- [ ] If distance interval is NULL, distance section shows accumulated distance but no status
- [ ] Progress bars appear/disappear based on which intervals are configured (1 bar, 2 bars, or 0 bars)

**Edge Cases:**
- What if component has NO intervals configured (all NULL)? Show "No maintenance intervals configured"
- What if user configures ONLY thresholds but no intervals? Thresholds have no effect, status = NULL

**Out of Scope (Future Enhancements):**
- Adaptive UI that hides irrelevant fields
- Component type templates (e.g., "Sealant Template" pre-populates time fields only)

---

### User Story 8: Migration of Existing Components

**As a** existing Velo Supervisor user
**I want to** preserve my current component data during migration
**So that** I don't lose tracking history

**Acceptance Criteria:**
- [ ] Database migration adds 4 new fields to ComponentTypes table (service_interval_days, lifetime_expected_days, threshold_km, threshold_days - all nullable)
- [ ] Database migration adds 4 new user-editable fields + 3 calculated fields to Components table
- [ ] Existing ComponentTypes: all new fields set to NULL (users configure as needed)
- [ ] Existing Components: time intervals set to NULL, threshold_km = 200, threshold_days = NULL
- [ ] Existing components continue using distance-only status calculations (unchanged behavior)
- [ ] User can gradually add time intervals to component types as needed
- [ ] Existing status badges remain accurate (no regression)

**Edge Cases:**
- What if user has 500+ components? Migration must complete in reasonable time (<5 minutes)
- What if migration fails midway? Rollback mechanism (architect responsibility)
- What if user manually edited database before migration? Validate data integrity before/after

**Out of Scope (Future Enhancements):**
- Automatic population of time intervals based on component type guessing (e.g., "Sealant" → 180 days)
- Migration wizard to guide user through configuring time intervals

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

### Test Case 2: Tubeless Tape (Time-Only, Long Lifetime)

**Configuration:**
- Component Type: "Tubeless Tape"
- service_interval_days = NULL
- lifetime_expected_days = 1095 (3 years)
- service_interval (km) = NULL
- lifetime_expected (km) = NULL
- threshold_km = NULL (no distance intervals)
- threshold_days = 60

**State:**
- Component installed: 912 days ago
- Distance accumulated: 8,000 km

**Expected Calculations:**
- `component_age_days` = 912
- `lifetime_remaining_days` = 1095 - 912 = 183 days
- Lifetime status (time): 183 days < 60 days threshold? NO → **"OK"**
- Service status: NULL (no interval configured)
- Final status: **"OK"**
- Trigger indicator: None (no warning)

**VALIDATED: ✓**

---

### Test Case 3: Chain (Distance-Only with Simplified Threshold)

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

### Test Case 4: Tire (Hybrid Time + Distance)

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

### Test Case 5: Brake Pads at Exactly End of Life

**Configuration:**
- Component Type: "Brake Pads"
- lifetime_expected = 2,500 km
- threshold_km = 250

**State:**
- Component distance: 2,500 km (exactly at lifetime)
- Lifetime remaining: 0 km

**Expected Calculations:**
- Remaining: 0 km
- Exceeded logic: 0 km <= 0 → **"Lifetime exceeded"**

**EDGE CASE:** At exactly 0km remaining, component should show "Lifetime exceeded" (action is overdue).

**Logic:**
```python
if remaining_km <= 0:
    status = "Lifetime exceeded"
```

**VALIDATED: ✓** (Simplified - at 0 remaining shows "Exceeded" status)

---

### Test Case 6: Component with Custom Thresholds

**Configuration:**
- Component Type: "Premium Chain"
- lifetime_expected = 8,000 km
- threshold_km = 1,000 (custom, higher than typical 300km for chains)

**State:**
- Component distance: 7,200 km
- Lifetime remaining: 800 km

**Expected Calculations:**
- Remaining: 800 km
- 800 km < 1,000 km threshold → **"Due for replacement"**

**Compare to smaller threshold (e.g., 300km):**
- With threshold_km = 300: 800 km < 300 km? NO → **"OK"**
- With threshold_km = 1,000: 800 km < 1,000 km? YES → **"Due for replacement"**

**Validation:** Custom thresholds allow earlier warnings for long-lifetime components. Long-lifetime components benefit from higher thresholds.

**VALIDATED: ✓** (Simplified - absolute threshold provides flexibility per component type)

---

## Edge Cases & Error Handling

### Edge Case 1: Component Never Installed

**Scenario:** User creates component but never installs it on a bike

**Handling:**
- `component_age_days` = NULL (no installation date exists)
- `lifetime_remaining_days` = NULL
- `service_next_days` = NULL
- No time-based status calculations
- Distance-based calculations also impossible (no distance accumulation)
- Component detail page shows "Not yet installed" message
- Status = NULL or "Not configured"

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

### Edge Case 3: Service Registered Before Component First Installed

**Scenario:** Data integrity issue - service record exists with date before first installation

**Handling:**
- Backend validation prevents this during service creation
- If exists in database (legacy data), skip service-based calculations
- Display warning: "Service record date invalid (before installation)"
- Suggest user corrects data

---

### Edge Case 4: Component Has No Expected Lifetime or Service Interval

**Scenario:** Component created with ALL interval fields NULL

**Handling:**
- No status calculations possible
- Component detail page shows: "No maintenance intervals configured"
- Component overview table shows "-" for status
- No progress bars displayed
- Distance and age still tracked and displayed (for reference)

---

### Edge Case 5: Separate Threshold Fields for Time vs. Distance

**Design Decision:** Use separate `threshold_km` and `threshold_days` fields (not shared).

**Rationale:**
- Distance thresholds measured in km (e.g., 300km)
- Time thresholds measured in days (e.g., 30 days)
- Different scales require separate configuration
- Simpler logic: remaining < threshold (no percentage calculation needed)

**Example:**
- Component with lifetime_expected_days = 365, threshold_days = 30
- At 340 days (25 days remaining): 25 < 30 → "Due for replacement"
- At 320 days (45 days remaining): 45 >= 30 → "OK"

**Schema:**
- ComponentTypes: `threshold_km`, `threshold_days` (both nullable)
- Components: `threshold_km`, `threshold_days` (both nullable, inherited from type)

---

### Edge Case 6: Negative Remaining Days

**Scenario:** Component installed 400 days ago, lifetime_expected_days = 365

**Handling:**
- `lifetime_remaining_days` = 365 - 400 = -35
- Exceeded logic: -35 <= 0 → **"Lifetime exceeded"**
- Display: "Lifetime exceeded by 35 days"
- No threshold check needed (exceeded is binary)

---

### Edge Case 7: User Changes Component Type After Creation

**Scenario:** User creates component as "Chain", later changes to "Cassette"

**Handling:**
- Component's interval fields are NOT automatically updated
- User must manually update intervals if desired
- Rationale: Preserve user customizations, avoid data loss
- UI may show notification: "Component type changed. Review intervals."

---

### Edge Case 8: Component Type Defaults Changed

**Scenario:** User updates ComponentType "Chain" from 3,000km lifetime to 4,000km

**Handling:**
- Existing components with type "Chain" are NOT automatically updated
- Only newly created "Chain" components inherit 4,000km
- Rationale: Existing components may have custom overrides or different characteristics
- Optional feature for future: "Apply type defaults to all components of this type" button

---

### Edge Case 9: Database Migration Failure Midway

**Scenario:** Migration adds 4 new fields, succeeds for 200 components, fails at component 201

**Handling:**
- Use database transaction for migration (all-or-nothing)
- If any operation fails, ROLLBACK entire migration
- User sees error message with details
- Database remains in pre-migration state
- User can retry migration after investigating

---

### Edge Case 10: Component Has Service Interval But Never Serviced

**Scenario:** New component installed with service_interval_days = 180, no service records yet

**Handling:**
- Service timer counts from installation date (not service date)
- `service_next_days` = 180 - days_since_installation
- When service record is registered, timer resets to count from service date

---

## Questions for UX Designer

The following open-ended questions should guide the UI/UX design for the Component Status Refinement feature:

### General Interface Design

1. **How should the refined 3-level status system (OK / Due / Exceeded) be visually distinguished from the current 4-level system?** What color schemes, badge styles, and iconography will make the simplified system immediately understandable?

2. **How should users configure the 6 new fields (2 time intervals, 2 distance intervals, 2 thresholds) without overwhelming them?** Should fields be grouped, collapsed, or presented with progressive disclosure?

3. **How should the system communicate to users which components use time-based, distance-based, or hybrid tracking?** Should there be visual indicators (icons, badges) in component lists?

### Status Display

4. **How should the status trigger indicator (📍 / 📅 / 📍📅) be presented in component tables?** Should it be inline with status badge, separate column, tooltip, or another pattern?

5. **How should "worst case wins" logic be explained to users?** If distance says "OK" but time says "Due", how do we clarify why the component shows "Due"?

6. **How should components with NULL intervals (no maintenance configured) be displayed?** Should they show "-", "Not configured", greyed out status, or another pattern?

### Progress Bars and Visual Feedback

7. **How should dual progress bars (time + distance) be laid out on component detail pages?** Vertical stack, horizontal side-by-side, tabbed interface, or another pattern?

8. **How should single-interval components (time-only or distance-only) be displayed?** Should empty/unused progress bars be hidden, greyed out, or shown with "Not configured" message?

9. **How should negative remaining values be displayed visually?** When a component shows "Exceeded by 35 days" or "Exceeded by 200km", what color, iconography, or visual treatment emphasizes urgency?

### Component Creation and Editing

10. **How should the component creation form present 6 interval/threshold fields without overwhelming new users?** Should defaults be pre-filled, should fields be collapsible, or should there be a "simple" vs. "advanced" mode?

11. **How should inherited vs. overridden values be visually distinguished in component edit forms?** Should inherited values have a different background color, icon, or label?

12. **How should users reset component-level values back to type defaults?** Button, link, dropdown action, or another pattern?

13. **How should form validation errors for thresholds (e.g., threshold_km must be >0) be displayed?** Inline, at top of form, tooltip, or another pattern?

### Component Type Management

14. **How should ComponentType edit forms communicate that changing defaults won't affect existing components?** Should there be an informational banner, tooltip, or warning message?

15. **How should users apply updated type defaults to existing components (future enhancement)?** What UI pattern would make this safe and clear (e.g., "Apply to 23 existing components" with preview)?

### Component Overview Tables

16. **How should component overview tables accommodate the status trigger indicator column?** Should it be a new column, merged with status column, or shown on hover/tooltip?

17. **How should users filter component tables by status trigger (time-triggered, distance-triggered, both)?** Should there be filter buttons, dropdown, or another pattern?

18. **How should the overview page statistics (count by status) adapt to the 3-level system?** Should there be separate counts for time-triggered vs. distance-triggered warnings?

### Time Display Conventions

19. **How should days remaining be formatted and displayed?** Examples: "45 days", "45d", "1.5 months", "6 weeks" - which convention is most scannable?

20. **How should "days since installation" be distinguished from "days until service"?** Should there be different icons, labels, or positioning?

21. **How should time-based and distance-based remaining values be displayed side-by-side?** Should they use the same format (e.g., "200km remaining" and "30 days remaining"), or different visual treatments?

### Mobile and Responsive Design

22. **How should dual progress bars be adapted for mobile screens?** Should they stack vertically, collapse into summary view, or use another pattern?

23. **How should the 6-field configuration form be optimized for mobile?** Should fields collapse into accordion, use wizard steps, or adapt in another way?

### Warnings and Edge Cases

24. **How should the system communicate when a component's first installation date cannot be determined (no history)?** Warning banner, greyed out time fields, or another pattern?

25. **How should users be notified that time-based fields might be stale (if using lazy calculation)?** "Last updated X hours ago" indicator, refresh button, or another pattern?

### Consistency and Patterns

26. **What visual treatment should clearly communicate the simplified threshold logic (remaining < threshold)?** Should there be tooltips or help text explaining how thresholds work?

27. **How should the "component age continues during uninstall" behavior be communicated?** Should there be tooltips, help text, or visual indicators?

---

## Questions for Architect

The following open-ended questions should guide the technical architecture for the Component Status Refinement feature:

### Database and Schema Design

1. **Should time-based calculated fields (`component_age_days`, `lifetime_remaining_days`, `service_next_days`) be stored in the database or calculated on-the-fly?** What are the performance implications of each approach for 100+ components?

2. **Should we store `threshold_km` and `threshold_days` as separate database fields, or use a single polymorphic threshold field?** Recommendation: separate fields for clarity and type safety.

3. **What database indexes are needed to optimize queries filtering by installation_status, time intervals, and date calculations?** Are composite indexes needed?

4. **How should we handle database migration rollback if the migration fails midway through updating hundreds of components?** Should we use transactions, backup tables, or another safety mechanism?

### Time-Based Update Strategy (CRITICAL)

5. **What is the most efficient approach for updating time-based fields that change daily?**
   - Lazy calculation on query (no storage, always accurate)
   - Scheduled batch update (nightly cron, pre-computed)
   - Hybrid lazy + cached (calculate once per day per component)
   - User-triggered refresh (updates when user views page)

6. **If using scheduled batch updates, what infrastructure is available (cron, celery, background workers)?** How should errors be handled if batch update fails?

7. **If using lazy calculation, what is the performance impact of calculating age/remaining for 50+ components on component overview page?** Are there caching strategies to mitigate this?

8. **How should staleness be handled for time-based data?** Should users see "Last calculated: 2 hours ago" indicators, or should calculations always be real-time?

### Status Calculation Logic

9. **What is the best approach for implementing the hybrid "worst case wins" logic when comparing time-based and distance-based statuses?** Should this be a single function, separate functions, or a pluggable strategy pattern?

10. **How should we refactor the existing `compute_component_status()` function to use simplified threshold logic (remaining < threshold)?** Should we maintain backward compatibility or introduce breaking changes?

11. **Should status calculation logic be extracted into a separate service/module, or remain in `business_logic.py`?** What separation of concerns makes sense?

12. **How should we handle edge cases where time intervals are NULL for some components and configured for others in the same query?** Conditional logic, separate query paths, or another approach?

### API and Backend Endpoints

13. **Do we need new API endpoints for updating time/threshold configurations, or can existing endpoints be extended?** What request/response schemas are needed?

14. **How should the backend validate that `threshold_km` and `threshold_days` are >0 when configured?** Client-side only, server-side only, or both? Should validation enforce that thresholds are required when corresponding intervals exist?

15. **Should time-based field updates trigger re-calculation of bike-level status aggregations?** How do we avoid cascading performance issues?

### Integration with Existing Features

16. **How does the quick swap feature interact with time-based component tracking?** Does swapping reset age timer or preserve it?

17. **How should service registration interact with time-based service intervals?** Does registering service reset `service_next_days` to `service_interval_days`?

18. **How should component retirement affect time-based tracking?** Should age timer stop, or continue counting?

### Testing and Validation

19. **What test cases are critical for validating simplified threshold logic (remaining < threshold)?** How do we ensure edge cases like exactly 0km remaining are handled correctly (should use <= for exceeded check)?

20. **How should we test time-based calculations that depend on current date?** Should we use fixed test dates, mocking, or another approach?

### Performance and Scalability

21. **What is the expected performance impact of adding 7 new fields per component (4 user-configured, 3 calculated)?** How does this scale to 1,000+ components?

22. **Should we implement pagination or lazy loading for component overview pages if calculations become expensive?** What threshold determines when optimization is needed?

### Migration and Backward Compatibility

23. **How should we handle existing components during migration?** Should time fields default to NULL, or should we attempt to populate them based on component type heuristics?

24. **What rollback strategy should be in place if the migration causes unexpected issues in production?** Backup database, reversible migration scripts, or another approach?

25. **How should we maintain backward compatibility with existing API consumers (if any)?** Should old endpoints continue to work, or require updates?

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

**Phase 2 Enhancements:**
- Separate `status_threshold_days` field (if architect determines it's necessary)
- "Apply type defaults to all components" bulk update feature
- Configurable status level names (e.g., "Needs attention" instead of "Due")
- Component age pause/resume for storage periods
- Notification system for time-based threshold crossings

**Phase 3 Enhancements:**
- Different deterioration rates for different storage conditions (humidity, temperature)
- Predictive analytics: "Based on your riding patterns, this component will need service in X weeks"
- Component health scoring (0-100) combining time, distance, service history
- Advanced filtering: "Show all components reaching end of life in next 30 days"

**Long-Term Considerations:**
- Machine learning for component lifetime predictions based on actual usage
- Integration with external component databases (expected lifetimes by brand/model)
- Component warranty tracking (time-based expiration)
- Seasonal component swap reminders (e.g., "Time to switch to winter tires")

---

## Integration Points

### Existing Features Impacted

**1. Component Status Calculations**
- Current `compute_component_status()` function must be refactored
- Current `update_component_lifetime_status()` and `update_component_service_status()` must be enhanced
- Hybrid logic requires checking both time and distance factors

**2. Component Creation and Editing**
- Create component modal must add 6 new fields
- Edit component modal must add 6 new fields
- Validation logic must handle NULL values for time intervals

**3. Component Type Management**
- Component types form must add 4 new fields
- Type defaults must be applied to new components (inheritance logic)

**4. Component Overview Page**
- Table must add status trigger indicator column (or merge into existing status column)
- Statistics (count by status) must reflect 3-level system

**5. Bike Details Page**
- Component table must add status trigger indicator
- Bike-level status aggregation must use 3-level system

**6. Component Detail Page**
- Must display component age, lifetime remaining (days), service next (days)
- Must display dual progress bars (time + distance)
- Must show which factor triggered current status

**7. Service Registration**
- Registering service must reset `service_next_days` to `service_interval_days`
- Must NOT reset `component_age_days` or `lifetime_remaining_days`

**8. Component History**
- First installation date derived from ComponentHistory table
- Age calculation depends on accurate history records

### Database Tables Affected

**1. `component_types` table**
- 4 new fields added: `service_interval_days`, `lifetime_expected_days`, `threshold_km`, `threshold_days`
- Migration adds fields with defaults (all NULL)

**2. `components` table**
- 7 new fields added: 4 user-configured (inherited from type), 3 calculated (age, remaining days)
- Migration adds fields with defaults

**3. `component_history` table**
- NOT modified, but heavily queried (first installation date lookup)

**4. `services` table**
- NOT modified, but queried for "last service date" in time-based service calculations

### API Endpoints Needed

**Modified Endpoints:**
- `POST /api/component` (create component) - accept 6 new fields
- `PUT /api/component/{id}` (update component) - accept 6 new fields
- `POST /api/component_type` (create type) - accept 4 new fields
- `PUT /api/component_type/{id}` (update type) - accept 4 new fields

**Query Endpoints:**
- `GET /api/components` - return time-based fields in response
- `GET /api/component/{id}` - return calculated age and remaining days

**No new endpoints required** - existing CRUD operations extended to handle new fields.

### Strava Integration Considerations

**No direct Strava integration changes needed.**

However, note:
- Distance-based updates triggered by Strava ride sync (existing behavior)
- Time-based updates NOT triggered by Strava (continuous/scheduled, see FR-6)
- Ride sync may trigger re-calculation of worst-case status (time vs. distance)

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
1. All 8 user stories are implemented with acceptance criteria met
2. All 6 validation examples pass automated and manual testing
3. No data loss or corruption during migration
4. Time-based status calculations accurate within 1 day
5. Hybrid threshold logic eliminates premature warnings for long-lifetime components
6. Performance impact <500ms for component overview page (50+ components)
7. Zero critical bugs in first month post-launch

---

## Technical Considerations for Architect

### 1. Time-Based Field Update Strategy (Detailed Analysis)

**Problem:** Time-based fields (`component_age_days`, etc.) change every day for ALL components, unlike distance-based fields which only update when rides are synced.

**Approach Comparison:**

| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| **Lazy Calculation** | Always accurate, no stale data, no scheduled tasks | Calculation overhead on EVERY query, N+1 query problem | ✓ RECOMMENDED for MVP (simplest) |
| **Scheduled Batch** | Pre-computed (fast queries), controlled resource usage | Stale data (up to 24h), requires cron/scheduler infrastructure | Consider for Phase 2 if performance issues |
| **Hybrid Cached** | Balance accuracy/performance, updates once per day | Complex cache invalidation logic | Consider for Phase 2 |
| **User-Triggered** | User controls freshness, no background tasks | May feel stale, requires manual action | Not recommended |

**Lazy Calculation Implementation:**

```python
@property
def component_age_days(self):
    """Calculate age dynamically from first installation date"""
    first_install = ComponentHistory.select().where(
        ComponentHistory.component_id == self.component_id,
        ComponentHistory.update_reason == "Installed"
    ).order_by(ComponentHistory.updated_date.asc()).first()

    if not first_install:
        return None

    first_install_date = datetime.strptime(first_install.updated_date, "%Y-%m-%d %H:%M")
    return (datetime.now() - first_install_date).days
```

**Optimization:**
- Cache first installation date in component record (avoid repeated history queries)
- Bulk load first installation dates for component overview pages

### 2. Database Transaction Strategy

**Critical Requirements:**
- Migration must be atomic (all-or-nothing)
- No partial state if migration fails

**Peewee Transaction Pattern:**
```python
with database.atomic():
    # Add columns to ComponentTypes
    migrator.add_column('component_types', 'service_interval_days', IntegerField(null=True))
    # ... add other fields

    # Update all existing records with defaults
    ComponentTypes.update(
        status_threshold_percentage=90,
        status_threshold_km=500
    ).execute()

    # If any operation fails, entire transaction rolls back
```

### 3. Simplified Threshold Logic Implementation

**Proposed Function Signature:**
```python
def compute_component_status(
    mode: str,  # "service" or "lifetime"
    remaining_value: int,  # km or days remaining
    threshold_value: int  # user-configured threshold
) -> str:
    """
    Compute component status using simplified threshold logic.

    Returns:
        "OK" | "Due for service" | "Service exceeded" |
        "Due for replacement" | "Lifetime exceeded"
    """
    # Exceeded logic
    if remaining_value <= 0:
        return "Service exceeded" if mode == "service" else "Lifetime exceeded"

    # Due logic - simple comparison
    if remaining_value < threshold_value:
        return "Due for service" if mode == "service" else "Due for replacement"

    # Otherwise OK
    return "OK"
```

### 4. Worst-Case Status Determination

**Helper Function:**
```python
def determine_worst_status(status1: str, status2: str) -> str:
    """
    Determine worst-case status from two status values.

    Status severity ranking (worst to best):
    1. "Exceeded" (worst)
    2. "Due"
    3. "OK"
    4. None (not configured)
    """
    severity_map = {
        "Service exceeded": 3,
        "Lifetime exceeded": 3,
        "Due for service": 2,
        "Due for replacement": 2,
        "OK": 1,
        None: 0
    }

    severity1 = severity_map.get(status1, 0)
    severity2 = severity_map.get(status2, 0)

    return status1 if severity1 >= severity2 else status2
```

### 5. Query Optimization Strategies

**Index Recommendations:**
- Index on `components.installation_status` (existing, used frequently)
- Index on `component_history.component_id` and `component_history.updated_date` (for first installation lookup)
- Composite index on `(component_id, update_reason, updated_date)` for optimized history queries

**Caching First Installation Date:**
- Option A: Add `first_installation_date` field to Components table (denormalized, updated on install/uninstall)
- Option B: Application-level cache (LRU cache for recent lookups)
- **Recommendation: Option A** (avoids repeated history queries)

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
- Add 4 fields to `ComponentTypes` model
- Add 7 fields to `Components` model (4 stored, 3 calculated/properties)

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
- **Scope:** Fully defined MVP with 8 user stories, comprehensive acceptance criteria, 6 validated test cases
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
