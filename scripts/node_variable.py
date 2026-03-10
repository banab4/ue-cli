import unreal

blueprint_name = "{blueprint_name}"
variable_name = "{variable_name}"
variable_type = "{variable_type}"
default_value = "{default_value}"

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    lib = unreal.BlueprintEditorLibrary
    lib.add_variable(blueprint, variable_name, variable_type, default_value)
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.log("Added variable: " + variable_name + " (" + variable_type + ") to " + blueprint_name)
