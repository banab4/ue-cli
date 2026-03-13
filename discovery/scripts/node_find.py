import unreal
import json

blueprint_name = "{blueprint_name}"
search_term = "{search_term}"
output_path = "{output_path}"

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
    with open(output_path, "w") as f:
        json.dump({"error": "Blueprint not found: " + blueprint_name, "nodes": [], "total": 0}, f)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    nodes = lib.find_nodes(blueprint, graph, search_term)
    results = []
    for node in nodes:
        results.append({"comment": str(node.get_editor_property("NodeComment")), "node": str(node)})
    with open(output_path, "w") as f:
        json.dump({"nodes": results, "total": len(results)}, f)
    unreal.log("Found " + str(len(results)) + " nodes")
