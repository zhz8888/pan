import os
import subprocess
import shutil

def get_size(start_path):
    """计算单个文件的大小"""
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    else:
        return 0

def compress_and_copy_large_files(directory, target_directory):
    """遍历目录，找到大于1GB的文件，使用7zip分卷压缩，并复制到目标目录"""
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            file_size = get_size(file_path)
            if file_size > 1024*1024*1024:  # 大于1GB
                print(f"正在压缩大文件：{file_path}")
                # 使用7z命令进行分卷压缩
                base_name = os.path.splitext(file_path)[0]
                command = ['7z', 'a', '-v500m', f'{base_name}.7z', file_path]
                subprocess.run(command, check=True)

                # 构造目标路径
                target_base_name = os.path.join(target_directory, os.path.basename(base_name))
                # 复制生成的7z分卷文件到目标文件夹
                for file in os.listdir(os.path.dirname(file_path)):
                    if file.startswith(os.path.basename(base_name)) and (file.endswith('.7z') or '.7z.' in file):
                        source_file = os.path.join(os.path.dirname(file_path), file)
                        target_file = os.path.join(target_directory, file)
                        print(f"正在复制文件：{source_file} 到 {target_file}")
                        shutil.copy(source_file, target_file)

# 调用函数，指定需要遍历的目录和目标目录
directory_to_search = '${{ github.workspace }}/gdown-files'
target_directory = '${{ github.workspace }}/upload-files'
compress_and_copy_large_files(directory_to_search, target_directory)