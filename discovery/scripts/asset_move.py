import unreal
import json

source_path = "{source_path}"
destination_path = "{destination_path}"
output_path = "{output_path}"

subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
success = subsystem.rename_asset(source_path, destination_path)

if success:
    unreal.log("Moved: " + source_path + " -> " + destination_path)
    with open(output_path, "w") as f:
        json.dump({"moved": True, "source": source_path, "destination": destination_path}, f)
else:
    unreal.log_error("Failed to move: " + source_path)
    with open(output_path, "w") as f:
        json.dump({"moved": False, "error": "Failed to move: " + source_path}, f)
