import unreal
import json

action_name = "{action_name}"
key_name = "{key_name}"
shift = {shift}
ctrl = {ctrl}
alt = {alt}
output_path = "{output_path}"

input_settings = unreal.InputSettings.get_input_settings()

key = unreal.Key(key_name)
action_mapping = unreal.InputActionKeyMapping(
    action_name=action_name,
    key=key,
    shift=shift,
    ctrl=ctrl,
    alt=alt
)

input_settings.add_action_mapping(action_mapping)
input_settings.save_key_mappings()

unreal.log("Added input mapping: " + action_name + " -> " + key_name)
with open(output_path, "w") as f:
    json.dump({"added": True, "action_name": action_name, "key_name": key_name, "shift": shift, "ctrl": ctrl, "alt": alt}, f)
