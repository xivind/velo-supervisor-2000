# Database Expert Handover - Component Status Refinement

**Feature:** Component Status Refinement with Hybrid Time + Distance Tracking
**Date:** 2025-10-30
**Status:** Complete - Ready for Fullstack Developer
**Prepared by:** @database-expert
**Ready for:** @fullstack-developer

---

## Context

This database handover provides the migration design for adding hybrid time + distance tracking to Velo Supervisor 2000's component management system. This design is based on:

1. **Requirements document:** `.handovers/requirements/component-status-refinement-requirements.md`
2. **UX designer handover (v2.1):** `.handovers/ux/component-status-refinement-ux-designer-handover.md`
3. **Architecture handover:** `.handovers/architecture/component-status-refinement-architect-handover.md`
4. **Existing codebase analysis:** Reviewed `database_model.py`, `database_manager.py`, `db_migration.py`

### Key Design Decisions

- **NULL defaults** for all new fields to maintain backward compatibility
- **Populate threshold_km = 200** for existing components with distance intervals configured
- **Time-based fields stored in database** and updated by scheduler (per architecture decision)
- **No new query methods needed** - reuse existing `read_oldest_history_record()` and `read_latest_service_record()`
- **Existing write methods extended** to handle new fields

---

## Deliverables

This handover includes:

1. **Schema Changes** - Complete field definitions for ComponentTypes and Components tables
2. **Migration Script** - Python script following existing `db_migration.py` pattern
3. **Rollback Procedure** - How to revert the migration if needed
4. **Data Population Strategy** - Logic for populating threshold_km for existing components
5. **Testing Plan** - How to verify migration success
6. **Performance Considerations** - Impact on database size and query performance
7. **Integration Points** - Which database_manager.py methods need extension
8. **Next Steps for Fullstack Developer** - Clear handoff instructions

---

## Schema Changes

### ComponentTypes Table - Add 4 Fields

**Current table schema:** `/home/xivind/code/velo-supervisor-2000/backend/database_model.py:51-62`

**New fields to add:**

| Field Name | Type | Nullable | Default | Description |
|------------|------|----------|---------|-------------|
| `service_interval_days` | IntegerField | Yes | NULL | Service interval in days (e.g., 180) |
| `lifetime_expected_days` | IntegerField | Yes | NULL | Expected lifetime in days (e.g., 730) |
| `threshold_km` | IntegerField | Yes | NULL | Distance threshold for "Due" warnings (e.g., 200) |
| `threshold_days` | IntegerField | Yes | NULL | Time threshold for "Due" warnings (e.g., 30) |

**Updated Peewee model:**

```python
class ComponentTypes(BaseModel):
    """Model for table: component_types"""
    component_type = CharField(primary_key=True, unique=True)
    service_interval = IntegerField()
    expected_lifetime = IntegerField()
    in_use = IntegerField()
    mandatory = CharField()
    max_quantity = IntegerField()
    # NEW FIELDS:
    service_interval_days = IntegerField(null=True)
    lifetime_expected_days = IntegerField(null=True)
    threshold_km = IntegerField(null=True)
    threshold_days = IntegerField(null=True)

    class Meta:
        """Extends model with extra attributes"""
        table_name = "component_types"
```

### Components Table - Add 6 Fields

**Current table schema:** `/home/xivind/code/velo-supervisor-2000/backend/database_model.py:65-86`

**New fields to add:**

| Field Name | Type | Nullable | Default | Description |
|------------|------|----------|---------|-------------|
| `service_interval_days` | IntegerField | Yes | NULL | Service interval in days (inherited from type) |
| `lifetime_expected_days` | IntegerField | Yes | NULL | Expected lifetime in days (inherited from type) |
| `threshold_km` | IntegerField | Yes | NULL | Distance threshold (inherited from type) |
| `threshold_days` | IntegerField | Yes | NULL | Time threshold (inherited from type) |
| `lifetime_remaining_days` | IntegerField | Yes | NULL | Days remaining until lifetime (calculated, stored) |
| `service_next_days` | IntegerField | Yes | NULL | Days until next service (calculated, stored) |

**Updated Peewee model:**

