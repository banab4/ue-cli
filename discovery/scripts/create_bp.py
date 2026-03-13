import unreal
import json

name = "{name}"
parent_class_name = "{parent_class}"
package_path = "{package_path}"
output_path = "{output_path}"

factory = unreal.BlueprintFactory()

if parent_class_name:
    parent = unreal.EditorAssetLibrary.load_asset("/Script/Engine." + parent_class_name)
    if parent:
        factory.set_editor_property("ParentClass", parent.generated_class() if hasattr(parent, "generated_class") else parent)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
blueprint = asset_tools.create_asset(name, package_path, unreal.Blueprint, factory)

if blueprint:
    full_path = package_path + "/" + name
    unreal.EditorAssetLibrary.save_asset(full_path)
    unreal.log("Created blueprint: " + full_path)
    with open(output_path, "w") as f:
        json.dump({"created": True, "name": name, "path": full_path, "parent_class": parent_class_name}, f)
else:
    unreal.log_error("Failed to create blueprint: " + name)
    with open(output_path, "w") as f:
        json.dump({"created": False, "error": "Failed to create blueprint: " + name}, f)
