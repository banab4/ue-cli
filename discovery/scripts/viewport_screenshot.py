import unreal
import json
import os

output_path = "{output_path}"
screenshot_path = "{screenshot_path}"

try:
    import shutil

    # Default screenshot path if not specified
    if not screenshot_path or screenshot_path == "{screenshot_path}":
        project_dir = unreal.Paths.project_saved_dir()
        screenshot_path = os.path.join(project_dir, "Screenshots", "viewport_capture.png")

    # Ensure target directory exists
    screenshot_dir = os.path.dirname(screenshot_path)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # take_high_res_screenshot saves to project Screenshots dir with the given filename
    # Use a temp filename to capture, then move to requested path
    project_dir = unreal.Paths.project_saved_dir()
    default_dir = os.path.join(project_dir, "Screenshots")
    temp_name = "ue_cli_capture_temp.png"
    temp_path = os.path.join(default_dir, temp_name)

    if not os.path.exists(default_dir):
        os.makedirs(default_dir)

    # Remove old temp if exists
    if os.path.exists(temp_path):
        os.remove(temp_path)

    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, temp_name)

    # Copy to requested path (take_high_res_screenshot is async, file may appear with delay)
    # Try to copy immediately; if temp doesn't exist yet, fall back to direct capture path
    if os.path.exists(temp_path):
        shutil.copy2(temp_path, screenshot_path)
        os.remove(temp_path)
    else:
        # Fallback: try direct path in case the API wrote there
        shutil.copy2(os.path.join(default_dir, temp_name), screenshot_path) if os.path.exists(os.path.join(default_dir, temp_name)) else None

    unreal.log("Screenshot saved: " + screenshot_path)
    with open(output_path, "w") as f:
        json.dump({"captured": True, "path": screenshot_path}, f)
except Exception as e:
    unreal.log_error("Screenshot failed: " + str(e))
    with open(output_path, "w") as f:
        json.dump({"captured": False, "error": str(e)}, f)
