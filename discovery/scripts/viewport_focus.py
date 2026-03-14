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
        json.dump({"focused": False, "error": "Actor not found: " + actor_name}, f)
else:
    actor_subsystem = unreal.EditorActorSubsystem()
    actor_subsystem.set_selected_level_actors([found])

    loc = found.get_actor_location()
    rot = unreal.Rotator(0, -30, 0)
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc + unreal.Vector(-500, 0, 300), rot)

    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.editor_invalidate_viewports()
    unreal.log("Focused on: " + actor_name)
    with open(output_path, "w") as f:
        json.dump({"focused": True, "actor": actor_name, "location": {"x": loc.x, "y": loc.y, "z": loc.z}}, f)
