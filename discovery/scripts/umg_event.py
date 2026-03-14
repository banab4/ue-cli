import unreal
import json

widget_name = "{widget_name}"
widget_element_name = "{widget_element_name}"
event_name = "{event_name}"
output_path = "{output_path}"

try:
    w_path = widget_name if widget_name.startswith("/") else "/Game/UI/" + widget_name
    widget_bp = unreal.EditorAssetLibrary.load_asset(w_path)

    if not widget_bp:
        with open(output_path, "w") as f:
            json.dump({"bound": False, "error": "Widget not found: " + w_path}, f)
    else:
        graph = widget_bp.get_editor_property("UbergraphPages")[0]
        lib = unreal.BlueprintEditorLibrary
        lib.add_event_node(widget_bp, graph, event_name, unreal.Vector2D(0, 0))
        lib.compile_blueprint(widget_bp)
        unreal.EditorAssetLibrary.save_asset(w_path)
        unreal.log("Bound event: " + event_name + " on " + widget_element_name + " in " + widget_name)
        with open(output_path, "w") as f:
            json.dump({"bound": True, "event_name": event_name, "element": widget_element_name, "widget": w_path}, f)
except Exception as e:
    unreal.log_error("umg_event failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"bound": False, "error": str(e)}, f)
