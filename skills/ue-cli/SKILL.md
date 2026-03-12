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

**Script-first**: Always check `ue-cli script --list` for a matching script before using raw API calls. Scripts run inside UE Python and bypass Remote Control API serialization limits.

1. `ue-cli script --list` — check available scripts
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

## Available Scripts

### Asset
| Script | Params | Description |
|--------|--------|-------------|
| `asset_open` | asset_path | Open asset in editor |
| `asset_find` | search | Search assets by name/path |
| `asset_save` | asset_path | Save asset (* for all) |

### Actor
| Script | Params | Description |
|--------|--------|-------------|
| `actor_spawn` | asset_path, location_x, location_y, location_z | Spawn actor from asset |
| `actor_delete` | actor_name | Delete actor by name/label |
| `actor_select` | actor_name | Select actor by name/label |
| `actor_transform` | actor_name, location_x/y/z, rotation_pitch/yaw/roll, scale_x/y/z | Set transform |
| `actor_list` | filter_class | List actors (* for all) |

### Blueprint
| Script | Params | Description |
|--------|--------|-------------|
| `create_bp` | name, parent_class | Create blueprint |
| `add_component` | blueprint_name, component_type, component_name | Add component |
| `node_event` | blueprint_name, event_name, node_pos_x, node_pos_y | Add event node |
| `node_function` | blueprint_name, target_class, function_name, node_pos_x, node_pos_y | Add function node |
| `node_connect` | blueprint_name, source_node_name, source_pin_name, target_node_name, target_pin_name | Connect pins |
| `node_find` | blueprint_name, search_term | Find nodes |
| `node_variable` | blueprint_name, variable_name, variable_type, default_value | Add variable |
| `node_component` | blueprint_name, component_name, node_pos_x, node_pos_y | Get-component node |
| `node_self` | blueprint_name, node_pos_x, node_pos_y | Self-reference node |
| `node_input` | blueprint_name, action_name, node_pos_x, node_pos_y | Input action node |
| `input_mapping` | action_name, key_name, shift, ctrl, alt | Add input mapping |

### UMG
| Script | Params | Description |
|--------|--------|-------------|
| `umg_create` | widget_name | Create widget |
| `umg_button` | widget_name, button_name, button_text | Add button |
| `umg_text` | widget_name, text_content, text_name | Add text |
| `umg_event` | widget_name, widget_element_name, event_name | Bind event |
| `umg_text_bind` | widget_name, text_block_name, binding_function | Text binding |
| `umg_viewport` | widget_name, z_order | Show in viewport |

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
