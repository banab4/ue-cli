import unreal

widget_name = "{widget_name}"
button_name = "{button_name}"
button_text = "{button_text}"

widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/UI/" + widget_name)

if not widget_bp:
    unreal.log_error("Widget blueprint not found: " + widget_name)
else:
    widget_tree = widget_bp.get_editor_property("WidgetTree")
    root = widget_tree.get_editor_property("RootWidget")

    button = unreal.WidgetTree.construct_widget(widget_tree, unreal.Button, button_name)
    text_block = unreal.WidgetTree.construct_widget(widget_tree, unreal.TextBlock, button_name + "_Text")
    text_block.set_text(unreal.Text(button_text))
    button.add_child(text_block)

    if root:
        root.add_child(button)

    unreal.KismetEditorUtilities.compile_blueprint(widget_bp)
    unreal.EditorAssetLibrary.save_asset("/Game/UI/" + widget_name)
    unreal.log("Added button: " + button_name + " to " + widget_name)
