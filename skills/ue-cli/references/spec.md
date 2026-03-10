# ue-cli spec
---

Classified by Remote Control API endpoint.

## Group 1: Direct HTTP (18)

### `PUT /remote/object/call` — Function Call (8)

| Command | Target |
|---------|--------|
| List actors | `EditorLevelLibrary.GetAllLevelActors()` |
| Spawn actor | `EditorLevelLibrary.SpawnActorFromClass()` |
| Delete actor | `EditorLevelLibrary.DestroyActor()` |
| Spawn BP | `SpawnActorFromObject()` |
| Spawn BP actor | `SpawnActorFromObject()` |
| Compile BP | `KismetEditorUtilities.CompileBlueprint()` |
| Move viewport | `SetViewportLocation()` |
| Take screenshot | `AutomationBlueprintFunctionLibrary` |

### `PUT /remote/object/property` — Property Read/Write (8)

| Command | Target | access |
|---------|--------|--------|
| Set transform | Actor Transform | WRITE_ACCESS |
| Set property | Actor property | WRITE_ACCESS |
| Component property | Component objectPath | WRITE_ACCESS |
| Physics settings | BodyInstance | WRITE_ACCESS |
| BP property | CDO objectPath | WRITE_ACCESS |
| Pawn property | Pawn settings | WRITE_ACCESS |
| Mesh/Material assignment | StaticMesh/Material | WRITE_ACCESS |
| BP default values | CDO defaults | WRITE_ACCESS |

### `PUT /remote/object/describe` — Schema Query (1)

| Command | Target |
|---------|--------|
| Describe properties | Full object schema |

### Client-side Processing (1)

| Command | Method |
|---------|--------|
| Find actor | Filter actor list by name |

---

## Group 2: via Python Script (17)

Execution path: `PUT /remote/object/call` → `ExecutePythonScript()` → UE built-in Python (`unreal` module)

### AssetTools — Asset Creation (2)

| Command | Script | API |
|---------|--------|-----|
| Create BP | `scripts/create_bp.py` | `BlueprintFactory` → `AssetTools.create_asset()` |
| Create Widget BP | `scripts/umg_create.py` | `WidgetBlueprintFactory` → `AssetTools.create_asset()` |

### SubobjectDataSubsystem — Component Manipulation (1)

| Command | Script | API |
|---------|--------|-----|
| Add component | `scripts/add_component.py` | `SubobjectDataSubsystem.add_new_subobject()` |

### BlueprintEditorLibrary — Graph Node Manipulation (8)

| Command | Script |
|---------|--------|
| Event node | `scripts/node_event.py` |
| Function call node | `scripts/node_function.py` |
| Variable declaration | `scripts/node_variable.py` |
| Input action node | `scripts/node_input.py` |
| Self reference | `scripts/node_self.py` |
| Component getter | `scripts/node_component.py` |
| Connect node pins | `scripts/node_connect.py` |
| Find nodes | `scripts/node_find.py` |

### WidgetTree — UI Widget Manipulation (5)

| Command | Script |
|---------|--------|
| Add text block | `scripts/umg_text.py` |
| Add button | `scripts/umg_button.py` |
| Display in viewport | `scripts/umg_viewport.py` |
| Bind event | `scripts/umg_event.py` |
| Bind text | `scripts/umg_text_bind.py` |

### InputSettings — Project Settings (1)

| Command | Script |
|---------|--------|
| Add input mapping | `scripts/input_mapping.py` |
