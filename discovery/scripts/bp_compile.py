import unreal
import json

blueprint_path = "{blueprint_path}"
output_path = "{output_path}"

blueprint = unreal.EditorAssetLibrary.load_asset(blueprint_path)

if not blueprint:
    unreal.log_error("Blueprint not found: " + blueprint_path)
    with open(output_path, "w") as f:
        json.dump({"compiled": False, "error": "Blueprint not found: " + blueprint_path}, f)
else:
    lib = unreal.BlueprintEditorLibrary
    lib.compile_blueprint(blueprint)
    unreal.EditorAssetLibrary.save_asset(blueprint_path)
    unreal.log("Compiled: " + blueprint_path)
    with open(output_path, "w") as f:
        json.dump({"compiled": True, "blueprint_path": blueprint_path}, f)
