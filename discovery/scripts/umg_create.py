import unreal
import json

widget_name = "{widget_name}"
package_path = "{package_path}"
output_path = "{output_path}"
_package_path_set = True

try:
    pkg = package_path if (_package_path_set and package_path) else "/Game/UI"

    factory = unreal.WidgetBlueprintFactory()
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    widget_bp = asset_tools.create_asset(widget_name, pkg, unreal.WidgetBlueprint, factory)

    if widget_bp:
        full_path = pkg + "/" + widget_name
        unreal.EditorAssetLibrary.save_asset(full_path)
        unreal.log("Created widget blueprint: " + full_path)
        with open(output_path, "w") as f:
            json.dump({"created": True, "widget_path": full_path}, f)
    else:
        with open(output_path, "w") as f:
            json.dump({"created": False, "error": "Failed to create widget: " + widget_name}, f)
except Exception as e:
    unreal.log_error("umg_create failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"created": False, "error": str(e)}, f)
