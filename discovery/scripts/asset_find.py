import unreal

search = "{search}"

registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = registry.get_all_assets()

results = []
search_lower = search.lower()

for asset_data in assets:
    name = str(asset_data.asset_name)
    path = str(asset_data.package_name)
    if search_lower in name.lower() or search_lower in path.lower():
        results.append({"name": name, "path": path + "." + name, "class": str(asset_data.asset_class_path.asset_name)})

if results:
    for r in results[:50]:
        unreal.log("FOUND: " + r["path"] + " [" + r["class"] + "]")
    if len(results) > 50:
        unreal.log("... and " + str(len(results) - 50) + " more")
    unreal.log("Total: " + str(len(results)) + " assets found")
else:
    unreal.log("No assets found matching: " + search)
