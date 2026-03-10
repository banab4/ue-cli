import unreal

blueprint_name = "{blueprint_name}"
target_class = "{target_class}"
function_name = "{function_name}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    node = lib.add_function_node(blueprint, graph, target_class, function_name, unreal.Vector2D(node_pos_x, node_pos_y))
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.log("Added function node: " + function_name + " to " + blueprint_name)
