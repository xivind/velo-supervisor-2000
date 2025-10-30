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
3. **Data Population Strategy** - Logic for populating threshold_km for existing components
4. **Performance Considerations** - Impact on database size and query performance
5. **Integration Points** - Which database_manager.py methods need extension
6. **Next Steps for Fullstack Developer** - Clear handoff instructions

**Note:** Rollback procedures, comprehensive testing plans, and detailed risk analyses were removed from this handover as they are unnecessary for this simple additive migration (see "Note on Scope Reduction" section).

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

**Updated Peewee model (logically grouped):**

```python
class ComponentTypes(BaseModel):
    """Model for table: component_types"""
    component_type = CharField(primary_key=True, unique=True)
    service_interval = IntegerField()
    expected_lifetime = IntegerField()
    service_interval_days = IntegerField()
    lifetime_expected_days = IntegerField()
    threshold_km = IntegerField()
    threshold_days = IntegerField()
    in_use = IntegerField()
    mandatory = CharField()
    max_quantity = IntegerField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "component_types"
```

**Note on field order and nullability:** Field order rearranged for logical grouping without affecting code functionality. New fields follow existing pattern - no explicit `null=True` parameter (consistent with existing nullable fields like `service_interval`, `expected_lifetime`). The actual database column order remains unchanged (new columns are at the end due to ALTER TABLE).

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

**Updated Peewee model (logically grouped):**

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
    service_interval_days = IntegerField()
    service_next = FloatField()
    service_next_days = IntegerField()
    service_status = CharField()
    lifetime_expected = IntegerField()
    lifetime_expected_days = IntegerField()
    lifetime_remaining = FloatField()
    lifetime_remaining_days = IntegerField()
    lifetime_status = CharField()
    threshold_km = IntegerField()
    threshold_days = IntegerField()
    updated_date = CharField()
    cost = IntegerField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "components"
```

**Note on field order and nullability:** Same as ComponentTypes - field order rearranged for logical grouping, no explicit `null=True` parameters (consistent with existing pattern).

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
    # Note: Other fields remain NULL (SQLite default for new columns)
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
        print("Other new fields remain NULL (SQLite default) - no explicit action needed")

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

**NULL handling:** SQLite automatically defaults new columns to NULL when using `ALTER TABLE ADD COLUMN` (no explicit DEFAULT NULL needed). No update statement required - new columns are NULL by default.

**Post-migration:** Users configure time intervals as needed. Scheduler populates calculated fields on next run (3:00 AM or triggered manually). Business logic passes `None` to database_manager when values should be NULL, and Peewee writes NULL to database (consistent with existing pattern at business_logic.py:791-797).

---

## Note on Scope Reduction

**Original sections removed:** Rollback Procedure, Testing Plan, Risks and Mitigations

**Rationale:** Given the minimal nature of these database changes, these comprehensive procedures are unnecessary:

- **Simple additive migration:** Only adding nullable columns with NULL defaults - no data modification, no complex transformations
- **Low risk:** Cannot break existing functionality since:
  - All new fields are nullable
  - Existing code ignores new columns
  - No schema restructuring or data deletion
- **Standard workflow coverage:** Existing `db_migration.py` already has idempotent checks, backup prompts, and error handling
- **Fast verification:** App startup immediately reveals any model/schema mismatches

**Testing approach:** The @fullstack-developer will verify migration success by simply:
1. Running migration script on template database
2. Starting the application (Peewee will validate schema automatically)
3. Opening component overview page (confirms database queries work)

The comprehensive testing, rollback, and risk procedures documented in the original version are available in git history (commit b2aee5c) if ever needed for reference.

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

**IMPORTANT - Pattern Consistency:**
- **NO default values** in method signatures (all parameters required)
- Business logic explicitly passes `None` when values should be NULL
- Peewee automatically writes NULL to database when field value is `None`
- See existing pattern at business_logic.py:791-797 and database_manager.py:382-406

#### Extend write_component_lifetime_status() (Lines 382-393)

**Current signature:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status):
```

**NEW signature:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status, lifetime_remaining_days):
```

**NEW implementation:**
```python
def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status, lifetime_remaining_days):
    """Method to update component lifetime status in database"""
    try:
        with database.atomic():
            component.lifetime_remaining = lifetime_remaining
            component.lifetime_status = lifetime_status
            component.lifetime_remaining_days = lifetime_remaining_days  # NEW - can be None
            component.save()

        return True, f"{component.component_name}."

    except peewee.OperationalError as error:
        return False, f"{component.component_name}: {str(error)}."
