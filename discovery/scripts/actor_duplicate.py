import unreal
import json

actor_name = "{actor_name}"
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
        json.dump({"duplicated": False, "error": "Actor not found: " + actor_name}, f)
else:
    actor_subsystem = unreal.EditorActorSubsystem()
    actor_subsystem.set_selected_level_actors([found])
    duplicated = actor_subsystem.duplicate_selected_actors(world)

    if duplicated and len(duplicated) > 0:
        new_actor = duplicated[0]
        label = new_actor.get_actor_label()
        name = new_actor.get_name()
        loc = new_actor.get_actor_location()
        unreal.log("Duplicated: " + actor_name + " -> " + label)
        level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        level_subsystem.editor_invalidate_viewports()
        with open(output_path, "w") as f:
            json.dump({"duplicated": True, "original": actor_name, "new_label": label, "new_name": name, "location": {"x": loc.x, "y": loc.y, "z": loc.z}}, f)
    else:
        unreal.log_error("Failed to duplicate: " + actor_name)
        with open(output_path, "w") as f:
            json.dump({"duplicated": False, "error": "Failed to duplicate: " + actor_name}, f)
