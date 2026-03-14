import unreal
import json

sequence_path = "{sequence_path}"
action = "{action}"
output_path = "{output_path}"
_action_set = True

try:
    seq_lib = unreal.LevelSequenceEditorBlueprintLibrary

    sequence = unreal.EditorAssetLibrary.load_asset(sequence_path)
    if not sequence:
        with open(output_path, "w") as f:
            json.dump({"success": False, "error": "Sequence not found: " + sequence_path}, f)
    else:
        # Open sequence editor first
        asset_subsystem = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
        asset_subsystem.open_editor_for_assets([sequence])

        act = action.lower() if (_action_set and action) else "play"

        if act == "play":
            seq_lib.play()
            with open(output_path, "w") as f:
                json.dump({"success": True, "action": "play", "sequence_path": sequence_path}, f)
        elif act == "stop":
            seq_lib.stop_playback()
            with open(output_path, "w") as f:
                json.dump({"success": True, "action": "stop", "sequence_path": sequence_path}, f)
        elif act == "pause":
            seq_lib.pause()
            with open(output_path, "w") as f:
                json.dump({"success": True, "action": "pause", "sequence_path": sequence_path}, f)
        else:
            with open(output_path, "w") as f:
                json.dump({"success": False, "error": "Unknown action: " + action + ". Supported: play, stop, pause"}, f)

        unreal.log("Sequencer " + act + ": " + sequence_path)
except Exception as e:
    unreal.log_error("seq_playback failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"success": False, "error": str(e)}, f)
