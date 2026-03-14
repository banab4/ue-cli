import unreal
import json

save_path = "{save_path}"
output_path = "{output_path}"
_save_path_set = True

try:
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "Unknown"

    if _save_path_set and save_path:
        result = unreal.EditorLoadingAndSavingUtils.save_map(world, save_path)
        if result:
            unreal.log("Saved level as: " + save_path)
            with open(output_path, "w") as f:
                json.dump({"saved": True, "level": level_name, "save_path": save_path}, f)
        else:
            unreal.log_error("Failed to save level as: " + save_path)
            with open(output_path, "w") as f:
                json.dump({"saved": False, "error": "Failed to save level as: " + save_path}, f)
    else:
        result = level_subsystem.save_current_level()
        if result:
            unreal.log("Saved level: " + level_name)
            with open(output_path, "w") as f:
                json.dump({"saved": True, "level": level_name}, f)
        else:
            unreal.log_error("Failed to save level. If Untitled, provide save_path.")
            with open(output_path, "w") as f:
                json.dump({"saved": False, "error": "Failed to save level. If Untitled, provide save_path parameter."}, f)
except Exception as e:
    unreal.log_error("level_save failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"saved": False, "error": "Script error: " + str(e)}, f)
