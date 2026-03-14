import unreal
import json

actor_name = "{actor_name}"
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
        json.dump({"found": False, "error": "Actor not found: " + actor_name}, f)
else:
    try:
        label = found.get_actor_label()
        name = found.get_name()
        cls_name = found.get_class().get_name()
        loc = found.get_actor_location()
        rot = found.get_actor_rotation()
        scale = found.get_actor_scale3d()
        folder = str(found.get_folder_path())
        try:
            hidden = found.is_hidden_ed()
        except Exception:
            try:
                hidden = found.get_editor_property("bHidden")
            except Exception:
                hidden = False

        try:
            root = found.get_editor_property("root_component")
            mobility = str(root.get_editor_property("mobility")) if root else "Unknown"
        except Exception:
            mobility = "Unknown"

        components = []
        try:
            for comp in found.get_components_by_class(unreal.ActorComponent):
                comp_info = {"name": comp.get_name(), "class": comp.get_class().get_name()}
                components.append(comp_info)
        except Exception:
            pass

        unreal.log("Actor info: " + label)
        with open(output_path, "w") as f:
            json.dump({
                "found": True, "label": label, "name": name, "class": cls_name,
                "location": {"x": loc.x, "y": loc.y, "z": loc.z},
                "rotation": {"pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll},
                "scale": {"x": scale.x, "y": scale.y, "z": scale.z},
                "folder": folder, "hidden": hidden, "mobility": mobility,
                "components": components
            }, f)
    except Exception as e:
        unreal.log_error("actor_info failed: " + str(e))
        with open(output_path, "w") as f:
            json.dump({"found": False, "error": "Script error: " + str(e)}, f)
