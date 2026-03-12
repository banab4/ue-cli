import unreal

asset_path = "{asset_path}"

if asset_path == "*":
    unreal.EditorAssetLibrary.save_directory("/Game/")
    unreal.log("Saved all assets in /Game/")
else:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset:
        unreal.log_error("Asset not found: " + asset_path)
    else:
        result = unreal.EditorAssetLibrary.save_asset(asset_path)
        if result:
            unreal.log("Saved: " + asset_path)
        else:
            unreal.log_error("Failed to save: " + asset_path)
