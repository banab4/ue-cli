import unreal
import json

search = "{search}"
output_path = "{output_path}"

registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = registry.get_all_assets()

results = []
search_lower = search.lower()

for asset_data in assets:
    name = str(asset_data.asset_name)
    path = str(asset_data.package_name)
    if search_lower in name.lower() or search_lower in path.lower():
        results.append({"name": name, "path": path + "." + name, "class": str(asset_data.asset_class_path.asset_name)})

with open(output_path, "w") as f:
    json.dump({"assets": results, "total": len(results)}, f)

unreal.log("Total: " + str(len(results)) + " assets found")
