import unreal
import json

widget_name = "{widget_name}"
button_name = "{button_name}"
button_text = "{button_text}"
output_path = "{output_path}"

try:
    w_path = widget_name if widget_name.startswith("/") else "/Game/UI/" + widget_name
    widget_bp = unreal.EditorAssetLibrary.load_asset(w_path)

    if not widget_bp:
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Widget not found: " + w_path}, f)
    else:
        widget_tree = widget_bp.get_editor_property("WidgetTree")
        root = widget_tree.get_editor_property("RootWidget")

        button = unreal.WidgetTree.construct_widget(widget_tree, unreal.Button, button_name)
        text_block = unreal.WidgetTree.construct_widget(widget_tree, unreal.TextBlock, button_name + "_Text")
        text_block.set_text(unreal.Text(button_text))
        button.add_child(text_block)

        if root:
            root.add_child(button)

        unreal.BlueprintEditorLibrary.compile_blueprint(widget_bp)
        unreal.EditorAssetLibrary.save_asset(w_path)
        unreal.log("Added button: " + button_name + " to " + widget_name)
        with open(output_path, "w") as f:
            json.dump({"added": True, "button_name": button_name, "widget": w_path}, f)
except Exception as e:
    unreal.log_error("umg_button failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
