import unreal
import json

output_path = "{output_path}"

try:
    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "Unknown"

    # Run map check
    validator = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
    result = validator.validate_asset(world)
    result_str = str(result)
    is_valid = "VALID" in result_str.upper() and "INVALID" not in result_str.upper()

    unreal.log("Map check: " + level_name + " = " + result_str)
    with open(output_path, "w") as f:
        json.dump({
            "valid": is_valid,
            "level_name": level_name,
            "result": result_str
        }, f)
except Exception as e:
    unreal.log_error("validate_map failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"valid": False, "error": str(e)}, f)
