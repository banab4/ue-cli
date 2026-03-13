import unreal
import json

actor_name = "{actor_name}"
material_path = "{material_path}"
slot_index = {slot_index}
output_path = "{output_path}"

world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

found = None
for actor in actors:
    if actor.get_actor_label().lower() == actor_name.lower() or actor.get_name().lower() == actor_name.lower():
        found = actor
        break

if not found:
    unreal.log_error("Actor not found: " + actor_name)
    with open(output_path, "w") as f:
        json.dump({"applied": False, "error": "Actor not found: " + actor_name}, f)
else:
    material = unreal.EditorAssetLibrary.load_asset(material_path)
    if not material:
        unreal.log_error("Material not found: " + material_path)
        with open(output_path, "w") as f:
            json.dump({"applied": False, "error": "Material not found: " + material_path}, f)
    else:
        mesh_comp = found.get_component_by_class(unreal.StaticMeshComponent)
        if not mesh_comp:
            mesh_comp = found.get_component_by_class(unreal.SkeletalMeshComponent)

        if not mesh_comp:
            unreal.log_error("No mesh component found on: " + actor_name)
            with open(output_path, "w") as f:
                json.dump({"applied": False, "error": "No mesh component on: " + actor_name}, f)
        else:
            mesh_comp.set_material(slot_index, material)
            unreal.log("Applied material: " + material_path + " to " + actor_name + " slot " + str(slot_index))
            level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
            level_subsystem.editor_invalidate_viewports()
            with open(output_path, "w") as f:
                json.dump({"applied": True, "actor": actor_name, "material": material_path, "slot_index": slot_index}, f)
