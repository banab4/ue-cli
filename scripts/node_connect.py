import unreal

blueprint_name = "{blueprint_name}"
source_node_name = "{source_node_name}"
source_pin_name = "{source_pin_name}"
target_node_name = "{target_node_name}"
target_pin_name = "{target_pin_name}"

blueprint = unreal.EditorAssetLibrary.load_asset("/Game/Blueprints/" + blueprint_name)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_name)
else:
    graph = blueprint.get_editor_property("UbergraphPages")[0]
    lib = unreal.BlueprintEditorLibrary
    lib.connect_pins(blueprint, graph, source_node_name, source_pin_name, target_node_name, target_pin_name)
    unreal.KismetEditorUtilities.compile_blueprint(blueprint)
    unreal.log("Connected: " + source_node_name + "." + source_pin_name + " -> " + target_node_name + "." + target_pin_name)
