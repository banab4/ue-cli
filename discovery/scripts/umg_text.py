import unreal

widget_name = "{widget_name}"
text_content = "{text_content}"
text_name = "{text_name}"

widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/UI/" + widget_name)

if not widget_bp:
    unreal.log_error("Widget blueprint not found: " + widget_name)
else:
    widget_tree = widget_bp.get_editor_property("WidgetTree")
    root = widget_tree.get_editor_property("RootWidget")

    text_block = unreal.WidgetTree.construct_widget(widget_tree, unreal.TextBlock, text_name)
    text_block.set_text(unreal.Text(text_content))

    if root:
        root.add_child(text_block)

    unreal.KismetEditorUtilities.compile_blueprint(widget_bp)
    unreal.EditorAssetLibrary.save_asset("/Game/UI/" + widget_name)
    unreal.log("Added text block: " + text_name + " to " + widget_name)
