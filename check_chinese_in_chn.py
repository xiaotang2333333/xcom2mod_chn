#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import re

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def contains_chinese(text: str) -> bool:
    return bool(CHINESE_PATTERN.search(text))

def check_chn_files_for_chinese(directory='.'):
    """
    检查指定目录下每个子文件夹中的所有.chn文件是否包含中文字符
    
    Args:
        directory: 要检查的目录，默认为当前目录
        
    Returns:
        dict: 包含检查结果的字典
    """
    results = {
        'has_chinese': [],          # 包含中文的文件
        'no_chinese': [],           # 不包含中文的文件
        'errors': [],               # 读取错误的文件
        'subfolders_no_chinese': [] # 所有.chn文件都不包含中文的子文件夹
    }
    
    if not os.path.exists(directory):
        print(f"错误: 路径 '{directory}' 不存在")
        results['errors'].append(f"路径 '{directory}' 不存在")
        return results
    
    # 获取所有子文件夹
    subfolders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
    
    if not subfolders:
        print("未找到任何子文件夹")
        return results
    
    print(f"开始检查 {len(subfolders)} 个子文件夹...\n")
    
    for subfolder in sorted(subfolders):
        subfolder_name = os.path.basename(subfolder)
        print(f"检查子文件夹: {subfolder_name}")
        print("-" * 50)
        
        # 统计当前子文件夹中的.chn文件
        chn_files = []
        for root, dirs, files in os.walk(subfolder):
            for file in files:
                if file.lower().endswith('.chn'):
                    chn_files.append(os.path.join(root, file))
        
        if not chn_files:
            print(f"子文件夹 {subfolder_name} 中没有.chn文件")
            print()
            continue
        
        # 检查当前子文件夹的所有.chn文件
        has_chinese_in_subfolder = False
        has_errors_in_subfolder = False
        
        for i, file_path in enumerate(chn_files, 1):
            try:
                # 使用UTF-16 LE编码读取文件
                with codecs.open(file_path, 'r', encoding='utf-16-le') as f:
                    content = f.read()
                
                # 检查是否包含中文
                if contains_chinese(content):
                    results['has_chinese'].append(file_path)
                    has_chinese_in_subfolder = True
                    print(f"✅ [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 包含中文")
                else:
                    results['no_chinese'].append(file_path)
                    print(f"❌ [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 不包含中文")
                    
            except UnicodeDecodeError:
                # 如果UTF-16 LE解码失败，尝试其他编码
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if contains_chinese(content):
                        results['has_chinese'].append(file_path)
                        has_chinese_in_subfolder = True
                        print(f"✅ [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 包含中文 (UTF-8)")
                    else:
                        results['no_chinese'].append(file_path)
                        print(f"❌ [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 不包含中文 (UTF-8)")
                        
                except Exception as e:
                    error_msg = f"{file_path}: {e}"
                    results['errors'].append(error_msg)
                    has_errors_in_subfolder = True
                    print(f"⚠️  [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 读取错误: {e}")
                    
            except Exception as e:
                error_msg = f"{file_path}: {e}"
                results['errors'].append(error_msg)
                has_errors_in_subfolder = True
                print(f"⚠️  [{i}/{len(chn_files)}] {os.path.basename(file_path)} - 读取错误: {e}")
        
        # 如果子文件夹中没有错误且所有文件都不包含中文，则添加到结果中
        if not has_chinese_in_subfolder and not has_errors_in_subfolder:
            results['subfolders_no_chinese'].append(subfolder_name)
            print(f"📌 子文件夹 {subfolder_name} 的所有.chn文件都不包含中文")
        
        print()
    
    return results

def print_results(results):
    """打印检查结果"""
    print("\n" + "="*80)
    print("检查结果汇总")
    print("="*80)
    
    # 所有.chn文件都不包含中文的子文件夹
    print(f"\n📌 所有.chn文件都不包含中文的子文件夹 ({len(results['subfolders_no_chinese'])} 个):")
    if results['subfolders_no_chinese']:
        for subfolder in sorted(results['subfolders_no_chinese']):
            print(f"  - {subfolder}")
    else:
        print("  无 - 所有子文件夹都至少有一个文件包含中文！")
    
    # 不包含中文的文件
    print(f"\n❌ 不包含中文的.chn文件 ({len(results['no_chinese'])} 个):")
    if results['no_chinese']:
        for file_path in sorted(results['no_chinese']):
            print(f"  - {file_path}")
    else:
        print("  无")
    
    # 包含中文的文件（仅显示统计）
    print(f"\n✅ 包含中文的.chn文件 ({len(results['has_chinese'])} 个)")
    print("  (详细信息已在上面的检查过程中显示)")
    
    # 错误信息
    print(f"\n⚠️  读取错误的文件 ({len(results['errors'])} 个):")
    if results['errors']:
        for error in results['errors']:
            print(f"  - {error}")
    else:
        print("  无")
    
    # 统计信息
    total_checked = len(results['has_chinese']) + len(results['no_chinese']) + len(results['errors'])
    
    print(f"\n📊 统计信息:")
    print(f"  总共检查: {total_checked} 个文件")
    print(f"  包含中文: {len(results['has_chinese'])} 个 ({len(results['has_chinese'])/total_checked*100:.1f}%)")
    print(f"  不包含中文: {len(results['no_chinese'])} 个 ({len(results['no_chinese'])/total_checked*100:.1f}%)")
    print(f"  读取错误: {len(results['errors'])} 个 ({len(results['errors'])/total_checked*100:.1f}%)")

def main():
    """主函数"""
    # 如果提供了路径参数，使用该路径，否则使用当前目录
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"开始检查目录: {os.path.abspath(directory)}")
    print("正在扫描所有.chn文件并检查是否包含中文字符...")
    print("=" * 80)
    
    results = check_chn_files_for_chinese(directory)
    print_results(results)

if __name__ == "__main__":
    main()