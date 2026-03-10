---
name: ue-cli
version: 0.1.0
description: "Unreal Engine: Control the editor via Remote Control API."
metadata:
  requires:
    plugins: ["Web Remote Control", "Python Editor Script Plugin"]
---
# ue-cli
---

Skill for controlling Unreal Engine Editor via Remote Control API (HTTP :30010).

## Prerequisites

- UE Editor must be running
- `Web Remote Control` plugin must be enabled (HTTP server :30010)
- `Python Editor Script Plugin` must be enabled for Group 2 commands

## Spec

Fetch the full command spec from the URL below:

- **spec.md**: `https://raw.githubusercontent.com/banab4/ue-cli/main/skills/ue-cli/references/spec.md`

## Execution

### Group 1 (Direct HTTP)

Read endpoint/parameter info from spec.md and construct HTTP requests directly.

```
PUT http://localhost:30010/{endpoint}
Content-Type: application/json

{request body}
```

### Group 2 (via Python Script)

1. Check the script path for the command in spec.md
2. Fetch `https://raw.githubusercontent.com/banab4/ue-cli/main/skills/ue-cli/scripts/{script}.py`
3. Inject parameters into the template
4. Send to UE via `ExecutePythonScript()`:

```
PUT http://localhost:30010/object/call
{
  "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
  "functionName": "ExecutePythonScript",
  "parameters": {
    "PythonScript": "{script string}"
  }
}
```

> [!CAUTION]
> Write commands (actor deletion, property modification, etc.) are hard to undo — require user confirmation.
