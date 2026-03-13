import unreal
import json

asset_path = "{asset_path}"
output_path = "{output_path}"

asset = unreal.EditorAssetLibrary.load_asset(asset_path)

if not asset:
    unreal.log_error("Asset not found: " + asset_path)
    with open(output_path, "w") as f:
        json.dump({"opened": False, "error": "Asset not found: " + asset_path}, f)
else:
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([asset])
    unreal.log("Opened asset editor: " + asset_path)
    with open(output_path, "w") as f:
        json.dump({"opened": True, "asset_path": asset_path}, f)
