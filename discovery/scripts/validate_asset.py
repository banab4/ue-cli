import unreal
import json

asset_path = "{asset_path}"
output_path = "{output_path}"

try:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset:
        with open(output_path, "w") as f:
            json.dump({"valid": False, "error": "Asset not found: " + asset_path}, f)
    else:
        cls_name = asset.get_class().get_name()
        issues = []

        # Check if blueprint compiles
        if cls_name == "Blueprint":
            try:
                lib = unreal.BlueprintEditorLibrary
                lib.compile_blueprint(asset)
                # Check for compiler errors by recompiling
            except Exception as e:
                issues.append("Blueprint compile error: " + str(e))

        # Check asset references
        try:
            deps = unreal.EditorAssetLibrary.find_package_referencers_for_asset(asset_path)
            ref_count = len(deps) if deps else 0
        except Exception:
            ref_count = -1

        is_valid = len(issues) == 0

        unreal.log("Validated: " + asset_path)
        with open(output_path, "w") as f:
            json.dump({
                "valid": is_valid,
                "asset_path": asset_path,
                "class": cls_name,
                "issues": issues,
                "referencer_count": ref_count
            }, f)
except Exception as e:
    unreal.log_error("validate_asset failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"valid": False, "error": str(e)}, f)
