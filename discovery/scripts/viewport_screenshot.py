import unreal
import json
import os

output_path = "{output_path}"
screenshot_path = "{screenshot_path}"
_screenshot_param_set = True

try:
    project_dir = unreal.Paths.project_saved_dir()
    # UE saves high-res screenshots to Screenshots/WindowsEditor/
    screenshot_dir = os.path.join(project_dir, "Screenshots", "WindowsEditor")

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    if _screenshot_param_set and screenshot_path:
        capture_name = os.path.basename(screenshot_path) if screenshot_path else "viewport_capture.png"
    else:
        capture_name = "viewport_capture.png"

    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, capture_name)

    actual_path = os.path.join(screenshot_dir, capture_name)
    # Normalize to forward slashes for consistency
    actual_path = actual_path.replace("\\", "/")

    unreal.log("Screenshot queued: " + actual_path)
    with open(output_path, "w") as f:
        json.dump({
            "captured": True,
            "path": actual_path,
            "note": "Screenshot is async. File appears after next frame render."
        }, f)

except Exception as e:
    unreal.log_error("Screenshot failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"captured": False, "error": str(e)}, f)
