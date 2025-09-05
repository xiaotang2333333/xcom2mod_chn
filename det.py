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
                        print(f"{fpath}: unknown encoding")
                        continue

                    enc = result.encoding.lower()
                    print(f"{fpath}: detected as {enc}, chaos={result.chaos:.3f}")

                    # 已经是 utf-16/utf-16le/utf-16le-sig，跳过
                    if enc.startswith("utf-16"):
                        continue

                    # 遇到 utf-8 / gb18030 需要转码
                    if enc in ("utf-8", "gb18030"):
                        try:
                            text = raw.decode(enc)
                            with open(fpath, "w", encoding="utf-16") as fw:
                                fw.write(text)
                            print(f"{fpath}: converted to UTF-16LE with BOM")
                        except Exception as e:
                            print(f"{fpath}: convert failed - {e}")


