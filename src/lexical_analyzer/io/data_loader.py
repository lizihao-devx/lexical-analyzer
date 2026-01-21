from pathlib import Path


class TextLoader:
    @staticmethod # 静态方法，无需实例化即可调用
    def load_from_file(path: str, encoding: str = "utf-8") -> str:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"文本文件不存在: {path}")

        if not file_path.is_file():
            raise ValueError(f"路径不是文件: {path}")

        return file_path.read_text(encoding=encoding)
