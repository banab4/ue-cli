import unreal

asset_path = "{asset_path}"

asset = unreal.EditorAssetLibrary.load_asset(asset_path)

if not asset:
    unreal.log_error("Asset not found: " + asset_path)
else:
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([asset])
    unreal.log("Opened asset editor: " + asset_path)
