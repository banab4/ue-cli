# ue-cli
---

CLI + AI agent skill for controlling Unreal Engine Editor via Remote Control API.

## Installation

### CLI (for humans and agents)

```bash
npm install -g @banab4/ue-cli
```

### Skill (for AI agents)

```bash
npx skills add https://github.com/banab4/ue-cli
```

## Requirements

- Unreal Engine 5.x (editor running)
- `Web Remote Control` plugin enabled (HTTP :30010)
- `Python Editor Script Plugin` enabled (for script commands)
- `Enable Remote Python Execution` enabled in Project Settings → Remote Control → Security (for script commands)
- Node.js 18+

## Usage

```bash
# Check connectivity
ue-cli info

# Browse available objects and functions (offline, from GitHub)
ue-cli discover
ue-cli discover --detail /Script/UnrealEd.Default__EditorActorSubsystem
ue-cli discover --category subsystem
ue-cli discover --object Actor

# Inspect full object schema (online, from UE editor)
ue-cli describe /Script/UnrealEd.Default__EditorActorSubsystem

# Read a property
ue-cli get /Game/Map.Map:PersistentLevel.Cube_0.StaticMeshComponent0 RelativeLocation

# Call a function (requires confirmation or --force)
ue-cli call /Script/UnrealEd.Default__EditorActorSubsystem GetAllLevelActors --force

# Write a property
ue-cli set /Game/Map.Map:PersistentLevel.Cube_0.StaticMeshComponent0 RelativeLocation --value '{"X":0,"Y":0,"Z":200}' --force

# Execute a Python template
ue-cli script create_bp --params '{"name":"BP_Player","parent_class":"Actor"}' --force

# List available templates
ue-cli script --list

# Preview without executing
ue-cli call /Script/UnrealEd.Default__EditorActorSubsystem DestroyActors --params '{}' --dry-run
```

## Architecture

```
Agent → SKILL.md → ue-cli command → CLI validates + sends HTTP → UE Editor (:30010)
                                  ↗
              discovery/index.json  (object/function catalog, fetched from GitHub)
              discovery/scripts/*.py (Python templates, fetched from GitHub)
```

## Structure

```
ue-cli/
├── package.json
├── bin/ue-cli.js              # Entry point
├── src/
│   ├── cli.js                 # Command dispatcher
│   ├── commands/              # Verb handlers (call, get, set, describe, discover, script, search, info, batch)
│   ├── http.js                # HTTP client
│   ├── validation.js          # Input validation
│   ├── safety.js              # Write confirmation
│   └── output.js              # JSON output
├── discovery/
│   ├── index.json             # Object/function catalog (runtime fetch from GitHub)
│   └── scripts/*.py           # Python templates (17, runtime fetch from GitHub)
└── skills/ue-cli/
    └── SKILL.md               # Agent skill definition
```
