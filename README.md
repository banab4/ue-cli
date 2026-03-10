# ue-cli
---

AI agent skill + spec for controlling Unreal Engine Editor.

Uses UE's built-in Remote Control API (HTTP :30010) to manipulate the editor.

## Structure

```
ue-cli/
├── README.md
└── skills/
    └── ue-cli/
        ├── SKILL.md               # Agent skill (install target)
        ├── references/
        │   └── spec.md            # Command spec (35 commands)
        └── scripts/               # Group 2 Python templates
```

## Installation

```bash
npx skills add https://github.com/banab4/ue-cli
```

## Requirements

- Unreal Engine 5.x (editor running)
- `Web Remote Control` plugin enabled
- `Python Editor Script Plugin` enabled (for Group 2)

## Architecture

```
Agent → Read SKILL.md → Fetch spec.md → Build HTTP request → UE Editor (:30010)
```

- **Group 1** (18): Direct HTTP — call endpoints with parameters
- **Group 2** (17): HTTP → `ExecutePythonScript()` — send Python templates as strings
