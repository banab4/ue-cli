import unreal
import json
import os

output_path = "{output_path}"
screenshot_path = "{screenshot_path}"

try:
    # Default screenshot path if not specified
    if not screenshot_path or screenshot_path == "{screenshot_path}":
        project_dir = unreal.Paths.project_saved_dir()
        screenshot_path = os.path.join(project_dir, "Screenshots", "viewport_capture.png")

    # Ensure directory exists
    screenshot_dir = os.path.dirname(screenshot_path)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Take high-res screenshot of active viewport
    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, screenshot_path)

    unreal.log("Screenshot saved: " + screenshot_path)
    with open(output_path, "w") as f:
        json.dump({"captured": True, "path": screenshot_path}, f)
except Exception as e:
    unreal.log_error("Screenshot failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"captured": False, "error": str(e)}, f)
