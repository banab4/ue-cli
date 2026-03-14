import unreal
import json

sequence_path = "{sequence_path}"
output_path = "{output_path}"

try:
    sequence = unreal.EditorAssetLibrary.load_asset(sequence_path)

    if not sequence:
        # Try to create if not exists
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        parts = sequence_path.rsplit("/", 1)
        package_path = parts[0] if len(parts) > 1 else "/Game"
        asset_name = parts[1] if len(parts) > 1 else sequence_path
        factory = unreal.LevelSequenceFactoryNew()
        sequence = asset_tools.create_asset(asset_name, package_path, unreal.LevelSequence, factory)
        if sequence:
            unreal.EditorAssetLibrary.save_asset(sequence_path)

    if not sequence:
        with open(output_path, "w") as f:
            json.dump({"opened": False, "error": "Sequence not found and failed to create: " + sequence_path}, f)
    else:
        asset_subsystem = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
        asset_subsystem.open_editor_for_assets([sequence])

        unreal.log("Opened sequence: " + sequence_path)
        with open(output_path, "w") as f:
            json.dump({"opened": True, "sequence_path": sequence.get_path_name()}, f)
except Exception as e:
    unreal.log_error("seq_open failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"opened": False, "error": str(e)}, f)
