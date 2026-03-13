import unreal

actor_subsystem = unreal.EditorActorSubsystem()
actor_subsystem.select_nothing()
unreal.log("Deselected all actors")

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level_subsystem.editor_invalidate_viewports()
