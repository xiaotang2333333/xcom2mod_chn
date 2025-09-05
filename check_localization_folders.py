#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil

def check_and_fix_cn_subfolders(cn_path='cn'):
    """
    检查并修复cn文件夹下每个子文件夹，使其只包含Localization文件夹
    
    Args:
        cn_path: cn文件夹的路径，默认为'cn'
    
    Returns:
        dict: 包含检查和处理结果的字典
    """
    results = {
        'already_correct': [],        # 已经正确的子文件夹（只包含Localization）
        'fixed_other_content': [],    # 修复了其他内容的子文件夹
        'fixed_no_localization': [],  # 修复了没有Localization的子文件夹
        'deleted_empty': [],          # 删除的空文件夹
        'errors': []                  # 处理过程中出现的错误
    }
    
    if not os.path.exists(cn_path):
        print(f"错误: 路径 '{cn_path}' 不存在")
        results['errors'].append(f"路径 '{cn_path}' 不存在")
        return results
    
    # 获取cn目录下所有子文件夹
    try:
        subfolders = [f for f in os.listdir(cn_path) 
                     if os.path.isdir(os.path.join(cn_path, f))]
    except PermissionError:
        print(f"错误: 没有权限访问 '{cn_path}' 目录")
        results['errors'].append(f"没有权限访问 '{cn_path}' 目录")
        return results
    
    total_folders = len(subfolders)
    print(f"开始检查和处理 {total_folders} 个子文件夹...\n")
    
    for folder in subfolders:
        folder_path = os.path.join(cn_path, folder)
        
        try:
            # 获取子文件夹中的所有内容
            contents = os.listdir(folder_path)
            
            if not contents:
                # 空文件夹 - 删除
                print(f"📁 删除空文件夹: {folder}")
                os.rmdir(folder_path)
                results['deleted_empty'].append(folder)
                continue
            
            # 检查是否只包含Localization文件夹
            localization_exists = 'Localization' in contents
            has_other_items = len(contents) > 1 or (len(contents) == 1 and not localization_exists)
            
            if localization_exists and not has_other_items:
                # 已经正确 - 只包含Localization文件夹
                print(f"✅ 已正确: {folder} (只包含Localization)")
                results['already_correct'].append(folder)
                
            elif localization_exists and has_other_items:
                # 包含Localization和其他内容 - 删除其他文件
                print(f"⚠️  处理包含其他内容的文件夹: {folder}")
                print(f"   内容: {contents}")
                
                for item in contents:
                    if item != 'Localization':
                        item_path = os.path.join(folder_path, item)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            print(f"   删除目录: {item}")
                        else:
                            os.remove(item_path)
                            print(f"   删除文件: {item}")
                
                results['fixed_other_content'].append((folder, contents))
                print(f"   ✅ 处理完成: {folder}")
                
            else:
                # 没有Localization文件夹 - 创建Localization并移动所有内容
                print(f"❌ 处理没有Localization的文件夹: {folder}")
                print(f"   内容: {contents}")
                
                # 创建Localization文件夹
                localization_path = os.path.join(folder_path, 'Localization')
                os.makedirs(localization_path, exist_ok=True)
                print(f"   创建目录: Localization")
                
                # 移动所有内容到Localization文件夹
                for item in contents:
                    src_path = os.path.join(folder_path, item)
                    dst_path = os.path.join(localization_path, item)
                    
                    if os.path.isdir(src_path):
                        shutil.move(src_path, dst_path)
                        print(f"   移动目录: {item} -> Localization/{item}")
                    else:
                        shutil.move(src_path, dst_path)
                        print(f"   移动文件: {item} -> Localization/{item}")
                
                results['fixed_no_localization'].append((folder, contents))
                print(f"   ✅ 处理完成: {folder}")
                
        except PermissionError:
            error_msg = f"没有权限处理 '{folder}'"
            print(f"❌ 错误: {error_msg}")
            results['errors'].append(error_msg)
            continue
        except Exception as e:
            error_msg = f"处理 '{folder}' 时出错: {e}"
            print(f"❌ 错误: {error_msg}")
            results['errors'].append(error_msg)
            continue
    
    return results

def print_summary(results):
    """打印处理结果汇总"""
    print("\n" + "="*60)
    print("处理结果汇总")
    print("="*60)
    
    # 已经正确的文件夹
    print(f"\n✅ 已经正确的文件夹 ({len(results['already_correct'])} 个):")
    if results['already_correct']:
        for folder in sorted(results['already_correct']):
            print(f"  - {folder}")
    else:
        print("  无")
    
    # 修复了其他内容的文件夹
    print(f"\n🔄 修复了其他内容的文件夹 ({len(results['fixed_other_content'])} 个):")
    if results['fixed_other_content']:
        for folder, original_contents in sorted(results['fixed_other_content']):
            print(f"  - {folder}: 原内容 → {original_contents}")
    else:
        print("  无")
    
    # 修复了没有Localization的文件夹
    print(f"\n🔄 修复了没有Localization的文件夹 ({len(results['fixed_no_localization'])} 个):")
    if results['fixed_no_localization']:
        for folder, original_contents in sorted(results['fixed_no_localization']):
            print(f"  - {folder}: 原内容 → {original_contents}")
    else:
        print("  无")
    
    # 删除的空文件夹
    print(f"\n🗑️  删除的空文件夹 ({len(results['deleted_empty'])} 个):")
    if results['deleted_empty']:
        for folder in sorted(results['deleted_empty']):
            print(f"  - {folder}")
    else:
        print("  无")
    
    # 错误信息
    print(f"\n❌ 处理错误 ({len(results['errors'])} 个):")
    if results['errors']:
        for error in results['errors']:
            print(f"  - {error}")
    else:
        print("  无")
    
    # 统计信息
    total_processed = (len(results['already_correct']) + 
                      len(results['fixed_other_content']) + 
                      len(results['fixed_no_localization']) + 
                      len(results['deleted_empty']) + 
                      len(results['errors']))
    
    print(f"\n📊 统计信息:")
    print(f"  总共处理: {total_processed} 个子文件夹")
    print(f"  已经正确: {len(results['already_correct'])} 个")
    print(f"  修复完成: {len(results['fixed_other_content']) + len(results['fixed_no_localization'])} 个")
    print(f"  删除空文件夹: {len(results['deleted_empty'])} 个")
    print(f"  处理错误: {len(results['errors'])} 个")

if __name__ == "__main__":
    # 如果提供了路径参数，使用该路径，否则使用默认的'cn'
    cn_path = sys.argv[1] if len(sys.argv) > 1 else 'cn'
    
    print(f"开始检查和处理目录: {os.path.abspath(cn_path)}")
    print("=" * 60)
    
    results = check_and_fix_cn_subfolders(cn_path)
    print_summary(results)