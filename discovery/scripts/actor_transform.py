import unreal
import json

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
output_path = "{output_path}"

actor_subsystem = unreal.EditorActorSubsystem()
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
        json.dump({"transformed": False, "error": "Actor not found: " + actor_name}, f)
else:
    location = unreal.Vector(location_x, location_y, location_z)
    rotation = unreal.Rotator(rotation_roll, rotation_pitch, rotation_yaw)
    scale = unreal.Vector(scale_x, scale_y, scale_z)
    found.set_actor_location_and_rotation(location, rotation, False, True)
    found.set_actor_scale3d(scale)
    label = found.get_actor_label()
    name = found.get_name()
    loc = found.get_actor_location()
    rot = found.get_actor_rotation()
    sc = found.get_actor_scale3d()
    unreal.log("Transformed: " + actor_name)
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.editor_invalidate_viewports()
    with open(output_path, "w") as f:
        json.dump({"transformed": True, "label": label, "name": name, "location": {"x": loc.x, "y": loc.y, "z": loc.z}, "rotation": {"pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll}, "scale": {"x": sc.x, "y": sc.y, "z": sc.z}}, f)
