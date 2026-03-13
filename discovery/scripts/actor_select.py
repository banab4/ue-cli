import unreal
import json

actor_name = "{actor_name}"
output_path = "{output_path}"

actor_subsystem = unreal.EditorActorSubsystem()
world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

found = None
for actor in actors:
    if actor.get_actor_label().lower() == actor_name.lower() or actor.get_name().lower() == actor_name.lower():
        found = actor
        break

if found:
    actor_subsystem.set_selected_level_actors([found])
    label = found.get_actor_label()
    name = found.get_name()
    unreal.log("Selected: " + actor_name)
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.editor_invalidate_viewports()
    with open(output_path, "w") as f:
        json.dump({"selected": True, "label": label, "name": name}, f)
else:
    unreal.log_error("Actor not found: " + actor_name)
    with open(output_path, "w") as f:
        json.dump({"selected": False, "error": "Actor not found: " + actor_name}, f)
