import unreal
import json

material_path = "{material_path}"
output_path = "{output_path}"

try:
    mat_lib = unreal.MaterialEditingLibrary
    material = unreal.EditorAssetLibrary.load_asset(material_path)

    if not material:
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Material not found: " + material_path}, f)
    else:
        cls_name = material.get_class().get_name()
        is_instance = cls_name == "MaterialInstanceConstant"

        params = []

        # Scalar parameters
        scalar_names = mat_lib.get_scalar_parameter_names(material)
        for name in scalar_names:
            entry = {"name": str(name), "type": "scalar"}
            if is_instance:
                entry["value"] = mat_lib.get_material_instance_scalar_parameter_value(material, name)
            params.append(entry)

        # Vector parameters
        vector_names = mat_lib.get_vector_parameter_names(material)
        for name in vector_names:
            entry = {"name": str(name), "type": "vector"}
            if is_instance:
                color = mat_lib.get_material_instance_vector_parameter_value(material, name)
                entry["value"] = [color.r, color.g, color.b, color.a]
            params.append(entry)

        # Texture parameters
        texture_names = mat_lib.get_texture_parameter_names(material)
        for name in texture_names:
            entry = {"name": str(name), "type": "texture"}
            if is_instance:
                tex = mat_lib.get_material_instance_texture_parameter_value(material, name)
                entry["value"] = tex.get_path_name() if tex else None
            params.append(entry)

        # Static switch parameters
        switch_names = mat_lib.get_static_switch_parameter_names(material)
        for name in switch_names:
            entry = {"name": str(name), "type": "static_switch"}
            if is_instance:
                entry["value"] = mat_lib.get_material_instance_static_switch_parameter_value(material, name)
            params.append(entry)

        unreal.log("Got params for: " + material_path)
        with open(output_path, "w") as f:
            json.dump({
                "found": True,
                "material_path": material_path,
                "class": cls_name,
                "parameter_count": len(params),
                "parameters": params
            }, f)
except Exception as e:
    unreal.log_error("material_get_param failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"found": False, "error": str(e)}, f)
