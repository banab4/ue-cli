import unreal
import json

mesh_path = "{mesh_path}"
lod_index = {lod_index}
screen_size = {screen_size}
output_path = "{output_path}"

try:
    sm_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)

    if not mesh:
        with open(output_path, "w") as f:
            json.dump({"set": False, "error": "Mesh not found: " + mesh_path}, f)
    else:
        result = sm_subsystem.set_lod_screen_size(mesh, lod_index, float(screen_size))
        if result:
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            unreal.log("Set LOD screen size: " + mesh_path + " LOD" + str(lod_index))
            with open(output_path, "w") as f:
                json.dump({"set": True, "mesh_path": mesh_path, "lod_index": lod_index, "screen_size": screen_size}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"set": False, "error": "Failed to set LOD screen size. LOD index may be invalid."}, f)
except Exception as e:
    unreal.log_error("mesh_set_lod failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": str(e)}, f)
