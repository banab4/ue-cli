import unreal
import json

sublevel_path = "{sublevel_path}"
action = "{action}"
output_path = "{output_path}"
_action_set = True

try:
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    act = action.lower() if (_action_set and action) else "add"

    if act == "remove":
        world = unreal.EditorLevelLibrary.get_editor_world()
        levels = world.get_editor_property("levels") if world else []
        removed = False
        for level in levels:
            if sublevel_path.lower() in level.get_path_name().lower():
                unreal.EditorLevelUtils.remove_level_from_world(level)
                removed = True
                break
        if removed:
            unreal.log("Removed sublevel: " + sublevel_path)
            with open(output_path, "w") as f:
                json.dump({"removed": True, "sublevel_path": sublevel_path}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"removed": False, "error": "Sublevel not found: " + sublevel_path}, f)
    else:
        new_level = unreal.EditorLevelUtils.add_level_to_world(
            unreal.EditorLevelLibrary.get_editor_world(),
            sublevel_path,
            unreal.LevelStreamingDynamic
        )
        if new_level:
            unreal.log("Added sublevel: " + sublevel_path)
            with open(output_path, "w") as f:
                json.dump({"added": True, "sublevel_path": sublevel_path}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"added": False, "error": "Failed to add sublevel: " + sublevel_path}, f)
except Exception as e:
    unreal.log_error("level_sublevel failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"error": str(e)}, f)
