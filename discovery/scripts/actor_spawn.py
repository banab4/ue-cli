import unreal

asset_path = "{asset_path}"
location_x = {location_x}
location_y = {location_y}
location_z = {location_z}

actor_subsystem = unreal.EditorActorSubsystem()

asset = unreal.EditorAssetLibrary.load_asset(asset_path)
if not asset:
    unreal.log_error("Asset not found: " + asset_path)
else:
    location = unreal.Vector(location_x, location_y, location_z)
    rotation = unreal.Rotator(0, 0, 0)
    actor = actor_subsystem.spawn_actor_from_object(asset, location, rotation)
    if actor:
        unreal.log("Spawned: " + actor.get_name() + " at " + str(location))
        level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        level_subsystem.editor_invalidate_viewports()
    else:
        unreal.log_error("Failed to spawn actor from: " + asset_path)
