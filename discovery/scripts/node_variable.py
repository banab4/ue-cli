import unreal
import json

blueprint_name = "{blueprint_name}"
variable_name = "{variable_name}"
variable_type = "{variable_type}"
default_value = "{default_value}"
output_path = "{output_path}"

try:
    bp_path = blueprint_name if blueprint_name.startswith("/") else "/Game/Blueprints/" + blueprint_name
    blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)

    if not blueprint:
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Blueprint not found: " + bp_path}, f)
    else:
        lib = unreal.BlueprintEditorLibrary
        lib.add_variable(blueprint, variable_name, variable_type, default_value)
        lib.compile_blueprint(blueprint)
        unreal.log("Added variable: " + variable_name + " (" + variable_type + ") to " + blueprint_name)
        with open(output_path, "w") as f:
            json.dump({"added": True, "variable_name": variable_name, "variable_type": variable_type, "blueprint": bp_path}, f)
except Exception as e:
    unreal.log_error("node_variable failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
