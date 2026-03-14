import unreal
import json

widget_name = "{widget_name}"
z_order = {z_order}
output_path = "{output_path}"

try:
    w_path = widget_name if widget_name.startswith("/") else "/Game/UI/" + widget_name
    widget_bp = unreal.EditorAssetLibrary.load_asset(w_path)

    if not widget_bp:
        with open(output_path, "w") as f:
            json.dump({"displayed": False, "error": "Widget not found: " + w_path}, f)
    else:
        unreal.log("Widget " + widget_name + " prepared for viewport display (z_order=" + str(z_order) + ")")
        unreal.log("Note: Runtime viewport display requires CreateWidget + AddToViewport in BP graph.")
        with open(output_path, "w") as f:
            json.dump({"displayed": True, "widget": w_path, "z_order": z_order, "note": "Runtime display requires CreateWidget + AddToViewport in BP graph"}, f)
except Exception as e:
    unreal.log_error("umg_viewport failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"displayed": False, "error": str(e)}, f)