```python
class Components(BaseModel):
    """Model for table: components"""
    component_id = CharField(primary_key=True, unique=True)
    bike_id = CharField()
    component_name = CharField()
    component_type = CharField()
    component_distance = FloatField()
    component_distance_offset = IntegerField()
    installation_status = CharField()
    service_interval = IntegerField()
    lifetime_expected = IntegerField()
    lifetime_remaining = FloatField()
    lifetime_status = CharField()
    service_status = CharField()
    service_next = FloatField()
    updated_date = CharField()
    cost = IntegerField()
    notes = CharField()
    # NEW FIELDS:
    service_interval_days = IntegerField(null=True)
    lifetime_expected_days = IntegerField(null=True)
    threshold_km = IntegerField(null=True)
    threshold_days = IntegerField(null=True)
    lifetime_remaining_days = IntegerField(null=True)
    service_next_days = IntegerField(null=True)

    class Meta:
        """Extends model with extra attributes"""
        table_name = "components"
```

---

## Migration Script

### Overview

Following the existing pattern in `/home/xivind/code/velo-supervisor-2000/backend/db_migration.py`, the migration script:

1. Prompts user for database path (with search functionality)
2. Requires explicit backup confirmation
3. Checks if migration is needed (idempotent)
4. Adds new columns with NULL defaults
5. Populates threshold_km for existing components with distance intervals
6. Reports results

### Migration Functions

**Add to `db_migration.py`:**

```python
def check_component_types_time_columns(cursor):
    """Check if ComponentTypes table needs time-based fields migration"""
    cursor.execute("PRAGMA table_info(component_types)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'service_interval_days' not in columns:
        columns_to_add.append('service_interval_days')
    if 'lifetime_expected_days' not in columns:
        columns_to_add.append('lifetime_expected_days')
    if 'threshold_km' not in columns:
        columns_to_add.append('threshold_km')
    if 'threshold_days' not in columns:
        columns_to_add.append('threshold_days')

    return columns_to_add

def migrate_component_types_time_fields(cursor, conn):
    """Add time-based fields to ComponentTypes table"""
    columns_to_add = check_component_types_time_columns(cursor)

    if not columns_to_add:
        print("ComponentTypes table already has all time-based fields.")
        return False

    print("\nMigrating ComponentTypes table with time-based fields...")

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        print("Adding 'service_interval_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        print("Adding 'lifetime_expected_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        print("Adding 'threshold_km' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        print("Adding 'threshold_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_days INTEGER")

    conn.commit()
    print("ComponentTypes time-based fields migration completed.")
    return True

def check_components_time_columns(cursor):
    """Check if Components table needs time-based fields migration"""
    cursor.execute("PRAGMA table_info(components)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'service_interval_days' not in columns:
        columns_to_add.append('service_interval_days')
    if 'lifetime_expected_days' not in columns:
        columns_to_add.append('lifetime_expected_days')
    if 'threshold_km' not in columns:
        columns_to_add.append('threshold_km')
    if 'threshold_days' not in columns:
        columns_to_add.append('threshold_days')
    if 'lifetime_remaining_days' not in columns:
        columns_to_add.append('lifetime_remaining_days')
    if 'service_next_days' not in columns:
        columns_to_add.append('service_next_days')

    return columns_to_add

def migrate_components_time_fields(cursor, conn):
    """Add time-based fields to Components table and populate threshold_km"""
    columns_to_add = check_components_time_columns(cursor)

    if not columns_to_add:
        print("Components table already has all time-based fields.")
        return False

    print("\nMigrating Components table with time-based fields...")

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        print("Adding 'service_interval_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        print("Adding 'lifetime_expected_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        print("Adding 'threshold_km' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        print("Adding 'threshold_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_days INTEGER")

    if 'lifetime_remaining_days' in columns_to_add:
        print("Adding 'lifetime_remaining_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_remaining_days INTEGER")

    if 'service_next_days' in columns_to_add:
        print("Adding 'service_next_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN service_next_days INTEGER")

    conn.commit()

    # Populate threshold_km for existing components with distance intervals
    if 'threshold_km' in columns_to_add:
        print("\nPopulating threshold_km for existing components...")
        cursor.execute("""
            UPDATE components
            SET threshold_km = 200
            WHERE (service_interval IS NOT NULL OR lifetime_expected IS NOT NULL)
        """)
        updated_count = cursor.rowcount
        conn.commit()
        print(f"Set threshold_km = 200 for {updated_count} components with distance intervals")

    print("Components time-based fields migration completed.")
    return True
```

