import os
from charset_normalizer import from_bytes

target_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\268500"

for root, dirs, files in os.walk(target_path):
    loc_dir = os.path.join(root, "Localization")
    if os.path.isdir(loc_dir):
        for loc_root, _, loc_files in os.walk(loc_dir):
            for fname in loc_files:
                if fname.endswith(".chn"):
                    fpath = os.path.join(loc_root, fname)
                    with open(fpath, "rb") as f:
                        raw = f.read()

                    result = from_bytes(raw).best()  # 取最优猜测
                    if result is None:
                        print(f"{fpath}: unknown")
                        continue

                    enc = result.encoding.lower()
                    if enc not in ("utf_16"):
                        print(f"{fpath}: detected as {enc}, confidence={result.chaos:.3f}")

