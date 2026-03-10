import unreal

widget_name = "{widget_name}"
text_block_name = "{text_block_name}"
binding_function = "{binding_function}"

widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/UI/" + widget_name)

if not widget_bp:
    unreal.log_error("Widget blueprint not found: " + widget_name)
else:
    widget_tree = widget_bp.get_editor_property("WidgetTree")

    unreal.KismetEditorUtilities.compile_blueprint(widget_bp)
    unreal.EditorAssetLibrary.save_asset("/Game/UI/" + widget_name)
    unreal.log("Set text binding: " + text_block_name + " -> " + binding_function + " in " + widget_name)
