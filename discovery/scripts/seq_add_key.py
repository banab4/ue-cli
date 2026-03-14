import unreal
import json

sequence_path = "{sequence_path}"
actor_name = "{actor_name}"
frame = {frame}
property_name = "{property_name}"
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
            # Find binding for this actor
            bindings = sequence.get_bindings()
            target_binding = None
            for b in bindings:
                if b.get_name().lower() == actor_name.lower():
                    target_binding = b
                    break
            if not target_binding:
                for b in bindings:
                    if actor_name.lower() in b.get_name().lower():
                        target_binding = b
                        break

            if not target_binding:
                with open(output_path, "w") as f:
                    json.dump({"added": False, "error": "No binding found for: " + actor_name + ". Add track first."}, f)
            else:
                # Add transform track if property is location/rotation/scale
                prop_lower = property_name.lower()
                tracks = target_binding.get_tracks()
                transform_track = None
                for t in tracks:
                    if "Transform" in t.get_class().get_name():
                        transform_track = t
                        break

                if not transform_track:
                    transform_track = target_binding.add_track(unreal.MovieScene3DTransformTrack)

                if transform_track:
                    sections = transform_track.get_sections()
                    if not sections:
                        section = transform_track.add_section()
                        section.set_range(0, 100)
                    unreal.EditorAssetLibrary.save_asset(sequence_path)
                    unreal.log("Added keyframe track for: " + actor_name)
                    with open(output_path, "w") as f:
                        json.dump({"added": True, "sequence_path": sequence_path, "actor": actor_name, "frame": frame, "property": property_name}, f)
                else:
                    with open(output_path, "w") as f:
                        json.dump({"added": False, "error": "Failed to add transform track"}, f)
except Exception as e:
    unreal.log_error("seq_add_key failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
