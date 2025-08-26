import os

target_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\268500"

count = 0
found_paths = []

# 遍历268500下的所有直接子目录
for subdir in os.listdir(target_path):
    full_path = os.path.join(target_path, subdir)
    if os.path.isdir(full_path):
        chn_path = os.path.join(full_path, "Localization", "CHN")
        if os.path.isdir(chn_path):
            count += 1
            found_paths.append(chn_path)

print(f"共有 {count} 个子目录包含 Localization\\CHN 文件夹")
for p in found_paths:
    print(p)
