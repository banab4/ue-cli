import unreal
import json

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

        # Parent class via generated_class → super_class
        parent = "Unknown"
        try:
            lib = unreal.BlueprintEditorLibrary
            gen_class = lib.generated_class(blueprint)
            if gen_class:
                super_cls = gen_class.get_super_class()
                parent = super_cls.get_name() if super_cls else "None"
        except Exception:
            try:
                parent_cls = blueprint.get_editor_property("parent_class")
                parent = parent_cls.get_name() if parent_cls else "None"
            except Exception:
                pass

        # Components via SimpleConstructionScript
        components = []
        try:
            scs = blueprint.get_editor_property("simple_construction_script")
            if scs:
                nodes = scs.get_all_nodes()
                for node in nodes:
                    try:
                        tmpl = node.get_editor_property("component_template")
                        if tmpl:
                            components.append({
                                "name": tmpl.get_name(),
                                "class": tmpl.get_class().get_name()
                            })
                    except Exception:
                        components.append({"name": "(unreadable)", "class": "Unknown"})
        except Exception:
            pass

        # Variables via BlueprintEditorLibrary
        lib = unreal.BlueprintEditorLibrary
        variables = []
        try:
            var_list = lib.get_blueprint_variable_list(blueprint)
            for v in var_list:
                try:
                    variables.append(v.get_editor_property("var_name").to_string())
                except Exception:
                    try:
                        variables.append(str(v.get_editor_property("var_name")))
                    except Exception:
                        variables.append(str(v))
        except Exception:
            pass

        # Graphs: uber_graph_pages + function_graphs
        graphs = []
        try:
            for page in blueprint.get_editor_property("uber_graph_pages"):
                graphs.append(page.get_name())
        except Exception:
            pass
        try:
            for fg in blueprint.get_editor_property("function_graphs"):
                graphs.append(fg.get_name())
        except Exception:
            pass

        unreal.log("BP info: " + blueprint_path)
        with open(output_path, "w") as f:
            json.dump({
                "found": True, "blueprint_path": blueprint_path,
                "class": bp_class, "parent_class": parent,
                "components_count": len(components),
                "components": components,
                "variables": variables,
                "graphs": graphs
            }, f)
    except Exception as e:
        unreal.log_error("bp_info failed: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Script error: " + str(e)}, f)
