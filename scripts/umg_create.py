import unreal

widget_name = "{widget_name}"
package_path = "/Game/UI"

factory = unreal.WidgetBlueprintFactory()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
widget_bp = asset_tools.create_asset(widget_name, package_path, unreal.WidgetBlueprint, factory)

if widget_bp:
    unreal.EditorAssetLibrary.save_asset(package_path + "/" + widget_name)
    unreal.log("Created widget blueprint: " + package_path + "/" + widget_name)
else:
    unreal.log_error("Failed to create widget blueprint: " + widget_name)
