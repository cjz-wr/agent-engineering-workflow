# Agent Engineering Workflow

[简体中文](./README.zh-CN.md)

Production-oriented workflow skills for AI coding agents.

**v2.2.0**

Organize the following pipeline into installable, reusable Coding Agent Workflows:

```
Requirement → Plan → Code Navigation → Impact Analysis → Implementation → Validation → Knowledge Capture → Git Commit → Delivery
```

This is not a plain collection of prompts, but a set of installable Coding Agent Workflow Skills.

## Why

Common problems with traditional Coding Agents:

- Reading too much context
- Losing control of change scope
- Not knowing the impact range of code changes
- Overwriting the user's existing modifications
- Lacking knowledge capture in long-running projects
- Depending on chat memory across sessions
- Unstable validation and delivery processes

This project addresses them through:

| Mechanism | What it solves |
| --- | --- |
| State Machine | Clear phases and resumable states, avoiding process drift |
| Risk Control | L0–L4 risk levels to keep change scope under control |
| Progressive Discovery | Locate code layer by layer, reducing context reads |
| Code Graph | Understand structure and impact (Impact / Blast Radius) |
| Vector Knowledge | Long-term knowledge capture, reusable across sessions |
| Git Safety | Protect the user's existing changes with small commits |
| Validation | Stable validation pipeline |
| Acceptance Criteria | Item-by-item verification before delivery |

## Two Ways of Use

This project offers two levels of usage:

### Lightweight Prompt Edition

Best for small projects, personal projects, and scenarios where you want to copy prompts directly.

Located at:

`simplePrompt/`

Main files:

- `OptimizeGeneratePromotSkill.md`
  - For new project initialization and incremental development
- `OptimizeEditFunctionSkill.md`
  - For feature modification, bug fixes, and local refactoring in existing projects

These prompts are verified through real usage — shorter workflow and lower context overhead, suitable for small projects that do not need a full Agent Skills infrastructure.

v2.2 adds state machine, risk control, code graph, and vector knowledge on top of the lightweight prompt edition, so it is more complete but also requires more context and a more complex execution flow.

### Agent Skills Edition

Best for medium-to-large projects, long-term maintained projects, and scenarios that need persistent knowledge, code graphs, state management, and standard Skill installation.

Includes:

- `project-bootstrap-workflow`
- `feature-change-workflow`

Features:

- Standard `SKILL.md` structure
- State machine
- Risk levels
- Code Graph
- Vector Backend
- Progressive Discovery
- Cross-session plan state
- Complete validation and delivery workflow

## Skills

| Skill | Use when | Input | Output |
| --- | --- | --- | --- |
| `project-bootstrap-workflow` | New project | `readme.md` | Complete project skeleton and development workflow |
| `feature-change-workflow` | Existing project | User request + project context | Safe incremental modification |

```
New project → project-bootstrap-workflow
Existing project change → feature-change-workflow
```

## Architecture

The two Skills share one Base Engineering Protocol. Feature Change only adds the specific flow for modifying existing projects, avoiding two duplicated rule sets.

```
        Shared Engineering Protocol
                 │
          ┌──────┴──────┐
          ↓             ↓
   Project Bootstrap  Feature Change
      Workflow           Workflow
          ↓                 ↓
      New Project     Existing Project
```

The Base Protocol is defined once, at `skills/project-bootstrap-workflow/references/base-protocol.md`.

## Core Capabilities

### Engineering Control

- Agent State Machine
- L0–L4 Risk Control
- Before Snapshot
- Decision Log

### Code Intelligence

- Progressive Discovery
- L1/L2/L3 Navigation
- Code Graph
- Impact / Blast Radius

### Knowledge

- Vector Backend
- MCP → Python → Markdown fallback
- Full Index
- Incremental Sync
- Health Check

### Delivery

- Git Safety
- Validation Pipeline
- Acceptance Criteria
- Cross-session Plan State

## Knowledge System

```
MCP Vector Backend
        ↓
Python Local Vector Backend
        ↓
Markdown fallback
```

- Reuse an existing Backend first
- When no MCP is available, try a Python project-level isolated environment
- Use Markdown Summary only as the last resort
- Not bound to any specific vector database product

## Quick Start

### New Project

```text
Use project-bootstrap-workflow to initialize and develop a new project from readme.md.
```

### Existing Project

```text
Use feature-change-workflow to modify the existing project based on the following requirement:
<feature request>
```

### Bug Fix

```text
Use feature-change-workflow to analyze and fix the existing project based on the following issue:
<bug description>
```

## Installation

### Option A — Project-local installation

Best for team projects. Clone the repository, then copy the Skill directory you need into the target agent's project-level skills directory.

```
git clone <your-repository-url>
cd <your-repository-name>
```

### Option B — User-level installation

Best for reusing across all your personal projects. Copy the Skill directory into the target agent's user-level skills directory.

### Option C — Local Installer

A local-only install script (copies files locally, never auto-installs extra dependencies over the network):

```
./scripts/install-local.sh codex
./scripts/install-local.sh claude
./scripts/install-local.sh cursor
```

Install to the user-level directory:

```
./scripts/install-local.sh codex --user
```

The script never silently overwrites an existing Skill with the same name — it fails safely with a hint.

> Skills search paths may differ between clients and versions. Always follow the target client's current official documentation.

## What Happens After Installation

```
User Request
    ↓
Skill Selection
    ↓
Analyze
    ↓
Plan
    ↓
Code Navigation
    ↓
Implement
    ↓
Validate
    ↓
Commit
    ↓
Delivery
```

## Example

`examples/demo-project/` demonstrates a complete example and the relationships between its files:

| File | Responsibility |
| --- | --- |
| `readme.md` | Product requirement source |
| `AGENTS.md` | AI development conventions |
| `plan.md` | Development plan and progress |
| `tree.md` | Directory structure explanation |
| `decision.md` | Key engineering decision log |

## Repository Layout

```
agent-engineering-workflow/
├── README.md
├── skills/      # Two Workflow Skills
├── docs/        # Architecture and protocol docs
├── examples/    # demo-project example
└── scripts/     # Validation and install scripts
```

## Compatibility

Designed for Agent Skills-compatible coding agents.

The exact discovery path and installation behavior may differ by client and version.
Always follow the target client's current documentation for skill installation and discovery.

## Development

Validate the Skill structure:

```
python scripts/validate-skills.py
```

Checks: Skill structure, frontmatter, references, version, duplication.

Suggested flow when changing the protocol:

```
Change Base Protocol → Validate → Sync both Skills → Update version
```

## Contributing

If you have suggestions or encounter issues, feel free to open an [Issue](../../issues) or submit a [Pull Request](../../pulls).

## Version

Current version: **v2.2.0**

See git history / release notes for changes.

## License

[MIT](./LICENSE)
