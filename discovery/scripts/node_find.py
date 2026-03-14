import unreal
import json

blueprint_name = "{blueprint_name}"
search_term = "{search_term}"
output_path = "{output_path}"

try:
    bp_path = blueprint_name if blueprint_name.startswith("/") else "/Game/Blueprints/" + blueprint_name
    blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)

    if not blueprint:
        with open(output_path, "w") as f:
            json.dump({"error": "Blueprint not found: " + bp_path, "nodes": [], "total": 0}, f)
    else:
        lib = unreal.BlueprintEditorLibrary
        graph = lib.find_event_graph(blueprint)
        nodes = lib.find_nodes(blueprint, graph, search_term)
        results = []
        for node in nodes:
            try:
                comment = str(node.get_editor_property("NodeComment"))
            except Exception:
                comment = ""
            results.append({"comment": comment, "node": str(node)})
        unreal.log("Found " + str(len(results)) + " nodes")
        with open(output_path, "w") as f:
            json.dump({"nodes": results, "total": len(results), "blueprint": bp_path}, f)
except Exception as e:
    unreal.log_error("node_find failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"error": str(e), "nodes": [], "total": 0}, f)
