import os
from charset_normalizer import from_bytes

target_path = r"cn"

for root, dirs, files in os.walk(target_path):
    loc_dir = os.path.join(root, "Localization")
    if os.path.isdir(loc_dir):
        for loc_root, _, loc_files in os.walk(loc_dir):
            for fname in loc_files:
                if fname.endswith(".chn"):
                    fpath = os.path.join(loc_root, fname)
                    with open(fpath, "rb") as f:
                        raw = f.read()

                    result = from_bytes(raw).best()
                    if result is None:
                        print(f"{fpath}: unknown")
                        continue

                    enc = result.encoding.lower()
                    if enc not in ("utf_16"):
                        print(f"{fpath}: detected as {enc}, confidence={result.chaos:.3f}")

                        # 检测为utf8或gb18030时，重新按utf16le保存
                        if enc in ("utf_8", "gb18030"):
                            try:
                                text = raw.decode(enc)
                                with open(fpath, "wb") as fw:
                                    fw.write(text.encode("utf-16le"))
                                print(f"{fpath}: converted to utf-16le")
                            except Exception as e:
                                print(f"{fpath}: convert failed - {e}")

