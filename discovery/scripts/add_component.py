import unreal
import json

blueprint_path = "{blueprint_path}"
component_type = "{component_type}"
component_name = "{component_name}"
output_path = "{output_path}"

blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_path)
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": "Blueprint not found: " + blueprint_path}, f)
else:
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
    root_handle = handles[0] if handles else None

    comp_class = getattr(unreal, component_type, None)
    if not comp_class:
        unreal.log_error("Component type not found: " + component_type)
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Component type not found: " + component_type}, f)
    else:
        params = unreal.AddNewSubobjectParams()
        params.set_editor_property("parent_handle", root_handle)
        params.set_editor_property("blueprint_context", blueprint)
        params.set_editor_property("new_class", comp_class.static_class())

        result = subsystem.add_new_subobject(params)
        unreal.EditorAssetLibrary.save_asset(blueprint_path)
        unreal.log("Added component: " + component_type + " to " + blueprint_path)
        with open(output_path, "w") as f:
            json.dump({"added": True, "component_name": component_name, "component_type": component_type, "blueprint_path": blueprint_path}, f)
