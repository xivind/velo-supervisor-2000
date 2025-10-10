# Handovers Directory

**Context-aware instructions for agents working with handover documents.**

## Purpose

This directory contains handover documents that facilitate communication between specialized agents in the Velo Supervisor 2000 development workflow. Handovers are the **primary communication mechanism** between agents, serving as persistent records of decisions, work completed, and context for next steps.

## Directory Structure

```
.handovers/
├── CLAUDE.md         # This file - instructions for using handovers
├── TEMPLATE.md       # Template for creating new handovers
├── requirements/     # Requirements and user stories from @product-manager
├── architecture/     # Architecture plans and decisions from @architect
├── database/         # Database schema designs and migrations from @database-expert
├── ux/              # UI/UX designs and specifications from @ux-designer
├── fullstack/       # Implementation notes from @fullstack-developer
├── review/          # Code review reports from @code-reviewer
└── documentation/   # Documentation updates from @docs-maintainer
```

## Naming Convention

**Pattern:** `[feature-name]-[source-agent]-to-[target-agent].md`

**Examples:**
- `component-swap-requirements.md` (requirements document from @product-manager)
- `tire-pressure-tracking-architect-to-ux-designer.md`
- `warranty-schema-database-to-fullstack.md`
- `collections-review-fullstack-to-reviewer.md`
- `strava-webhooks-decision-architect.md` (decision record without handoff)

**Rules:**
- Use lowercase with hyphens
- Be descriptive but concise
- Include source and target agent (unless it's a decision record)
- Keep related handovers using same feature prefix

## When You're Creating a Handover

1. **Use TEMPLATE.md** - Always start from the template
2. **Save to correct subdirectory** - Match your agent type
3. **Fill all sections** - Context, Deliverables, Decisions, Next Steps
4. **Be specific** - Include file paths, line numbers, commit references
5. **Update status** - "In Progress", "Complete", or "Blocked"
6. **Name clearly** - Follow the naming convention above

**Example workflow for @architect:**
```bash
# Copy template
cp .handovers/TEMPLATE.md .handovers/architecture/user-auth-architect-to-ux-designer.md

# Edit and fill in all sections
# Save when complete
```

## When You're Reading Handovers

**Finding the latest handover for your work:**
```bash
# Most recently modified handovers
ls -lt .handovers/*/*.md | head -5

# Handovers waiting for you (example for @ux-designer)
find .handovers -name "*to-ux-designer.md"

# Search by feature
find .handovers -name "*tire-pressure*"
```

**Read the handover from the previous agent** to understand:
- What was already completed
- Decisions that were made and why
- What you specifically need to do
- Any blockers or questions
- References to relevant files

## Standard Workflows

### Feature Development Flow

```
@product-manager (for vague/unclear requirements)
  ↓ creates requirements/[feature]-requirements.md

@architect (reads product-manager's handover)
  ↓ creates architecture/[feature]-architect-to-ux-designer.md

@ux-designer (reads architect's handover)
  ↓ creates ux/[feature]-ux-designer-to-fullstack.md

@fullstack-developer (reads ux-designer's handover)
  ↓ creates fullstack/[feature]-fullstack-to-reviewer.md

@code-reviewer (reads fullstack's handover)
  ↓ creates review/[feature]-reviewer-to-fullstack.md (if revisions)
  ↓ OR review/[feature]-reviewer-approved.md (if approved)

@docs-maintainer (reads reviewer's handover)
  ↓ creates documentation/[feature]-docs-complete.md
```

**Note**: Skip @product-manager if requirements are already crystal clear. Start with @architect in that case.

### Bug Fix Flow

```
@fullstack-developer
  ↓ creates fullstack/[bug]-fullstack-to-reviewer.md

@code-reviewer
  ↓ creates review/[bug]-reviewer-approved.md

@docs-maintainer
  ↓ creates documentation/[bug]-commit-ready.md
```

### Database-Involved Flow

When database changes are needed, @fullstack-developer should:

```
@fullstack-developer (identifies need for DB changes)
  ↓ creates fullstack/[feature]-fullstack-to-database.md

@database-expert (reads fullstack's handover)
  ↓ creates database/[feature]-database-to-fullstack.md

@fullstack-developer (continues with DB changes in place)
  ↓ creates fullstack/[feature]-fullstack-to-reviewer.md
```

## What to Include in Your Handover

### Context Section
- What you were asked to do
- What you actually did
- Why you made key decisions
- How this fits into the larger feature

### Deliverables Section
**Be specific with file paths:**
```markdown
## Deliverables
- `backend/main.py:145-167` - Added new `/api/export` endpoint
- `backend/business_logic.py:89-120` - Implemented export logic
- `frontend/templates/export.html` - Created export UI template
- `.handovers/fullstack/export-fullstack-to-reviewer.md` - This handover
```

### Decisions Made
Document **why** you chose certain approaches:
```markdown
## Decisions Made
1. **Used CSV format instead of JSON**: CSV is more compatible with Excel for end users
2. **Export limited to 1000 records**: Prevents timeout on large datasets
3. **Added background task**: Long exports won't block the UI
```

### Next Steps
Clear, actionable tasks for the receiving agent:
```markdown
## Next Steps for @code-reviewer
1. Review export endpoint security - ensure user can only export their own data
2. Check CSV generation logic for edge cases (special characters, nulls)
3. Validate UI responsiveness on mobile
4. Test with large datasets (500+ components)
```

## Handover Lifecycle

1. **Created** - Source agent writes handover, status: "In Progress"
2. **Handed Off** - Target agent reads and begins work
3. **Completed** - Target agent finishes, creates their own handover
4. **Committed** - Handovers are committed to git as documentation

**Never delete handovers** - they serve as:
- Architectural decision records (ADR)
- Implementation history
- Knowledge base for future work
- Audit trail for why decisions were made

## Finding Active Work

**To see what's currently in progress:**
```bash
# Handovers modified in last 7 days
find .handovers -name "*.md" -not -name "CLAUDE.md" -not -name "TEMPLATE.md" -mtime -7

# Search for in-progress work
grep -r "Status: In Progress" .handovers/

# Handovers waiting for a specific agent
grep -r "Ready for: \*\*ux-designer\*\*" .handovers/
```

## Best Practices

✅ **DO:**
- Use the template for every handover
- Include specific file paths and line numbers
- Document the "why" behind decisions
- Update status fields accurately
- Reference related handovers
- Keep feature names consistent across handovers
- Commit handovers to git

❌ **DON'T:**
- Create handovers outside this directory structure
- Skip sections in the template
- Make vague references ("fixed the bug")
- Delete old handovers
- Use generic file names
- Forget to update status

## Questions or Issues?

- Check `TEMPLATE.md` for handover structure
- Read the root `/CLAUDE.md` for overall agent workflow
- Review recent handovers for examples
- Ask the human if unclear about handover requirements

---

**Remember:** Handovers are how we maintain context across agent transitions. Write them as if you're briefing a colleague who's picking up where you left off - because that's exactly what's happening.
