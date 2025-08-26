import os
import shutil

# Target path
target_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\268500\2683996590"

# Check if the target path exists
if not os.path.exists(target_path):
    print(f"Target path {target_path} does not exist.")
    exit(1)

# Check if there's a Localization directory
localization_path = os.path.join(target_path, "Localization")
if not os.path.exists(localization_path):
    print(f"No Localization directory found at {target_path}")
    exit(0)

# Create INT and CHN directories in the current directory if they don't exist
int_dir = os.path.join(os.getcwd(), "INT")
chn_dir = os.path.join(os.getcwd(), "CHN")

os.makedirs(int_dir, exist_ok=True)
os.makedirs(chn_dir, exist_ok=True)

# Recursively find all files in the Localization directory
for root, _, files in os.walk(localization_path):
    for file in files:
        file_path = os.path.join(root, file)
        
        # 目标目录和后缀判断
        if file.endswith(".int"):
            dest_dir = int_dir
        elif file.endswith(".chn"):
            dest_dir = chn_dir
        else:
            continue

        # 检查重名文件，自动添加数字后缀
        base, ext = os.path.splitext(file)
        dest_path = os.path.join(dest_dir, file)
        count = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{base}_{count}{ext}")
            count += 1

        shutil.copy2(file_path, dest_path)
        print(f"Copied {file_path} to {dest_path}")
