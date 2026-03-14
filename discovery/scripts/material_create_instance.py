import unreal
import json

parent_path = "{parent_path}"
instance_name = "{instance_name}"
package_path = "{package_path}"
output_path = "{output_path}"

try:
    parent = unreal.EditorAssetLibrary.load_asset(parent_path)
    if not parent:
        with open(output_path, "w") as f:
            json.dump({"created": False, "error": "Parent material not found: " + parent_path}, f)
    else:
        factory = unreal.MaterialInstanceConstantFactoryNew()
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        instance = asset_tools.create_asset(instance_name, package_path, unreal.MaterialInstanceConstant, factory)

        if instance:
            unreal.MaterialEditingLibrary.set_material_instance_parent(instance, parent)
            full_path = package_path + "/" + instance_name
            unreal.EditorAssetLibrary.save_asset(full_path)
            unreal.log("Created material instance: " + full_path)
            with open(output_path, "w") as f:
                json.dump({"created": True, "instance_path": full_path, "parent": parent_path}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"created": False, "error": "Failed to create instance: " + instance_name}, f)
except Exception as e:
    unreal.log_error("material_create_instance failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"created": False, "error": str(e)}, f)
