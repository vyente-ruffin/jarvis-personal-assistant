---
description: "Execute JARVIS TDD tasks via sub-agents to preserve main context"
argument-hint: "[task-id|all|parallel-group] [--dry-run]"
---

# JARVIS TDD Orchestrator

You are the orchestrator for JARVIS Test-Driven Development tasks.

## Your Role

Spawn sub-agents to execute TDD tasks while preserving the main context window. Each task runs in isolation with its own context.

## Task Dependency Graph

```
M1.1 (Project Structure)
  ├── M1.2 (WebSocket) ──┬── M1.3 (Session) ── M1.4 (Graceful Shutdown)
  │                      │
  └── M2.1 (Mem0) ───────┴── M2.2 (Context) ── M2.3 (Memory Types)
                                    │
                                    ├── M2.4 (Auto-Tag)
                                    └── M2.5 (Memory Search)

M3.1 (Claude SDK) ── M3.2 (Streaming) ── M3.3 (Tool Use)
                            │
                            └── M3.4 (Multi-Turn)

M4.1 (Reminders) ─┬── M4.2 (Notes) ─┬── M4.3 (Tasks)
                  │                 │
                  └─────────────────┴── M4.4 (Calendar)
```

## Parallel Execution Groups

Tasks within the same group have no dependencies and can run in parallel:

| Group | Tasks | Prerequisites |
|-------|-------|---------------|
| G0 | M1.1 | None |
| G1 | M1.2, M2.1 | G0 complete |
| G2 | M1.3, M2.2, M3.1 | M1.2, M2.1 complete |
| G3 | M1.4, M2.3, M2.4, M3.2, M4.1 | G2 complete |
| G4 | M2.5, M3.3, M3.4, M4.2 | G3 complete |
| G5 | M4.3, M4.4 | G4 complete |

## Execution Modes

### Single Task
```
/jarvis:tdd M1.2
```
Spawns one sub-agent for the specified task.

### Parallel Group
```
/jarvis:tdd G1
```
Spawns sub-agents for all tasks in the group (in parallel).

### All Tasks
```
/jarvis:tdd all
```
Executes all groups sequentially, with parallel execution within each group.

### Dry Run
```
/jarvis:tdd all --dry-run
```
Shows execution plan without running.

## Orchestration Instructions

When user runs this command:

1. **Parse Arguments**: Identify target (task ID, group, or "all")

2. **For Single Task** ($ARGUMENTS matches M#.#):
   - Read task prompt: `.claude/tasks/$ARGUMENTS.md`
   - Spawn jarvis-tdd-runner agent with Task tool
   - Wait for completion promise or failure

3. **For Parallel Group** ($ARGUMENTS matches G#):
   - Identify all tasks in the group
   - Spawn ALL sub-agents in parallel using multiple Task tool calls in ONE message
   - Track completion promises from each

4. **For All Tasks**:
   - Execute groups G0 through G5 sequentially
   - Within each group, spawn agents in parallel
   - Only proceed to next group when ALL tasks in current group complete

5. **Track Progress**:
   - Use TodoWrite to track task status
   - Report completion promises as they arrive
   - Document any blocked tasks

## Sub-Agent Spawning Pattern

Use the Task tool with these parameters:

```
subagent_type: jarvis-tdd-runner
prompt: |
  Execute TDD task: [TASK_ID]

  Task prompt file: @.claude/tasks/[TASK_ID].md

  Follow the TDD workflow strictly. Only output the completion promise when ALL tests pass.
```

## Critical Rules

1. **ALWAYS use Task tool** - Never execute tasks in main context
2. **Parallel when possible** - Spawn multiple agents in ONE message for parallel groups
3. **Sequential for dependencies** - Wait for prerequisites before spawning dependent tasks
4. **Track promises** - Each sub-agent outputs `<promise>TASK_ID COMPLETE</promise>`
5. **Report failures** - If a task is blocked, document it and continue with independent tasks

## Success Criteria

All 25 tasks complete with their promises:
- M1.1-M1.4: Core infrastructure
- M2.1-M2.5: Memory system
- M3.1-M3.4: Claude integration
- M4.1-M4.4: Feature tools
