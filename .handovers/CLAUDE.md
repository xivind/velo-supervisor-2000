# Handovers Directory

Handover documents facilitate communication between agents. They are committed to git as architectural decision records.

## Directory Structure

```
.handovers/
├── stages/           # one handover per rewrite stage, written at its end
├── requirements/     # @product-manager
├── architecture/     # @architect
├── database/         # @database-expert
├── ux/              # @ux-designer
├── fullstack/       # @fullstack-developer
├── review/          # @code-reviewer
└── documentation/   # @docs-maintainer
```

Only `stages/` exists in git today. Git keeps no empty folders, so the other subfolders are created with their first handover.

## Creating Handovers

1. Copy `TEMPLATE.md` to the correct subdirectory
2. Name: `[feature-name]-[source-agent]-to-[target-agent].md`; a stage handover is `stages/stage-<n>-<name>-handover.md`
3. Fill all sections with specific file paths and line numbers
4. Max 100 lines (see Communication & Output Rules in CLAUDE.md)

## Finding Handovers

```bash
# Recent handovers
ls -lt .handovers/*/*.md | head -5

# Handovers for a specific agent
find .handovers -name "*to-ux-designer.md"

# By feature
find .handovers -name "*tire-pressure*"

# In-progress work
grep -r "Status: In Progress" .handovers/
```

## Rules

- Handovers are kept as decision records. A superseded one may be removed only with the user's agreement, after its decisions are captured in code, tests or a stage handover
- Include file paths with line numbers
- Document the "why" behind decisions
- See CLAUDE.md for workflow sequence and agent roles
