import unreal

blueprint_name = "{blueprint_name}"
node_pos_x = {node_pos_x}
node_pos_y = {node_pos_y}

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    node = lib.add_self_reference_node(blueprint, graph, unreal.Vector2D(node_pos_x, node_pos_y))
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.log("Added self reference node to " + blueprint_name)
