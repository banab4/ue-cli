import unreal
import json

location_x = {location_x}
location_y = {location_y}
location_z = {location_z}
rotation_pitch = {rotation_pitch}
rotation_yaw = {rotation_yaw}
rotation_roll = {rotation_roll}
output_path = "{output_path}"

try:
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    location = unreal.Vector(location_x, location_y, location_z)
    rotation = unreal.Rotator(rotation_roll, rotation_pitch, rotation_yaw)

    level_subsystem.set_level_viewport_camera_info(location, rotation)

    unreal.log("Set viewport camera")
    with open(output_path, "w") as f:
        json.dump({
            "set": True,
            "location": {"x": location_x, "y": location_y, "z": location_z},
            "rotation": {"pitch": rotation_pitch, "yaw": rotation_yaw, "roll": rotation_roll}
        }, f)
except Exception as e:
    unreal.log_error("viewport_camera failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"set": False, "error": str(e)}, f)
