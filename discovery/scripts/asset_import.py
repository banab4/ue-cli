import unreal
import json

file_path = "{file_path}"
destination_path = "{destination_path}"
output_path = "{output_path}"

try:
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Build import task
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", file_path)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)

    asset_tools.import_asset_tasks([task])

    imported = task.get_editor_property("imported_object_paths")
    if imported and len(imported) > 0:
        paths = [str(p) for p in imported]
        unreal.log("Imported: " + str(paths))
        with open(output_path, "w") as f:
            json.dump({"imported": True, "file": file_path, "destination": destination_path, "assets": paths}, f)
    else:
        result = task.get_editor_property("result")
        with open(output_path, "w") as f:
            json.dump({"imported": False, "error": "Import returned no assets. File may not exist or format unsupported.", "file": file_path}, f)
except Exception as e:
    unreal.log_error("asset_import failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"imported": False, "error": str(e)}, f)
