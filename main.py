import os
import shutil

target_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\268500"
src_root = os.path.join(os.getcwd(), "cn")
for mod_id in os.listdir(src_root):
    src_mod_path = os.path.join(src_root, mod_id, "Localization")
    tgt_mod_path = os.path.join(target_path, mod_id, "Localization")
    if not os.path.isdir(src_mod_path) or not os.path.isdir(tgt_mod_path):
        continue
    for file in os.listdir(src_mod_path):
        if file.endswith(".chn"):
            src_file = os.path.join(src_mod_path, file)
            tgt_file = os.path.join(tgt_mod_path, file)
            if not os.path.exists(tgt_file):
                shutil.copy2(src_file, tgt_file)
                mod_name = None
                mod_dir = os.path.join(target_path, mod_id)
                for fname in os.listdir(mod_dir):
                    if fname.endswith(".XComMod"):
                        mod_name = fname.split(".")[0]
                        break
                if mod_name:
                    print(f"已替换: {mod_name}")