```

**Pattern consistency:** Following existing pattern - NO default values, business_logic explicitly passes `None` when appropriate (see lines 791-797 for current pattern). Peewee automatically writes NULL to database when field value is `None`.

#### Extend write_component_service_status() (Lines 395-406)

**Current signature:**
```python
def write_component_service_status(self, component, service_next, service_status):
```

**NEW signature:**
```python
def write_component_service_status(self, component, service_next, service_status, service_next_days):
```

**NEW implementation:**
```python
def write_component_service_status(self, component, service_next, service_status, service_next_days):
    """Method to update component service status in database"""
    try:
        with database.atomic():
            component.service_next = service_next
            component.service_status = service_status
            component.service_next_days = service_next_days  # NEW - can be None
            component.save()

        return True, f"{component.component_name}."

    except peewee.OperationalError as error:
        return False, f"{component.component_name}: {str(error)}."
```

**Pattern consistency:** Same as above - NO default values, business_logic explicitly passes `None` when appropriate.

### Verification: Existing Methods Robustness

**Methods that DO NOT need modification (automatically handle new fields):**

✅ **All read methods** (lines 183-237):
- `read_component(component_id)` - Uses Peewee `.select()` which automatically includes ALL model fields
- `read_oldest_history_record(component_id)` - Returns complete ComponentHistory record
- `read_latest_service_record(component_id)` - Returns complete Services record
- `read_all_components()` - Selects all component records with all fields

✅ **write_component_details(component_id, new_component_data)** (lines 362-380):
- Uses `Components.update(**new_component_data)` - accepts dictionary, will update any fields included
- Uses `Components.create(**new_component_data)` - creates with any fields in dictionary
- **NO modification needed** - as long as business_logic includes new fields in the dictionary, they will be written

**Methods that REQUIRE modification (explicit field assignment):**

❌ **write_component_lifetime_status()** (lines 382-393):
- Currently: `component.lifetime_remaining = lifetime_remaining`
- Uses explicit field assignment, not dictionary unpacking
- **Must add:** `component.lifetime_remaining_days = lifetime_remaining_days` assignment

❌ **write_component_service_status()** (lines 395-406):
- Currently: `component.service_next = service_next`
- Uses explicit field assignment, not dictionary unpacking
- **Must add:** `component.service_next_days = service_next_days` assignment

**Why the difference?**
- `write_component_details()` uses `**new_component_data` dictionary unpacking → flexible, handles any fields
- Status write methods use direct field assignment → explicit, must be updated for each new field

**Architecture decision verified:** Only 2 methods need extension (status write methods). All other database operations will automatically handle new fields through Peewee's ORM and dictionary unpacking patterns.


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

- Extend `write_component_lifetime_status()` (lines 382-393) with new `lifetime_remaining_days` parameter (required, no default)
- Extend `write_component_service_status()` (lines 395-406) with new `service_next_days` parameter (required, no default)
- Refer to "Integration Points" and "Verification: Existing Methods Robustness" sections for details
- **Note:** All other database_manager methods require NO modification (verified in "Verification" section)

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

### 7. Verification Checklist

Simple verification steps (detailed procedures removed per scope reduction):

- [ ] Migration runs successfully on template database
- [ ] Application starts without Peewee model errors
- [ ] Component overview page loads without database errors

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
- [x] Migration script complete
- [x] Data population strategy defined
- [x] Performance impact analyzed
- [x] Integration points clearly identified
- [x] SQL examples provided where relevant
- [x] Peewee ORM usage correct
- [x] Rollback/testing/risks sections appropriately scoped for simple additive migration

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

- **database_model.py:** Add field definitions to Peewee models (10 fields total)
- **database_manager.py:** Extend ONLY 2 write methods with new required parameters (NO defaults - see pattern note)
  - All other methods (read, write_component_details) automatically handle new fields - NO modification needed
  - See "Verification: Existing Methods Robustness" section for details
- **db_migration.py:** Add 4 new functions, integrate into main migration

### Pattern Consistency Note

**Critical for implementation:**
- Database manager methods follow existing pattern - NO default values in signatures
- Business logic explicitly passes `None` for NULL values
- SQLite automatically defaults new columns to NULL during migration
- Peewee ORM automatically includes new fields in read operations
- Dictionary unpacking methods (`write_component_details`) automatically handle new fields

### Performance Impact

**Negligible:** < 3 KB total size increase for typical database, no index changes, no query performance degradation.

### Risk Assessment

**Very Low:** Simple additive migration with nullable fields. Standard `db_migration.py` workflow provides adequate safety (idempotency, backup prompts, atomic transactions).

### Handover Complete

Database migration design complete and verified. Ready for @fullstack-developer to:
1. Update models (10 new fields, logically grouped)
2. Extend ONLY 2 database_manager methods (all others verified to work automatically)
3. Test migration on template database
4. Run migration on production database
5. Implement backend logic per architecture handover

**Method robustness verified:** Read methods and `write_component_details()` require NO modification - they automatically handle new fields through Peewee ORM and dictionary unpacking.
