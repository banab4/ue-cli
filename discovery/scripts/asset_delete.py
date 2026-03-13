import unreal
import json

asset_path = "{asset_path}"
output_path = "{output_path}"

if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
    unreal.log_error("Asset not found: " + asset_path)
    with open(output_path, "w") as f:
        json.dump({"deleted": False, "error": "Asset not found: " + asset_path}, f)
else:
    result = unreal.EditorAssetLibrary.delete_asset(asset_path)
    if result:
        unreal.log("Deleted asset: " + asset_path)
        with open(output_path, "w") as f:
            json.dump({"deleted": True, "asset_path": asset_path}, f)
    else:
        unreal.log_error("Failed to delete: " + asset_path)
        with open(output_path, "w") as f:
            json.dump({"deleted": False, "error": "Failed to delete: " + asset_path}, f)
