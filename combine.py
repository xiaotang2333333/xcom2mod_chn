import os
import re

chn_dir = "C:\\Users\\65717\\Desktop\\chn\\CHN"
int_dir = "C:\\Users\\65717\\Desktop\\chn\\INT"
out_dir = "C:\\Users\\65717\\Desktop\\chn\\MERGED"

os.makedirs(out_dir, exist_ok=True)

section_pattern = re.compile(r'^\[.*\]$')
kv_pattern = re.compile(r'^(.+?)\s*=\s*"(.*)"$')

def parse_file(path):
    data = {}
    current_section = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
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

# 获取两个目录下的相同文件名

chn_files = set(os.listdir(chn_dir))
int_files = set(os.listdir(int_dir))
common_files = chn_files & int_files

# 用于收集所有 en->cn 映射
mapping = set()

for filename in common_files:
    file_cn = os.path.join(chn_dir, filename)
    file_en = os.path.join(int_dir, filename)
    
    cn_data = parse_file(file_cn)
    en_data = parse_file(file_en)
    
    for section, en_kvs in en_data.items():
        cn_kvs = cn_data.get(section, {})
        for k, en_val in en_kvs.items():
            cn_val = cn_kvs.get(k, "")
            # 只收集有值的 en->cn
            if en_val and cn_val:
                mapping.add(f'{en_val} -> {cn_val}')
    
    print(f"处理完成文件: {filename}")

# 输出所有 en->cn 映射到 mapping.txt
mapping_path = os.path.join(out_dir, "mapping.txt")
with open(mapping_path, "w", encoding="utf-8") as f:
    for item in sorted(mapping):
        f.write(item + "\n")
print(f"所有映射已保存到 {mapping_path}")
