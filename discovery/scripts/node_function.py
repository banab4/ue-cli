import unreal
import json

blueprint_name = "{blueprint_name}"
target_class = "{target_class}"
function_name = "{function_name}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}
output_path = "{output_path}"

try:
    bp_path = blueprint_name if blueprint_name.startswith("/") else "/Game/Blueprints/" + blueprint_name
    blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)

    if not blueprint:
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Blueprint not found: " + bp_path}, f)
    else:
        lib = unreal.BlueprintEditorLibrary
        graph = lib.find_event_graph(blueprint)
        node = lib.add_function_node(blueprint, graph, target_class, function_name, unreal.Vector2D(node_pos_x, node_pos_y))
        lib.compile_blueprint(blueprint)
        unreal.log("Added function node: " + function_name + " to " + blueprint_name)
        with open(output_path, "w") as f:
            json.dump({"added": True, "function_name": function_name, "target_class": target_class, "blueprint": bp_path}, f)
except Exception as e:
    unreal.log_error("node_function failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
