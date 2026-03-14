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

        # List available graphs
        graphs = []
        eg = lib.find_event_graph(blueprint)
        if eg:
            graphs.append(eg.get_name())
        for gname in ["ConstructionScript", "UserConstructionScript"]:
            try:
                g = lib.find_graph(blueprint, gname)
                if g and g.get_name() not in graphs:
                    graphs.append(g.get_name())
            except Exception:
                pass

        # Note: EdGraph.nodes is protected in Python. Cannot iterate nodes directly.
        # Return graph info and suggest using bp_info for structure overview.
        unreal.log("node_find: graphs=" + str(graphs) + " search=" + search_term)
        with open(output_path, "w") as f:
            json.dump({
                "blueprint": bp_path,
                "graphs": graphs,
                "search_term": search_term,
                "nodes": [],
                "total": 0,
                "note": "EdGraph.nodes is protected in Python. Use bp_info for component/graph overview. Node operations (add/connect) work by name."
            }, f)
except Exception as e:
    unreal.log_error("node_find failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"error": str(e), "nodes": [], "total": 0}, f)
