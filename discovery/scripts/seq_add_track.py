import unreal
import json

sequence_path = "{sequence_path}"
actor_name = "{actor_name}"
output_path = "{output_path}"

try:
    sequence = unreal.EditorAssetLibrary.load_asset(sequence_path)
    if not sequence:
        with open(output_path, "w") as f:
            json.dump({"added": False, "error": "Sequence not found: " + sequence_path}, f)
    else:
        world = unreal.EditorLevelLibrary.get_editor_world()
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
        found = None
        for actor in actors:
            if actor.get_actor_label().lower() == actor_name.lower() or actor.get_name().lower() == actor_name.lower():
                found = actor
                break

        if not found:
            with open(output_path, "w") as f:
                json.dump({"added": False, "error": "Actor not found: " + actor_name}, f)
        else:
            seq_lib = unreal.LevelSequenceEditorBlueprintLibrary
            # Open sequence first
            asset_subsystem = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
            asset_subsystem.open_editor_for_assets([sequence])

            # Add actor binding
            binding = sequence.add_possessable(found)
            if binding:
                unreal.EditorAssetLibrary.save_asset(sequence_path)
                unreal.log("Added actor track: " + actor_name)
                with open(output_path, "w") as f:
                    json.dump({"added": True, "sequence_path": sequence_path, "actor": actor_name, "binding_id": str(binding.get_id())}, f)
            else:
                with open(output_path, "w") as f:
                    json.dump({"added": False, "error": "Failed to add binding for: " + actor_name}, f)
except Exception as e:
    unreal.log_error("seq_add_track failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
