import unreal
import json

filter_class = "{filter_class}"
output_path = "{output_path}"

world = unreal.EditorLevelLibrary.get_editor_world()

if filter_class and filter_class != "*":
    cls = getattr(unreal, filter_class, None)
    if not cls:
        unreal.log_error("Unknown class: " + filter_class)
        actors = []
    else:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, cls)
else:
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)

results = []
for actor in actors:
    label = actor.get_actor_label()
    name = actor.get_name()
    cls_name = actor.get_class().get_name()
    loc = actor.get_actor_location()
    rot = actor.get_actor_rotation()
    scale = actor.get_actor_scale3d()
    folder = str(actor.get_folder_path())
    results.append({
        "label": label,
        "name": name,
        "class": cls_name,
        "location": {"x": loc.x, "y": loc.y, "z": loc.z},
        "rotation": {"pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll},
        "scale": {"x": scale.x, "y": scale.y, "z": scale.z},
        "folder": folder
    })

with open(output_path, "w") as f:
    json.dump({"actors": results, "total": len(results)}, f)

unreal.log("Total: " + str(len(results)) + " actors")
