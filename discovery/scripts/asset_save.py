import unreal
import json

asset_path = "{asset_path}"
output_path = "{output_path}"

if asset_path == "*":
    unreal.EditorAssetLibrary.save_directory("/Game/")
    unreal.log("Saved all assets in /Game/")
    with open(output_path, "w") as f:
        json.dump({"saved": True, "asset_path": "/Game/ (all)"}, f)
else:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset:
        unreal.log_error("Asset not found: " + asset_path)
        with open(output_path, "w") as f:
            json.dump({"saved": False, "error": "Asset not found: " + asset_path}, f)
    else:
        result = unreal.EditorAssetLibrary.save_asset(asset_path)
        if result:
            unreal.log("Saved: " + asset_path)
            with open(output_path, "w") as f:
                json.dump({"saved": True, "asset_path": asset_path}, f)
        else:
            unreal.log_error("Failed to save: " + asset_path)
            with open(output_path, "w") as f:
                json.dump({"saved": False, "error": "Failed to save: " + asset_path}, f)
