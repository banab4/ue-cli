import unreal
import json

actor_name = "{actor_name}"
property_name = "{property_name}"
property_value = "{property_value}"
output_path = "{output_path}"

world = unreal.EditorLevelLibrary.get_editor_world()
actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

found = None
for actor in actors:
    if actor.get_actor_label().lower() == actor_name.lower() or actor.get_name().lower() == actor_name.lower():
        found = actor
        break

if not found:
    unreal.log_error("Actor not found: " + actor_name)
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": "Actor not found: " + actor_name}, f)
else:
    try:
        old_value = str(found.get_editor_property(property_name))
        # Try to convert value to appropriate type
        try:
            val = json.loads(property_value)
        except (json.JSONDecodeError, ValueError):
            val = property_value

        found.set_editor_property(property_name, val)
        new_value = str(found.get_editor_property(property_name))
        unreal.log("Set " + property_name + " on " + actor_name)
        level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        level_subsystem.editor_invalidate_viewports()
        with open(output_path, "w") as f:
            json.dump({"set": True, "actor": actor_name, "property": property_name, "old_value": old_value, "new_value": new_value}, f)
    except Exception as e:
        unreal.log_error("Failed to set property: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"set": False, "error": str(e)}, f)
