import unreal

actor_name = "{actor_name}"
location_x = {location_x}
location_y = {location_y}
location_z = {location_z}
rotation_pitch = {rotation_pitch}
rotation_yaw = {rotation_yaw}
rotation_roll = {rotation_roll}
scale_x = {scale_x}
scale_y = {scale_y}
scale_z = {scale_z}

actor_subsystem = unreal.EditorActorSubsystem()
world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

found = None
for actor in actors:
    if actor.get_name() == actor_name or actor.get_actor_label() == actor_name:
        found = actor
        break

if not found:
    unreal.log_error("Actor not found: " + actor_name)
else:
    location = unreal.Vector(location_x, location_y, location_z)
    rotation = unreal.Rotator(rotation_pitch, rotation_yaw, rotation_roll)
    scale = unreal.Vector(scale_x, scale_y, scale_z)
    transform = unreal.Transform(location=location, rotation=rotation, scale3d=scale)
    actor_subsystem.set_actor_transform(found, transform)
    unreal.log("Transformed: " + actor_name)
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.editor_invalidate_viewports()
