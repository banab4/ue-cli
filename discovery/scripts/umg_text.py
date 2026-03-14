import unreal
import json

widget_name = "{widget_name}"
text_content = "{text_content}"
text_name = "{text_name}"
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

        text_block = unreal.WidgetTree.construct_widget(widget_tree, unreal.TextBlock, text_name)
        text_block.set_text(unreal.Text(text_content))

        if root:
            root.add_child(text_block)

        unreal.BlueprintEditorLibrary.compile_blueprint(widget_bp)
        unreal.EditorAssetLibrary.save_asset(w_path)
        unreal.log("Added text block: " + text_name + " to " + widget_name)
        with open(output_path, "w") as f:
            json.dump({"added": True, "text_name": text_name, "widget": w_path}, f)
except Exception as e:
    unreal.log_error("umg_text failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
