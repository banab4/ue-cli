import unreal
import json

material_path = "{material_path}"
from_expression_class = "{from_expression_class}"
from_output_name = "{from_output_name}"
to_target = "{to_target}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}
output_path = "{output_path}"
_from_output_set = True

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
        # Resolve expression class
        expr_cls = getattr(unreal, from_expression_class, None)
        if not expr_cls:
            expr_cls = getattr(unreal, "MaterialExpression" + from_expression_class, None)

        if not expr_cls:
            with open(output_path, "w") as f:
                json.dump({"connected": False, "error": "Unknown expression class: " + from_expression_class}, f)
        else:
            # Create expression and connect in one step
            expr = mat_lib.create_material_expression(material, expr_cls, node_pos_x, node_pos_y)
            if not expr:
                with open(output_path, "w") as f:
                    json.dump({"connected": False, "error": "Failed to create expression: " + from_expression_class}, f)
            else:
                from_out = from_output_name if (_from_output_set and from_output_name) else ""

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
                    result = mat_lib.connect_material_property(expr, from_out, prop)
                    if result:
                        mat_lib.recompile_material(material)
                        unreal.EditorAssetLibrary.save_asset(material_path)
                        unreal.log("Connected " + from_expression_class + " to " + to_target)
                        with open(output_path, "w") as f:
                            json.dump({
                                "connected": True,
                                "expression_class": expr.get_class().get_name(),
                                "node_name": expr.get_name(),
                                "from_output": from_out,
                                "to_property": to_target
                            }, f)
                    else:
                        with open(output_path, "w") as f:
                            json.dump({"connected": False, "error": "Failed to connect to property: " + to_target}, f)
                else:
                    with open(output_path, "w") as f:
                        json.dump({"connected": False, "error": "Unknown material property: " + to_target + ". Supported: BaseColor, Metallic, Specular, Roughness, EmissiveColor, Opacity, OpacityMask, Normal, WorldPositionOffset, AmbientOcclusion, SubsurfaceColor"}, f)
except Exception as e:
    unreal.log_error("material_connect failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"connected": False, "error": str(e)}, f)
