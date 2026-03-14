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

    b_shift = str(shift).lower() == "true"
    b_ctrl = str(ctrl).lower() == "true"
    b_alt = str(alt).lower() == "true"

    action_mapping = unreal.InputActionKeyMapping()
    action_mapping.set_editor_property("action_name", action_name)
    action_mapping.set_editor_property("shift", b_shift)
    action_mapping.set_editor_property("ctrl", b_ctrl)
    action_mapping.set_editor_property("alt", b_alt)

    # Set key via editor property
    key = unreal.Key()
    key.set_editor_property("key_name", key_name)
    action_mapping.set_editor_property("key", key)

    input_settings.add_action_mapping(action_mapping)
    input_settings.save_key_mappings()

    unreal.log("Added input mapping: " + action_name + " -> " + key_name)
    with open(output_path, "w") as f:
        json.dump({"added": True, "action_name": action_name, "key_name": key_name}, f)
except Exception as e:
    unreal.log_error("input_mapping failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"added": False, "error": str(e)}, f)
