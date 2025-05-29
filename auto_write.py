import re
import os

base_path = "/Users/omidshojaeianzanjani/Desktop/programmings /pythonCode/University/Moscato2"
for n in range(7, 51):
    filename = f"GoogleDriveConnect_{n}.py"
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    with open(filepath, "r") as f:
        content = f.read()
    # Improved regex to handle spaces
    new_content = re.sub(
        r"(result_all_AICs)\s*\[\s*\d+\s*:\s*\d+\s*\]",
        r"\1[263:]",
        content
    )
    with open(filepath, "w") as f:
        f.write(new_content)
    print(f"Updated: {filename}")