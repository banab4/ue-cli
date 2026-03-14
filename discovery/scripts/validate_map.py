import unreal
import json

output_path = "{output_path}"

try:
    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "Unknown"

    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
    issues = []

    # Check for common map issues
    actor_count = len(actors)
    has_player_start = False
    has_light = False
    overlapping_actors = []

    for actor in actors:
        cls = actor.get_class().get_name()
        if cls == "PlayerStart":
            has_player_start = True
        if "Light" in cls:
            has_light = True

    if not has_player_start:
        issues.append("No PlayerStart found in level")
    if not has_light:
        issues.append("No light source found in level")

    is_valid = len(issues) == 0

    unreal.log("Map check: " + level_name)
    with open(output_path, "w") as f:
        json.dump({
            "valid": is_valid,
            "level_name": level_name,
            "actor_count": actor_count,
            "issues": issues
        }, f)
except Exception as e:
    unreal.log_error("validate_map failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"valid": False, "error": str(e)}, f)