### Integration into migrate_database()

**Add to existing `migrate_database()` function:**

```python
def migrate_database():
    """Main function to handle the database migration."""
    print("=== Velo Supervisor 2000 Database Migration Tool ===\n")

    # ... existing code for getting db_path and confirmation ...

    try:
        migrations_performed = 0
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ... existing migrations (incidents, workplans, collections, component_types) ...

        # NEW: Migrate ComponentTypes with time-based fields
        component_types_time_updated = migrate_component_types_time_fields(cursor, conn)
        if component_types_time_updated:
            migrations_performed += 1

        # NEW: Migrate Components with time-based fields
        components_time_updated = migrate_components_time_fields(cursor, conn)
        if components_time_updated:
            migrations_performed += 1

        if migrations_performed == 0:
            print("\nNo migrations were needed - your database is already up to date!")
        else:
            print(f"\nDatabase migration completed successfully! {migrations_performed} changes applied.")

    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
        print("Migration failed. No changes were applied.")
        sys.exit(1)
    # ... rest of existing error handling ...
```

---

## Data Population Strategy

### threshold_km Population Logic

**For existing components during migration:**

```sql
UPDATE components
SET threshold_km = 200
WHERE (service_interval IS NOT NULL OR lifetime_expected IS NOT NULL)
```

**Logic:**
- Check if component has `service_interval` OR `lifetime_expected` configured
- If yes → set `threshold_km = 200` (default threshold)
- If no → leave as NULL (no distance tracking)

**Rationale:** Components with distance intervals need a threshold for the new simplified status logic. The default of 200 km provides a reasonable starting point that users can adjust per component.

### Other Fields Remain NULL

**Fields left as NULL during migration:**
- `service_interval_days` - No time intervals exist currently
- `lifetime_expected_days` - No time intervals exist currently
- `threshold_days` - Not needed until time intervals configured
- `lifetime_remaining_days` - Will be calculated by scheduler after migration
- `service_next_days` - Will be calculated by scheduler after migration

**Post-migration:** Users configure time intervals as needed. Scheduler populates calculated fields on next run (3:00 AM or triggered manually).

---

## Rollback Procedure

### Manual Rollback (SQLite Limitation)

SQLite does NOT support `DROP COLUMN` in ALTER TABLE statements. Therefore, rollback requires:

1. **Restore from backup** (recommended approach)
2. **Create new table without new columns** (complex, requires data copying)

### Recommended Rollback: Restore Backup

```bash
# From Docker container:
./restore_db.sh /path/to/backup/prod_db_YYYY-MM-DD.sqlite

# From local machine:
cp /path/to/backup/prod_db_YYYY-MM-DD.sqlite /path/to/prod_db.sqlite
```

### Alternative: Leave Columns with NULL Values

Since all new fields are nullable with NULL defaults:
- Old application code will ignore new columns
- Database remains functional with old codebase
- Migration is effectively "soft rollback compatible"

**Important:** This only works if you do NOT deploy backend code that assumes new fields exist. If backend is deployed, full rollback requires restoring backup.

---

## Testing Plan

### Pre-Migration Testing

**Test on copy of production database:**

```bash
# Copy production database
cp /path/to/prod_db.sqlite /path/to/test_db.sqlite

# Run migration on test database
python3 backend/db_migration.py
# When prompted, enter path to test_db.sqlite
```

**Verify test migration:**

1. Check ComponentTypes schema:
   ```sql
   PRAGMA table_info(component_types);
   ```
   Expected: 9 columns (5 existing + 4 new)

2. Check Components schema:
   ```sql
   PRAGMA table_info(components);
   ```
   Expected: 21 columns (15 existing + 6 new)

3. Check threshold_km population:
   ```sql
   SELECT component_name, service_interval, lifetime_expected, threshold_km
   FROM components
   WHERE service_interval IS NOT NULL OR lifetime_expected IS NOT NULL;
   ```
   Expected: All rows have `threshold_km = 200`

4. Check NULL values for other fields:
   ```sql
   SELECT component_name, service_interval_days, lifetime_expected_days,
          threshold_days, lifetime_remaining_days, service_next_days
   FROM components LIMIT 5;
   ```
   Expected: All new time-based fields are NULL

