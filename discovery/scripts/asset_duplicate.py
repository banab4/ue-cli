import unreal
import json

source_path = "{source_path}"
destination_path = "{destination_path}"
output_path = "{output_path}"

if not unreal.EditorAssetLibrary.does_asset_exist(source_path):
    unreal.log_error("Asset not found: " + source_path)
    with open(output_path, "w") as f:
        json.dump({"duplicated": False, "error": "Asset not found: " + source_path}, f)
else:
    result = unreal.EditorAssetLibrary.duplicate_asset(source_path, destination_path)
    if result:
        unreal.log("Duplicated: " + source_path + " -> " + destination_path)
        with open(output_path, "w") as f:
            json.dump({"duplicated": True, "source": source_path, "destination": destination_path}, f)
    else:
        unreal.log_error("Failed to duplicate: " + source_path)
        with open(output_path, "w") as f:
            json.dump({"duplicated": False, "error": "Failed to duplicate: " + source_path}, f)
