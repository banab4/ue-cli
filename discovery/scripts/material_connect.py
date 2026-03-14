import unreal
import json

material_path = "{material_path}"
from_expression_name = "{from_expression_name}"
from_output_name = "{from_output_name}"
to_target = "{to_target}"
to_input_name = "{to_input_name}"
output_path = "{output_path}"
_from_output_set = True
_to_input_set = True

try:
    mat_lib = unreal.MaterialEditingLibrary
    material = unreal.EditorAssetLibrary.load_asset(material_path)

    if not material:
        with open(output_path, "w") as f:
            json.dump({"connected": False, "error": "Material not found: " + material_path}, f)
    elif material.get_class().get_name() != "Material":
        with open(output_path, "w") as f:
            json.dump({"connected": False, "error": "Not a base Material. Got: " + material.get_class().get_name()}, f)
    else:
        # Find source expression by name
        expressions = material.get_editor_property("expressions")
        from_expr = None
        for expr in expressions:
            if expr.get_name() == from_expression_name or expr.get_class().get_name() == from_expression_name:
                from_expr = expr
                break

        if not from_expr:
            # Try partial match
            for expr in expressions:
                if from_expression_name.lower() in expr.get_name().lower() or from_expression_name.lower() in expr.get_class().get_name().lower():
                    from_expr = expr
                    break

        if not from_expr:
            expr_list = [e.get_class().get_name() + "(" + e.get_name() + ")" for e in expressions]
            with open(output_path, "w") as f:
                json.dump({"connected": False, "error": "Source expression not found: " + from_expression_name, "available": expr_list}, f)
        else:
            from_out = from_output_name if (_from_output_set and from_output_name) else ""
            to_in = to_input_name if (_to_input_set and to_input_name) else ""

            # Check if to_target is a material property (e.g., BaseColor, Normal, Metallic)
            property_map = {
                "basecolor": unreal.MaterialProperty.MP_BASE_COLOR,
                "metallic": unreal.MaterialProperty.MP_METALLIC,
                "specular": unreal.MaterialProperty.MP_SPECULAR,
                "roughness": unreal.MaterialProperty.MP_ROUGHNESS,
                "emissivecolor": unreal.MaterialProperty.MP_EMISSIVE_COLOR,
                "opacity": unreal.MaterialProperty.MP_OPACITY,
                "opacitymask": unreal.MaterialProperty.MP_OPACITY_MASK,
                "normal": unreal.MaterialProperty.MP_NORMAL,
                "worldpositionoffset": unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET,
                "ambientocclusion": unreal.MaterialProperty.MP_AMBIENT_OCCLUSION,
                "subsurfacecolor": unreal.MaterialProperty.MP_SUBSURFACE_COLOR,
            }

            prop = property_map.get(to_target.lower().replace(" ", ""), None)

            if prop is not None:
                result = mat_lib.connect_material_property(from_expr, from_out, prop)
                if result:
                    mat_lib.recompile_material(material)
                    unreal.log("Connected " + from_expression_name + " to " + to_target)
                    with open(output_path, "w") as f:
                        json.dump({"connected": True, "from": from_expression_name, "to_property": to_target}, f)
                else:
                    with open(output_path, "w") as f:
                        json.dump({"connected": False, "error": "Failed to connect to property: " + to_target}, f)
            else:
                # to_target is another expression name
                to_expr = None
                for expr in expressions:
                    if expr.get_name() == to_target or expr.get_class().get_name() == to_target:
                        to_expr = expr
                        break
                if not to_expr:
                    for expr in expressions:
                        if to_target.lower() in expr.get_name().lower() or to_target.lower() in expr.get_class().get_name().lower():
                            to_expr = expr
                            break

                if not to_expr:
                    with open(output_path, "w") as f:
                        json.dump({"connected": False, "error": "Target expression not found: " + to_target}, f)
                else:
                    result = mat_lib.connect_material_expressions(from_expr, from_out, to_expr, to_in)
                    if result:
                        mat_lib.recompile_material(material)
                        unreal.log("Connected " + from_expression_name + " to " + to_target)
                        with open(output_path, "w") as f:
                            json.dump({"connected": True, "from": from_expression_name, "to": to_target}, f)
                    else:
                        with open(output_path, "w") as f:
                            json.dump({"connected": False, "error": "Failed to connect expressions"}, f)
except Exception as e:
    unreal.log_error("material_connect failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"connected": False, "error": str(e)}, f)
