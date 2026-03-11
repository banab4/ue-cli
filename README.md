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
- Node.js 18+

## Usage

```bash
# Check connectivity
ue-cli info

# Discover object schema
ue-cli describe /Script/Engine.EditorLevelLibrary

# Read a property
ue-cli get /Game/Map.Map:PersistentLevel.Light_0.LightComponent0 Intensity

# Call a function (requires confirmation or --force)
ue-cli call /Script/Engine.EditorLevelLibrary GetAllLevelActors --force

# Write a property
ue-cli set /Game/Map.Map:PersistentLevel.Cube_0 RelativeLocation --value '{"X":0,"Y":0,"Z":200}' --force

# Execute a Python template
ue-cli script create_bp --params '{"name":"BP_Player","parent_class":"Actor"}' --force

# Preview without executing
ue-cli call /Script/Engine.EditorLevelLibrary DestroyActor --params '{}' --dry-run

# List available templates
ue-cli script --list
```

## Architecture

```
Agent → SKILL.md → ue-cli command → CLI validates + sends HTTP → UE Editor (:30010)
```

## Structure

```
ue-cli/
├── package.json
├── bin/ue-cli.js              # Entry point
├── src/
│   ├── cli.js                 # Command dispatcher
│   ├── commands/              # Verb handlers (call, get, set, describe, script, search, info, batch)
│   ├── http.js                # HTTP client
│   ├── validation.js          # Input validation
│   ├── safety.js              # Write confirmation
│   └── output.js              # JSON output
├── templates/                 # Bundled Python templates (17)
└── skills/ue-cli/             # Agent skill definition
    ├── SKILL.md
    ├── references/spec.md
    └── scripts/*.py
```
