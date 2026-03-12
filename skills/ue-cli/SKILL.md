---
name: ue-cli
version: 0.2.0
description: "Unreal Engine: Control the editor via Remote Control API."
metadata:
  requires:
    bins: ["ue-cli"]
    plugins: ["Web Remote Control", "Python Editor Script Plugin"]
---
# ue-cli
---

CLI for controlling Unreal Engine Editor via Remote Control API (HTTP :30010).

## Prerequisites

- UE Editor running with `Web Remote Control` plugin enabled (HTTP :30010)
- `Python Editor Script Plugin` enabled (for script commands)
- `ue-cli` installed: `npm install -g @banaba/ue-cli`

## Workflow (IMPORTANT)

**Script-first**: Always run `ue-cli script --list` to discover available scripts before using raw API calls. This is the **single source of truth** for the script catalog. Scripts run inside UE Python and bypass Remote Control API serialization limits.

1. `ue-cli script --list` — discover available scripts (dynamic catalog)
2. `ue-cli call <scriptName> --params '{...}' --force` — if script exists, use this
3. Only if no script matches: `ue-cli call <objectPath> <functionName> --params '{...}' --force`

### Script-first routing

`ue-cli call` auto-detects: if the first argument matches a script name, it runs the script. Otherwise it falls back to direct API call.

```bash
# Script mode (1 arg — preferred)
ue-cli call asset_open --params '{"asset_path":"/Game/SM/BP_Top"}' --force

# API fallback (2 args — only when no script covers the function)
ue-cli call /Script/UnrealEd.Default__UnrealEditorSubsystem GetEditorWorld --force
```

## Raw API Commands

Only use these when no script covers the operation:

| Command | Description |
|---------|-------------|
| `ue-cli call <objectPath> <functionName> [--params '{}']` | Call a function |
| `ue-cli get <objectPath> <propertyName>` | Read a property |
| `ue-cli set <objectPath> <propertyName> --value '{}'` | Write a property |
| `ue-cli describe <objectPath>` | Get object schema |

### Discovery

| Command | Description |
|---------|-------------|
| `ue-cli discover` | Browse available objects/functions |
| `ue-cli discover --detail <objectPath>` | Show function signatures |
| `ue-cli discover --object <keyword>` | Filter by class name |
| `ue-cli info` | List all API routes (online) |
| `ue-cli search --query '{}'` | Search assets (online) |

### Batch

| Command | Description |
|---------|-------------|
| `ue-cli batch --requests '[...]'` | Execute multiple requests |

## Global flags

| Flag | Description |
|------|-------------|
| `--host <url>` | UE host (default: http://localhost:30010) |
| `--dry-run` | Preview request without sending |
| `--force` | Skip confirmation (always use this flag) |
| `--timeout <ms>` | HTTP timeout (default: 5000) |
| `--verbose` | Print request/response headers |
| `--transaction` | Generate undo transaction (call, set) |

## Git Bash

On Git Bash (MSYS), `/Script/...` paths get converted. Always prefix with:
```bash
MSYS_NO_PATHCONV=1 ue-cli call ...
```