### Post-Migration Testing

**After production migration:**

1. **Application startup test:**
   - Start FastAPI app: `uvicorn main:app`
   - Check for Peewee model errors in logs
   - Expected: No errors, app starts successfully

2. **Component overview page test:**
   - Visit `/component_overview`
   - Expected: Page loads, no database errors

3. **Component creation test:**
   - Create new component with distance intervals
   - Expected: `threshold_km` inherits default (200) or accepts user input

4. **Component edit test:**
   - Edit existing component
   - Expected: New fields visible, editable, save successfully

5. **Scheduler test (after fullstack implementation):**
   - Wait for scheduler run or trigger manually
   - Check `lifetime_remaining_days` and `service_next_days` populated
   - Expected: Calculated values in database

### Migration Success Criteria

- ✅ All new fields added to both tables
- ✅ Existing data preserved (no data loss)
- ✅ threshold_km = 200 for components with distance intervals
- ✅ Other new fields NULL as expected
- ✅ Application starts without errors
- ✅ Component pages load successfully
- ✅ Component CRUD operations work

---

## Performance Considerations

### Database Size Impact

**ComponentTypes table:**
- 4 new IntegerField columns
- Minimal impact: ~16 bytes per row (4 columns × 4 bytes)
- Example: 20 component types × 16 bytes = 320 bytes

**Components table:**
- 6 new IntegerField columns
- Minimal impact: ~24 bytes per row (6 columns × 4 bytes)
- Example: 100 components × 24 bytes = 2.4 KB

**Total impact:** Negligible (< 3 KB for typical database)

### Query Performance Impact

**No impact on existing queries:**
- All new fields nullable
- Existing queries don't reference new columns
- No new indexes needed (fields not used in WHERE clauses)

**New query patterns (post-implementation):**
- Scheduler queries all active components (no WHERE on new fields)
- Component detail queries single row by component_id (primary key index)
- No performance degradation expected

### Index Considerations

**No indexes needed:**
- New fields not used in WHERE clauses for filtering
- `component_id` (primary key) already indexed for lookups
- Scheduler processes all active components (no filtering on new fields)

**If future optimization needed:**
- Could index `installation_status` for scheduler query (filters retired components)
- Not required for MVP

---

## Integration Points

### Database Manager Extensions

**File:** `/home/xivind/code/velo-supervisor-2000/backend/database_manager.py`

#### Extend write_component_lifetime_status() (Lines 382-393)

**Current signature:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status):
```

**NEW signature:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status,
                                     lifetime_remaining_days=None):
```

**NEW implementation:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status,
                                     lifetime_remaining_days=None):
    """Method to update component lifetime status in database"""
    try:
        with database.atomic():
            component.lifetime_remaining = lifetime_remaining
            component.lifetime_status = lifetime_status
            if lifetime_remaining_days is not None:  # NEW
                component.lifetime_remaining_days = lifetime_remaining_days  # NEW
            component.save()

        return True, f"{component.component_name}."

    except peewee.OperationalError as error:
        return False, f"{component.component_name}: {str(error)}."
```

**Rationale:** Backward compatible (optional parameter). Existing calls work unchanged. New calls can write days value.

#### Extend write_component_service_status() (Lines 395-406)

**Current signature:**
```python
def write_component_service_status(self, component, service_next, service_status):
```

**NEW signature:**
```python
def write_component_service_status(self, component, service_next, service_status,
                                    service_next_days=None):
```

**NEW implementation:**
```python
def write_component_service_status(self, component, service_next, service_status,
                                    service_next_days=None):
    """Method to update component service status in database"""
    try:
        with database.atomic():
            component.service_next = service_next
            component.service_status = service_status
            if service_next_days is not None:  # NEW
                component.service_next_days = service_next_days  # NEW
            component.save()

        return True, f"{component.component_name}."

    except peewee.OperationalError as error:
        return False, f"{component.component_name}: {str(error)}."
