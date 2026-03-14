import unreal
import json

blueprint_name = "{blueprint_name}"
source_node_name = "{source_node_name}"
source_pin_name = "{source_pin_name}"
target_node_name = "{target_node_name}"
target_pin_name = "{target_pin_name}"
output_path = "{output_path}"

try:
    bp_path = blueprint_name if blueprint_name.startswith("/") else "/Game/Blueprints/" + blueprint_name
    blueprint = unreal.EditorAssetLibrary.load_asset(bp_path)

    if not blueprint:
        with open(output_path, "w") as f:
            json.dump({"connected": False, "error": "Blueprint not found: " + bp_path}, f)
    else:
        graph = blueprint.get_editor_property("UbergraphPages")[0]
        lib = unreal.BlueprintEditorLibrary
        lib.connect_pins(blueprint, graph, source_node_name, source_pin_name, target_node_name, target_pin_name)
        lib.compile_blueprint(blueprint)
        unreal.log("Connected: " + source_node_name + "." + source_pin_name + " -> " + target_node_name + "." + target_pin_name)
        with open(output_path, "w") as f:
            json.dump({"connected": True, "source": source_node_name + "." + source_pin_name, "target": target_node_name + "." + target_pin_name, "blueprint": bp_path}, f)
except Exception as e:
    unreal.log_error("node_connect failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"connected": False, "error": str(e)}, f)
