import unreal

widget_name = "{widget_name}"
z_order = {z_order}

widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/UI/" + widget_name)

if not widget_bp:
    unreal.log_error("Widget blueprint not found: " + widget_name)
else:
    widget_class = widget_bp.generated_class()
    subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
    widget_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))

    unreal.log("Widget " + widget_name + " prepared for viewport display (z_order=" + str(z_order) + ")")
    unreal.log("Note: Runtime viewport display requires game mode. Use CreateWidget + AddToViewport in BP graph.")
