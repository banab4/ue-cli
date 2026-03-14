import unreal
import json

material_path = "{material_path}"
param_name = "{param_name}"
param_type = "{param_type}"
param_value = "{param_value}"
output_path = "{output_path}"

mat_lib = unreal.MaterialEditingLibrary

material = unreal.EditorAssetLibrary.load_asset(material_path)

if not material:
    unreal.log_error("Material not found: " + material_path)
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": "Material not found: " + material_path}, f)
elif material.get_class().get_name() != "MaterialInstanceConstant":
    cls_name = material.get_class().get_name()
    unreal.log_error("Not a MaterialInstanceConstant: " + material_path + " (class: " + cls_name + ")")
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": "Only MaterialInstanceConstant is supported. Got: " + cls_name + ". Create a MaterialInstance first."}, f)
else:
    try:
        value = json.loads(param_value)

        if param_type.lower() == "scalar":
            mat_lib.set_material_instance_scalar_parameter_value(material, param_name, float(value))
        elif param_type.lower() == "vector":
            color = unreal.LinearColor(value[0], value[1], value[2], value[3] if len(value) > 3 else 1.0)
            mat_lib.set_material_instance_vector_parameter_value(material, param_name, color)
        elif param_type.lower() == "texture":
            texture = unreal.EditorAssetLibrary.load_asset(str(value))
            mat_lib.set_material_instance_texture_parameter_value(material, param_name, texture)

        unreal.EditorAssetLibrary.save_asset(material_path)
        unreal.log("Set param: " + param_name + " on " + material_path)
        with open(output_path, "w") as f:
            json.dump({"set": True, "material_path": material_path, "param_name": param_name, "param_type": param_type}, f)
    except Exception as e:
        unreal.log_error("Failed to set param: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"set": False, "error": str(e)}, f)
