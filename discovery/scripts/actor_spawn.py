import unreal
import json

asset_path = "{asset_path}"
location_x = {location_x}
location_y = {location_y}
location_z = {location_z}
output_path = "{output_path}"

actor_subsystem = unreal.EditorActorSubsystem()

asset = unreal.EditorAssetLibrary.load_asset(asset_path)
if not asset:
    unreal.log_error("Asset not found: " + asset_path)
else:
    location = unreal.Vector(location_x, location_y, location_z)
    rotation = unreal.Rotator(0, 0, 0)
    actor = actor_subsystem.spawn_actor_from_object(asset, location, rotation)
    if actor:
        label = actor.get_actor_label()
        name = actor.get_name()
        loc = actor.get_actor_location()
        unreal.log("Spawned: " + name + " at " + str(loc))
        level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        level_subsystem.editor_invalidate_viewports()
        with open(output_path, "w") as f:
            json.dump({"label": label, "name": name, "location": {"x": loc.x, "y": loc.y, "z": loc.z}}, f)
    else:
        unreal.log_error("Failed to spawn actor from: " + asset_path)
