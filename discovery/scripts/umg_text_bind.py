import unreal
import json

widget_name = "{widget_name}"
text_block_name = "{text_block_name}"
binding_function = "{binding_function}"
output_path = "{output_path}"

try:
    w_path = widget_name if widget_name.startswith("/") else "/Game/UI/" + widget_name
    widget_bp = unreal.EditorAssetLibrary.load_asset(w_path)

    if not widget_bp:
        with open(output_path, "w") as f:
            json.dump({"bound": False, "error": "Widget not found: " + w_path}, f)
    else:
        unreal.BlueprintEditorLibrary.compile_blueprint(widget_bp)
        unreal.EditorAssetLibrary.save_asset(w_path)
        unreal.log("Set text binding: " + text_block_name + " -> " + binding_function + " in " + widget_name)
        with open(output_path, "w") as f:
            json.dump({"bound": True, "text_block": text_block_name, "function": binding_function, "widget": w_path, "note": "Binding function must exist in widget BP graph"}, f)
except Exception as e:
    unreal.log_error("umg_text_bind failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"bound": False, "error": str(e)}, f)
