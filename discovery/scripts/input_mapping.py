import unreal
import json

action_name = "{action_name}"
key_name = "{key_name}"
shift = "{shift}"
ctrl = "{ctrl}"
alt = "{alt}"
output_path = "{output_path}"

try:
    input_settings = unreal.InputSettings.get_input_settings()

    key = unreal.Key(key_name)
    action_mapping = unreal.InputActionKeyMapping(
        action_name=action_name,
        key=key,
        shift=str(shift).lower() == "true",
        ctrl=str(ctrl).lower() == "true",
        alt=str(alt).lower() == "true"
    )

    input_settings.add_action_mapping(action_mapping)
    input_settings.save_key_mappings()

    unreal.log("Added input mapping: " + action_name + " -> " + key_name)
    with open(output_path, "w") as f:
        json.dump({"added": True, "action_name": action_name, "key_name": key_name}, f)
except Exception as e:
    unreal.log_error("input_mapping failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
