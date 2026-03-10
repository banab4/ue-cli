import unreal

widget_name = "{widget_name}"
widget_element_name = "{widget_element_name}"
event_name = "{event_name}"

widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/UI/" + widget_name)

if not widget_bp:
    unreal.log_error("Widget blueprint not found: " + widget_name)
else:
    graph = widget_bp.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary

    lib.add_event_node(widget_bp, graph, event_name, unreal.Vector2D(0, 0))
    unreal.KismetEditorUtilities.compile_blueprint(widget_bp)
    unreal.EditorAssetLibrary.save_asset("/Game/UI/" + widget_name)
    unreal.log("Bound event: " + event_name + " on " + widget_element_name + " in " + widget_name)
