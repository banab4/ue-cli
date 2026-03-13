import unreal
import json

source_path = "{source_path}"
new_name = "{new_name}"
output_path = "{output_path}"

if not unreal.EditorAssetLibrary.does_asset_exist(source_path):
    unreal.log_error("Asset not found: " + source_path)
    with open(output_path, "w") as f:
        json.dump({"renamed": False, "error": "Asset not found: " + source_path}, f)
else:
    parts = source_path.rsplit("/", 1)
    parent_dir = parts[0] if len(parts) > 1 else "/Game"
    destination_path = parent_dir + "/" + new_name

    result = unreal.EditorAssetLibrary.rename_asset(source_path, destination_path)
    if result:
        unreal.log("Renamed: " + source_path + " -> " + destination_path)
        with open(output_path, "w") as f:
            json.dump({"renamed": True, "source": source_path, "destination": destination_path}, f)
    else:
        unreal.log_error("Failed to rename: " + source_path)
        with open(output_path, "w") as f:
            json.dump({"renamed": False, "error": "Failed to rename: " + source_path}, f)
