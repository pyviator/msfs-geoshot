from pathlib import Path
import subprocess

PACKAGE_NAME = "msfs_screenshot_geotag"

root_project_path = Path(__file__).parent.parent
qtdesigner_folder = root_project_path / "qtdesigner"
forms_folder = root_project_path / PACKAGE_NAME / "gui" / "forms"

for ui_file_path in qtdesigner_folder.glob("*.ui"):
    output_file = forms_folder / f"{ui_file_path.stem}.py"
    print(f"Building {ui_file_path} to {output_file}")
    arguments = ["pyuic5", "-o", str(output_file), str(ui_file_path)]
    output = subprocess.check_output(arguments, text=True)

print("All UI files built.")