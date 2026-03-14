import unreal
import json

mesh_path = "{mesh_path}"
collision_type = "{collision_type}"
output_path = "{output_path}"

try:
    sm_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)

    if not mesh:
        with open(output_path, "w") as f:
            json.dump({"set": False, "error": "Mesh not found: " + mesh_path}, f)
    else:
        col_type = collision_type.lower().replace(" ", "").replace("_", "")

        type_map = {
            "box": 0,
            "sphere": 1,
            "capsule": 2,
            "ndop10x": 3,
            "ndop10y": 4,
            "ndop10z": 5,
            "ndop18": 6,
            "ndop26": 7,
            "copy": 8,
            "convex": 9,
        }

        if col_type == "box":
            count_before = sm_subsystem.get_simple_collision_count(mesh)
            sm_subsystem.add_simple_collisions(mesh, unreal.ScriptingCollisionShapeType.BOX)
            count_after = sm_subsystem.get_simple_collision_count(mesh)
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            unreal.log("Added box collision: " + mesh_path)
            with open(output_path, "w") as f:
                json.dump({"set": True, "mesh_path": mesh_path, "collision_type": "box", "collision_count": count_after}, f)
        elif col_type == "sphere":
            sm_subsystem.add_simple_collisions(mesh, unreal.ScriptingCollisionShapeType.SPHERE)
            count_after = sm_subsystem.get_simple_collision_count(mesh)
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            with open(output_path, "w") as f:
                json.dump({"set": True, "mesh_path": mesh_path, "collision_type": "sphere", "collision_count": count_after}, f)
        elif col_type == "capsule":
            sm_subsystem.add_simple_collisions(mesh, unreal.ScriptingCollisionShapeType.CAPSULE)
            count_after = sm_subsystem.get_simple_collision_count(mesh)
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            with open(output_path, "w") as f:
                json.dump({"set": True, "mesh_path": mesh_path, "collision_type": "capsule", "collision_count": count_after}, f)
        elif col_type in ("ndop10x", "ndop10y", "ndop10z", "ndop18", "ndop26"):
            shape = getattr(unreal.ScriptingCollisionShapeType, col_type.upper(), None)
            if shape:
                sm_subsystem.add_simple_collisions(mesh, shape)
                count_after = sm_subsystem.get_simple_collision_count(mesh)
                unreal.EditorAssetLibrary.save_asset(mesh_path)
                with open(output_path, "w") as f:
                    json.dump({"set": True, "mesh_path": mesh_path, "collision_type": col_type, "collision_count": count_after}, f)
            else:
                with open(output_path, "w") as f:
                    json.dump({"set": False, "error": "Unknown NDOP type: " + collision_type}, f)
        elif col_type == "removeall":
            sm_subsystem.remove_collisions(mesh)
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            with open(output_path, "w") as f:
                json.dump({"set": True, "mesh_path": mesh_path, "collision_type": "removed_all", "collision_count": 0}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"set": False, "error": "Unknown collision type: " + collision_type + ". Supported: box, sphere, capsule, ndop10x/y/z, ndop18, ndop26, removeall"}, f)
except Exception as e:
    unreal.log_error("mesh_collision failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": str(e)}, f)
