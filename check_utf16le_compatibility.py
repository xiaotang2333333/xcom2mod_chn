#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs

def check_utf16le_compatibility(directory='cn'):
    """
    检查指定目录及其子目录中的所有文件是否可以用UTF-16 LE编码读取
    
    Args:
        directory: 要检查的目录，默认为当前目录
        
    Returns:
        dict: 包含检查结果的字典
    """
    results = {
        'utf16le_ok': [],      # 可以用UTF-16 LE正确读取的文件
        'utf16le_failed': [],  # 不能用UTF-16 LE读取的文件
        'other_errors': []     # 其他读取错误
    }
    
    if not os.path.exists(directory):
        print(f"错误: 路径 '{directory}' 不存在")
        results['other_errors'].append(f"路径 '{directory}' 不存在")
        return results
    
    # 获取所有文件
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    
    total_files = len(all_files)
    print(f"开始检查 {total_files} 个文件的UTF-16 LE兼容性...\n")
    
    if total_files == 0:
        print("未找到任何文件")
        return results
    
    for i, file_path in enumerate(all_files, 1):
        try:
            # 尝试用UTF-16 LE读取文件
            with codecs.open(file_path, 'r', encoding='utf-16-le') as f:
                content = f.read()
            
            # 如果能读取到内容，说明文件是UTF-16 LE编码
            results['utf16le_ok'].append(file_path)
            print(f"✅ [{i}/{total_files}] {file_path} - UTF-16 LE兼容")
            
        except UnicodeDecodeError:
            # UTF-16 LE解码失败
            results['utf16le_failed'].append(file_path)
            print(f"❌ [{i}/{total_files}] {file_path} - 不兼容UTF-16 LE")
            
        except Exception as e:
            # 其他错误（如权限问题、文件损坏等）
            error_msg = f"{file_path}: {e}"
            results['other_errors'].append(error_msg)
            print(f"⚠️  [{i}/{total_files}] {file_path} - 读取错误: {e}")
    
    return results

def detect_actual_encoding(file_path):
    """
    尝试检测文件的真实编码
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 检测到的编码，如果无法检测返回None
    """
    encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'ascii']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except:
            continue
    
    return None

def print_detailed_results(results):
    """打印详细的检查结果"""
    print("\n" + "="*80)
    print("UTF-16 LE兼容性检查结果")
    print("="*80)
    
    # 兼容UTF-16 LE的文件
    print(f"\n✅ 兼容UTF-16 LE的文件 ({len(results['utf16le_ok'])} 个):")
    if results['utf16le_ok']:
        for file_path in sorted(results['utf16le_ok']):
            print(f"  - {file_path}")
    else:
        print("  无")
    
    # 不兼容UTF-16 LE的文件
    print(f"\n❌ 不兼容UTF-16 LE的文件 ({len(results['utf16le_failed'])} 个):")
    if results['utf16le_failed']:
        for file_path in sorted(results['utf16le_failed']):
            # 尝试检测实际编码
            actual_encoding = detect_actual_encoding(file_path)
            if actual_encoding:
                print(f"  - {file_path} (实际编码: {actual_encoding})")
            else:
                print(f"  - {file_path} (无法确定编码)")
    else:
        print("  无 - 所有文件都兼容UTF-16 LE！")
    
    # 其他错误
    print(f"\n⚠️  读取错误的文件 ({len(results['other_errors'])} 个):")
    if results['other_errors']:
        for error in results['other_errors']:
            print(f"  - {error}")
    else:
        print("  无")
    
    # 统计信息
    total_checked = len(results['utf16le_ok']) + len(results['utf16le_failed']) + len(results['other_errors'])
    
    print(f"\n📊 统计信息:")
    print(f"  总共检查: {total_checked} 个文件")
    print(f"  UTF-16 LE兼容: {len(results['utf16le_ok'])} 个 ({len(results['utf16le_ok'])/total_checked*100:.1f}%)")
    print(f"  UTF-16 LE不兼容: {len(results['utf16le_failed'])} 个 ({len(results['utf16le_failed'])/total_checked*100:.1f}%)")
    print(f"  读取错误: {len(results['other_errors'])} 个 ({len(results['other_errors'])/total_checked*100:.1f}%)")

def main():
    """主函数"""
    # 如果提供了路径参数，使用该路径，否则使用当前目录
    directory = sys.argv[1] if len(sys.argv) > 1 else 'cn'
    
    print(f"开始检查目录: {os.path.abspath(directory)}")
    print("正在检查所有文件的UTF-16 LE兼容性...")
    print("=" * 80)
    
    results = check_utf16le_compatibility(directory)
    print_detailed_results(results)

if __name__ == "__main__":
    main()