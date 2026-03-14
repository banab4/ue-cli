import unreal
import json

level_path = "{level_path}"
output_path = "{output_path}"

try:
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    result = level_subsystem.load_level(level_path)

    if result:
        world = unreal.EditorLevelLibrary.get_editor_world()
        level_name = world.get_name() if world else "Unknown"
        unreal.log("Loaded level: " + level_path)
        with open(output_path, "w") as f:
            json.dump({"loaded": True, "level_path": level_path, "level_name": level_name}, f)
    else:
        unreal.log_error("Failed to load level: " + level_path)
        with open(output_path, "w") as f:
            json.dump({"loaded": False, "error": "Failed to load level: " + level_path}, f)
except Exception as e:
    unreal.log_error("level_load failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"loaded": False, "error": str(e)}, f)
