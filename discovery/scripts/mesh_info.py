import unreal
import json

actor_name = "{actor_name}"
output_path = "{output_path}"

try:
    world = unreal.EditorLevelLibrary.get_editor_world()
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

    found = None
    for actor in actors:
        if actor.get_actor_label().lower() == actor_name.lower() or actor.get_name().lower() == actor_name.lower():
            found = actor
            break

    if not found:
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Actor not found: " + actor_name}, f)
    else:
        mesh_comp = found.get_component_by_class(unreal.StaticMeshComponent)
        if not mesh_comp:
            with open(output_path, "w") as f:
                json.dump({"found": False, "error": "No StaticMeshComponent on: " + actor_name}, f)
        else:
            mesh = mesh_comp.get_editor_property("static_mesh")
            if not mesh:
                with open(output_path, "w") as f:
                    json.dump({"found": False, "error": "No static mesh assigned on: " + actor_name}, f)
            else:
                sm_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
                lod_count = sm_subsystem.get_lod_count(mesh)

                info = {
                    "found": True,
                    "actor": actor_name,
                    "mesh_path": mesh.get_path_name(),
                    "mesh_name": mesh.get_name(),
                    "lod_count": lod_count,
                    "lods": []
                }

                for i in range(lod_count):
                    try:
                        verts = sm_subsystem.get_number_verts(mesh, i)
                        tris = sm_subsystem.get_number_triangles(mesh, i)
                        info["lods"].append({"lod": i, "vertices": verts, "triangles": tris})
                    except Exception:
                        info["lods"].append({"lod": i, "vertices": -1, "triangles": -1})

                # Collision info
                try:
                    body_setup = mesh.get_editor_property("body_setup")
                    if body_setup:
                        collision_type = str(body_setup.get_editor_property("collision_trace_flag"))
                        info["collision_type"] = collision_type
                except Exception:
                    pass

                # Materials
                try:
                    mat_count = mesh_comp.get_num_materials()
                    materials = []
                    for i in range(mat_count):
                        mat = mesh_comp.get_material(i)
                        materials.append(mat.get_path_name() if mat else "None")
                    info["materials"] = materials
                except Exception:
                    pass

                unreal.log("Mesh info: " + actor_name)
                with open(output_path, "w") as f:
                    json.dump(info, f)
except Exception as e:
    unreal.log_error("mesh_info failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"found": False, "error": str(e)}, f)
