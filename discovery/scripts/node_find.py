import unreal

blueprint_name = "{blueprint_name}"
search_term = "{search_term}"

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    nodes = lib.find_nodes(blueprint, graph, search_term)
    for node in nodes:
        unreal.log("Found node: " + str(node.get_editor_property("NodeComment")) + " | " + str(node))