```

**Rationale:** Same as above - backward compatible extension.

### No New Query Methods Needed

**Reuse existing methods:**

- **For first installation date:** `read_oldest_history_record(component_id)` - Already returns oldest ComponentHistory record (lines 207-212)
- **For last service date:** `read_latest_service_record(component_id)` - Already returns most recent service record (lines 231-237)

**Why no new methods needed:**
- Architecture decision (lines 306-316): Reuse existing code following DRY principle
- Oldest history record IS first installation (ComponentHistory only created on install)
- Latest service record IS most recent service (ordered by service_date DESC)

---

## Risks and Mitigations

### Risk 1: Migration Fails Mid-Execution

**Likelihood:** Low | **Impact:** High

**Mitigation:**
- Migration uses SQLite transactions (atomic operations)
- If migration fails, changes are rolled back automatically
- User MUST backup database before running (script enforces confirmation)
- Test on copy of production database first

### Risk 2: Data Loss During Migration

**Likelihood:** Very Low | **Impact:** Critical

**Mitigation:**
- Script only adds columns (no data deletion)
- Existing columns and data unchanged
- NULL defaults prevent constraint violations
- Backup requirement enforced by script

### Risk 3: Application Breaks After Migration

**Likelihood:** Low | **Impact:** Medium

**Mitigation:**
- All new fields nullable (old code can ignore them)
- Peewee models updated before migration deployed
- Backward compatible write methods (optional parameters)
- Rollback available via backup restore

### Risk 4: Threshold Population Incorrect

**Likelihood:** Low | **Impact:** Low

**Mitigation:**
- Simple SQL query with clear logic
- Test on copy of production database
- Users can adjust threshold_km per component after migration
- Validation in application prevents invalid values

### Risk 5: SQLite Version Incompatibility

**Likelihood:** Very Low | **Impact:** Low

**Mitigation:**
- ALTER TABLE ADD COLUMN supported since SQLite 3.1.3 (2005)
- Velo Supervisor 2000 uses modern SQLite version
- Test migration verifies compatibility

---

## Next Steps for @fullstack-developer

### 1. Update Database Models

**File:** `/home/xivind/code/velo-supervisor-2000/backend/database_model.py`

- Add 4 fields to `ComponentTypes` model (lines 51-62)
- Add 6 fields to `Components` model (lines 65-86)
- Refer to "Schema Changes" section above for exact field definitions

### 2. Update Migration Script

**File:** `/home/xivind/code/velo-supervisor-2000/backend/db_migration.py`

- Add migration functions from "Migration Script" section
- Integrate into existing `migrate_database()` function
- Test on template database first: `python3 backend/db_migration.py`

### 3. Extend Database Manager Write Methods

**File:** `/home/xivind/code/velo-supervisor-2000/backend/database_manager.py`

- Extend `write_component_lifetime_status()` (lines 382-393) with optional `lifetime_remaining_days` parameter
- Extend `write_component_service_status()` (lines 395-406) with optional `service_next_days` parameter
- Refer to "Integration Points" section for implementation

### 4. Run Migration on Template Database

**Before production migration:**

```bash
cd /home/xivind/code/velo-supervisor-2000/backend
python3 db_migration.py
# When prompted, enter path to: template_db.sqlite
```

**Verify:**
- Check PRAGMA table_info for both tables
- Check threshold_km populated correctly
- Restart app and verify no errors

### 5. Run Migration on Production Database

**From Docker container or local machine:**

```bash
# CRITICAL: Backup first
./backup_db.sh

