import unreal

actor_name = "{actor_name}"

actor_subsystem = unreal.EditorActorSubsystem()
world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

found = None
for actor in actors:
    if actor.get_name() == actor_name or actor.get_actor_label() == actor_name:
        found = actor
        break

if found:
    actor_subsystem.set_selected_level_actors([found])
    unreal.log("Selected: " + actor_name)
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.editor_invalidate_viewports()
else:
    unreal.log_error("Actor not found: " + actor_name)
