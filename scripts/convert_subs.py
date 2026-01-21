"""
import pysubs2
import chardet
from pathlib import Path

def convert_to_txt(input_path: str, output_path: str):
    # 1. 自动检测编码
    with open(input_path, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding']
        print(f"检测到初始编码: {encoding}")

    # 2. 尝试加载字幕（增加容错逻辑）
    try:
        # 如果检测到是 GB2312 或 GBK，直接升级到 GB18030 以获得更好的兼容性
        if encoding and encoding.lower() in ['gb2312', 'gbk', 'ascii']:
            encoding = 'gb18030'
        
        subs = pysubs2.load(input_path, encoding=encoding)
    except UnicodeDecodeError:
        print(f"警告: {encoding} 解码失败，正在尝试强制使用 GB18030...")
        subs = pysubs2.load(input_path, encoding='gb18030')

    # 3. 提取文本并写入（后续逻辑不变）
    lines = [line.plaintext for line in subs]
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"成功保存为 UTF-8 TXT: {output_path}")

if __name__ == "__main__":
    # 示例使用
    file_to_convert = "data/NeZha2_2025.srt" 
    if Path(file_to_convert).exists():
        convert_to_txt(file_to_convert, "output_text.txt")
"""