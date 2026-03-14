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
    bp_class = blueprint.get_class().get_name()
    parent = str(blueprint.get_editor_property("parent_class").get_name()) if blueprint.get_editor_property("parent_class") else "None"

    # Get components via SubobjectDataSubsystem
    components = []
    component_count = 0
    try:
        subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
        component_count = len(handles)
        for h in handles:
            try:
                result = subsystem.k2_find_subobject_data_from_handle(h)
                if result:
                    components.append(str(result))
            except Exception:
                components.append("(unreadable)")
    except Exception:
        pass

    # Get variables
    lib = unreal.BlueprintEditorLibrary
    variables = []
    try:
        var_list = lib.get_blueprint_variable_list(blueprint)
        for v in var_list:
            variables.append(str(v))
    except:
        pass

    # Get graphs
    graphs = []
    try:
        graph_list = lib.get_blueprint_graphs(blueprint)
        for g in graph_list:
            graphs.append(g.get_name())
    except:
        pass

    unreal.log("BP info: " + blueprint_path)
    with open(output_path, "w") as f:
        json.dump({
            "found": True, "blueprint_path": blueprint_path,
            "class": bp_class, "parent_class": parent,
            "components_count": component_count,
            "components": components,
            "variables": variables,
            "graphs": graphs
        }, f)
