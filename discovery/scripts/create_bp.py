import unreal

name = "{name}"
parent_class_name = "{parent_class}"
package_path = "{package_path}"

factory = unreal.BlueprintFactory()

if parent_class_name:
    parent = unreal.EditorAssetLibrary.load_asset("/Script/Engine." + parent_class_name)
    if parent:
        factory.set_editor_property("ParentClass", parent.generated_class() if hasattr(parent, "generated_class") else parent)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
blueprint = asset_tools.create_asset(name, package_path, unreal.Blueprint, factory)

if blueprint:
    unreal.EditorAssetLibrary.save_asset(package_path + "/" + name)
    unreal.log("Created blueprint: " + package_path + "/" + name)
else:
    unreal.log_error("Failed to create blueprint: " + name)
