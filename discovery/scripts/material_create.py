import unreal
import json

material_name = "{material_name}"
package_path = "{package_path}"
output_path = "{output_path}"

factory = unreal.MaterialFactoryNew()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

material = asset_tools.create_asset(material_name, package_path, unreal.Material, factory)

if material:
    full_path = package_path + "/" + material_name
    unreal.EditorAssetLibrary.save_asset(full_path)
    unreal.log("Created material: " + full_path)
    with open(output_path, "w") as f:
        json.dump({"created": True, "material_path": full_path}, f)
else:
    unreal.log_error("Failed to create material: " + material_name)
    with open(output_path, "w") as f:
        json.dump({"created": False, "error": "Failed to create material: " + material_name}, f)
