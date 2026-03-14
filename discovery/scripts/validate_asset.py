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
        validator = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
        # Validate single asset
        result = validator.validate_asset(asset)
        # Result is EDataValidationResult enum
        result_str = str(result)
        is_valid = "VALID" in result_str.upper() and "INVALID" not in result_str.upper()

        unreal.log("Validated: " + asset_path + " = " + result_str)
        with open(output_path, "w") as f:
            json.dump({
                "valid": is_valid,
                "asset_path": asset_path,
                "result": result_str,
                "class": asset.get_class().get_name()
            }, f)
except Exception as e:
    unreal.log_error("validate_asset failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"valid": False, "error": str(e)}, f)
