import unreal
import json

material_path = "{material_path}"
expression_class = "{expression_class}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}
output_path = "{output_path}"

try:
    mat_lib = unreal.MaterialEditingLibrary
    material = unreal.EditorAssetLibrary.load_asset(material_path)

    if not material:
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Material not found: " + material_path}, f)
    elif material.get_class().get_name() != "Material":
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Not a base Material. Got: " + material.get_class().get_name()}, f)
    else:
        # Resolve expression class
        expr_cls = getattr(unreal, expression_class, None)
        if not expr_cls:
            # Try with MaterialExpression prefix
            expr_cls = getattr(unreal, "MaterialExpression" + expression_class, None)
        if not expr_cls:
            with open(output_path, "w") as f:
                json.dump({"added": False, "error": "Unknown expression class: " + expression_class}, f)
        else:
            expr = mat_lib.create_material_expression(material, expr_cls, node_pos_x, node_pos_y)
            if expr:
                unreal.log("Added expression: " + expression_class + " to " + material_path)
                with open(output_path, "w") as f:
                    json.dump({
                        "added": True,
                        "material_path": material_path,
                        "expression_class": expr.get_class().get_name(),
                        "node_name": expr.get_name(),
                        "position": {"x": node_pos_x, "y": node_pos_y}
                    }, f)
            else:
                with open(output_path, "w") as f:
                    json.dump({"added": False, "error": "Failed to create expression"}, f)
except Exception as e:
    unreal.log_error("material_add_node failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
