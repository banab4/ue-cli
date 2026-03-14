import unreal
import json

asset_path = "{asset_path}"
output_path = "{output_path}"

asset = unreal.EditorAssetLibrary.load_asset(asset_path)

if not asset:
    unreal.log_error("Asset not found: " + asset_path)
    with open(output_path, "w") as f:
        json.dump({"found": False, "error": "Asset not found: " + asset_path}, f)
else:
    try:
        cls = asset.get_class()
        cls_name = cls.get_name()
        full_name = asset.get_full_name()
        path_name = asset.get_path_name()
        outer = asset.get_outermost().get_name() if asset.get_outermost() else ""

        metadata = {}
        try:
            subsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
            tags = subsystem.get_metadata_tag_values(asset_path)
            if tags:
                for key in tags:
                    metadata[str(key)] = str(tags[key])
        except Exception:
            pass

        unreal.log("Asset info: " + asset_path)
        with open(output_path, "w") as f:
            json.dump({"found": True, "asset_path": asset_path, "class": cls_name, "full_name": full_name, "path_name": path_name, "package": outer, "metadata": metadata}, f)
    except Exception as e:
        unreal.log_error("asset_info failed: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Script error: " + str(e)}, f)
