import unreal
import json
import re

blueprint_path = "{blueprint_path}"
output_path = "{output_path}"

blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_path)
    with open(output_path, "w") as f:
        json.dump({"found": False, "error": "Blueprint not found: " + blueprint_path}, f)
else:
    try:
        bp_class = blueprint.get_class().get_name()
        lib = unreal.BlueprintEditorLibrary

        # Parent class: "Unknown" here, enriched by CLI post-processing
        parent = "Unknown"
        gen_class = None
        try:
            gen_class = lib.generated_class(blueprint)
        except Exception:
            pass

        # Components via SubobjectDataSubsystem + export_text parsing
        components = []
        try:
            subsys = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
            handles = subsys.k2_gather_subobject_data_for_blueprint(blueprint)
            for h in handles:
                try:
                    data = subsys.k2_find_subobject_data_from_handle(h)
                    if data:
                        export = data.export_text()
                        # Parse: WeakObjectPtr="/Script/Engine.SceneComponent'/Game/.../DefaultSceneRoot_GEN_VARIABLE'"
                        wp_match = re.search(r'WeakObjectPtr="([^"]*)"', export)
                        if wp_match:
                            wp = wp_match.group(1)
                            # Extract class: /Script/Engine.SceneComponent'...' → SceneComponent
                            cls_match = re.search(r'/[^.]+\.(\w+)\'', wp)
                            # Extract name: last part after : or / before '
                            name_match = re.search(r'[:/](\w+)\'?$', wp.split("'")[1] if "'" in wp else wp)
                            comp_class = cls_match.group(1) if cls_match else "Unknown"
                            comp_name = name_match.group(1) if name_match else "Unknown"
                            # Skip CDO entry (Default__*_C)
                            if "Default__" in wp:
                                continue
                            # Clean up GEN_VARIABLE suffix
                            comp_name = comp_name.replace("_GEN_VARIABLE", "")
                            components.append({"name": comp_name, "class": comp_class})
                except Exception:
                    components.append({"name": "(unreadable)", "class": "Unknown"})
        except Exception:
            pass

        # Graphs via find_event_graph / find_graph
        graphs = []
        try:
            eg = lib.find_event_graph(blueprint)
            if eg:
                graphs.append(eg.get_name())
        except Exception:
            pass
        try:
            # Try common graph names
            for gname in ["ConstructionScript", "UserConstructionScript"]:
                try:
                    g = lib.find_graph(blueprint, gname)
                    if g and g.get_name() not in graphs:
                        graphs.append(g.get_name())
                except Exception:
                    pass
        except Exception:
            pass

        unreal.log("BP info: " + blueprint_path)
        with open(output_path, "w") as f:
            json.dump({
                "found": True, "blueprint_path": blueprint_path,
                "class": bp_class, "parent_class": parent,
                "generated_class": gen_class.get_name() if gen_class else "Unknown",
                "components_count": len(components),
                "components": components,
                "variables": [],
                "graphs": graphs
            }, f)
    except Exception as e:
        unreal.log_error("bp_info failed: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Script error: " + str(e)}, f)