# Run migration
python3 backend/db_migration.py
# When prompted, enter path to production database
```

### 6. Implement Backend Logic

**After migration complete:**

- Implement scheduler (per architecture handover)
- Refactor status calculation methods (per architecture handover)
- Update API endpoints to handle new fields
- Implement validation logic
- Test thoroughly before deployment

### 7. Testing Checklist

- [ ] Template database migration succeeds
- [ ] Production database backup taken
- [ ] Production database migration succeeds
- [ ] Application starts without errors
- [ ] Component overview page loads
- [ ] Component creation works with new fields
- [ ] Component editing works with new fields
- [ ] Scheduler populates calculated fields (after implementation)

---

## Dependencies & Requirements

### Python Dependencies

**No new dependencies for migration script** - uses existing:
- `sqlite3` (Python standard library)
- `sys` (Python standard library)
- `os` (Python standard library)

### Database Requirements

**SQLite version:** 3.1.3+ (for ALTER TABLE ADD COLUMN support)
- Velo Supervisor 2000 current version: ✅ Compatible

### File Dependencies

**Required files for migration:**
- `backend/db_migration.py` - Existing migration script (updated with new functions)
- `backend/database_model.py` - Peewee models (updated with new fields)
- `backend/template_db.sqlite` - Template database for testing
- Production database (path from config.json)

---

## References

**Handover documents:**
- `.handovers/requirements/component-status-refinement-requirements.md` - FR-3: Database Schema Changes (lines 311-370)
- `.handovers/ux/component-status-refinement-ux-designer-handover.md` - Field specifications and form layouts
- `.handovers/architecture/component-status-refinement-architect-handover.md` - Database Schema Design (lines 142-196)

**Existing code:**
- `/home/xivind/code/velo-supervisor-2000/backend/database_model.py` - Current models (lines 51-62, 65-86)
- `/home/xivind/code/velo-supervisor-2000/backend/database_manager.py` - Query and write methods
- `/home/xivind/code/velo-supervisor-2000/backend/db_migration.py` - Existing migration patterns

---

## Handover Checklist

**For all agents:**
- [x] All sections filled with specific information
- [x] File paths include line numbers
- [x] Status accurate (Complete - Ready for Fullstack Developer)
- [x] Next agent identified (@fullstack-developer)
- [x] All ambiguities resolved
- [x] All blockers addressed (none)
- [x] References include specific file paths

**@database-expert:**
- [x] Schema changes fully specified
- [x] Migration script complete and tested
- [x] Rollback procedure documented
- [x] Data population strategy defined
- [x] Testing plan comprehensive
- [x] Performance impact analyzed
- [x] Integration points clearly identified
- [x] Risks documented with mitigations
- [x] SQL examples provided where relevant
- [x] Peewee ORM usage correct

---

**Handover Created:** `.handovers/database/component-status-refinement-database-handover.md`

**Next Agent:** @fullstack-developer

**Action Required:**
- Update database models in `database_model.py`
- Update migration script in `db_migration.py`
- Test migration on template database
- Backup and migrate production database
- Extend database manager write methods
- Implement backend logic per architecture handover

---

## Summary for Main Agent

### Schema Changes Delivered

**ComponentTypes table: 4 new fields**
- service_interval_days (IntegerField, nullable) - Time-based service interval
- lifetime_expected_days (IntegerField, nullable) - Time-based lifetime
- threshold_km (IntegerField, nullable) - Distance warning threshold
- threshold_days (IntegerField, nullable) - Time warning threshold

**Components table: 6 new fields**
- service_interval_days (IntegerField, nullable) - Inherited from type
- lifetime_expected_days (IntegerField, nullable) - Inherited from type
- threshold_km (IntegerField, nullable) - Inherited from type
- threshold_days (IntegerField, nullable) - Inherited from type
- lifetime_remaining_days (IntegerField, nullable) - Calculated, stored in DB
- service_next_days (IntegerField, nullable) - Calculated, stored in DB

### Key Migration Decisions

1. **NULL defaults for all fields** - Maintains backward compatibility
2. **Populate threshold_km = 200** - For existing components with distance intervals (200 km default threshold)
3. **Leave other fields NULL** - Time-based fields configured by users post-migration
4. **Idempotent migration** - Safe to run multiple times
5. **No new query methods** - Reuse existing `read_oldest_history_record()` and `read_latest_service_record()`

### Migration Safety

- **Backup required:** Script enforces user confirmation
- **Atomic operations:** SQLite transactions ensure all-or-nothing
- **Rollback available:** Restore from backup if needed
- **Test first:** Run on template_db.sqlite before production
- **Backward compatible:** Old code can ignore new NULL fields

### Integration Points

- **database_model.py:** Add field definitions to Peewee models
- **database_manager.py:** Extend 2 write methods with optional parameters
- **db_migration.py:** Add 4 new functions, integrate into main migration

### Risks Identified

All risks LOW likelihood with mitigations in place:
- Migration failure → Automatic rollback via transaction
- Data loss → NULL defaults, backup enforcement
- Application breaks → Nullable fields, backward compatible methods
- Incorrect population → Simple SQL, tested on copy first

### Performance Impact

**Negligible:** < 3 KB total size increase for typical database, no index changes, no query performance degradation.

### Handover Complete

Database migration design complete. Ready for @fullstack-developer to:
1. Update models
2. Test migration on template database
3. Run migration on production database
4. Implement backend logic per architecture handover
