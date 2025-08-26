import os
import re

chn_dir = "CHN"
int_dir = "INT"
out_dir = "MERGED"

os.makedirs(out_dir, exist_ok=True)

section_pattern = re.compile(r'^\[.*\]$')
kv_pattern = re.compile(r'^(.+?)\s*=\s*"(.*)"$')
chinese_pattern = re.compile(r'[\u4e00-\u9fff]')  # 用于检测中文字符

def parse_file(path):
    data = {}
    current_section = None
    with open(path, "r", encoding="utf-16le") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):  # 新增：跳过以分号开头的行
                continue
            if section_pattern.match(line):
                current_section = line
                data[current_section] = {}
            else:
                m = kv_pattern.match(line)
                if m:
                    # 如果没有section，自动加一个[DEFAULT]
                    if not current_section:
                        current_section = "[DEFAULT]"
                        data[current_section] = {}
                    key, val = m.groups()
                    data[current_section][key] = val
    return data

chn_files = {f for f in os.listdir(chn_dir) if f.lower().endswith(".chn")}
int_files = {f for f in os.listdir(int_dir) if f.lower().endswith(".int")}
common_basenames = {os.path.splitext(f)[0] for f in chn_files} & {os.path.splitext(f)[0] for f in int_files}

# 用于收集所有 en->cn 映射，避免重复
mapping = {}

for basename in common_basenames:
    file_cn = os.path.join(chn_dir, basename + ".chn")
    file_en = os.path.join(int_dir, basename + ".int")
    
    cn_data = parse_file(file_cn)
    en_data = parse_file(file_en)
    
    for section, en_kvs in en_data.items():
        cn_kvs = cn_data.get(section, {})
        for k, en_val in en_kvs.items():
            cn_val = cn_kvs.get(k, "")
            # 校验cn_val必须包含中文字符，且避免重复键值对
            if en_val and cn_val and chinese_pattern.search(cn_val):
                if en_val not in mapping or mapping[en_val] != cn_val:
                    mapping[en_val] = cn_val
    
    print(f"处理完成文件: {basename}")

# 输出所有 en->cn 映射到 mapping.txt
mapping_path = os.path.join(out_dir, "mapping.txt")
with open(mapping_path, "w", encoding="utf-8") as f:
    for en_val, cn_val in sorted(mapping.items()):
        f.write(f"{en_val} -> {cn_val}\n")
print(f"所有映射已保存到 {mapping_path}")
