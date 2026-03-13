import unreal
import json

output_path = "{output_path}"

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
result = level_subsystem.save_current_level()

if result:
    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "Unknown"
    unreal.log("Saved level: " + level_name)
    with open(output_path, "w") as f:
        json.dump({"saved": True, "level": level_name}, f)
else:
    unreal.log_error("Failed to save level")
    with open(output_path, "w") as f:
        json.dump({"saved": False, "error": "Failed to save level"}, f)
