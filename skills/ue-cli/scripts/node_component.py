import unreal

blueprint_name = "{blueprint_name}"
component_name = "{component_name}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    node = lib.add_get_component_node(blueprint, graph, component_name, unreal.Vector2D(node_pos_x, node_pos_y))
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.log("Added component getter node: " + component_name + " to " + blueprint_name)
