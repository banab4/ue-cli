import unreal

source_path = "{source_path}"
destination_path = "{destination_path}"

subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
success = subsystem.rename_asset(source_path, destination_path)

if success:
    unreal.log("Moved: " + source_path + " -> " + destination_path)
else:
    unreal.log_error("Failed to move: " + source_path)
