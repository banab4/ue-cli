import unreal

blueprint_path = "{blueprint_path}"
component_type = "{component_type}"
component_name = "{component_name}"

blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_path)
else:
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handle = subsystem.add_new_subobject(
        unreal.AddNewSubobjectParams(
            parent_handle=subsystem.get_root_subobject(blueprint),
            blueprint_context=blueprint,
            new_class=unreal.EditorAssetLibrary.load_asset("/Script/Engine." + component_type).static_class() if False else getattr(unreal, component_type),
            object_name=component_name
        )
    )
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_asset(blueprint_path)
    unreal.log("Added component: " + component_name + " to " + blueprint_path)
