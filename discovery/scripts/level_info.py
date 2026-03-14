import unreal
import json

output_path = "{output_path}"

try:
    world = unreal.EditorLevelLibrary.get_editor_world()
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

    level_name = world.get_name() if world else "Unknown"
    level_path = world.get_path_name() if world else "Unknown"

    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
    actor_count = len(actors)

    # Count by class
    class_counts = {}
    for actor in actors:
        cls = actor.get_class().get_name()
        class_counts[cls] = class_counts.get(cls, 0) + 1

    # Sort by count descending
    sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
    top_classes = [{"class": k, "count": v} for k, v in sorted_classes[:20]]

    unreal.log("Level info: " + level_name)
    with open(output_path, "w") as f:
        json.dump({
            "level_name": level_name,
            "level_path": level_path,
            "actor_count": actor_count,
            "top_classes": top_classes
        }, f)
except Exception as e:
    unreal.log_error("level_info failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"error": str(e)}, f)
