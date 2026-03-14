import unreal
import json

blueprint_name = "{blueprint_name}"
action_name = "{action_name}"
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
        node = lib.add_input_action_node(blueprint, graph, action_name, unreal.Vector2D(node_pos_x, node_pos_y))
        lib.compile_blueprint(blueprint)
        unreal.log("Added input action node: " + action_name + " to " + blueprint_name)
        with open(output_path, "w") as f:
            json.dump({"added": True, "action_name": action_name, "blueprint": bp_path}, f)
except Exception as e:
    unreal.log_error("node_input failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
