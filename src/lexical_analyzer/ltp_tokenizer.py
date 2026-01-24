from typing import List, Tuple
from ltp import LTP
import torch


class LTPTokenizer:
    """
    基于 LTP 的中文分词与词性标注器
    职责：
        - 对中文文本进行分词
        - 为每个词语标注词性（POS）
    """

    def __init__(
            self,
            model_name: str | None = None,
            device: str | None = None,
            user_dict: str | None = None,
            default_freq: int = 2
            ):
        """
        初始化 LTP 模型实例（重量级对象，建议全生命周期仅初始化一次）

        :param model_name: 可用的自定义模型路径名称，默认为None使用默认模型
        """
        # 加载模型
        if model_name:
            self._ltp = LTP(model_name=model_name)
        else:
            self._ltp = LTP("LTP/base1")

        # 选择设备
        if device is None:
            use_cuda = torch.cuda.is_available()
        elif device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError("CUDA requested but not available.")
            use_cuda = True
        elif device == "cpu":
            use_cuda = False
        else:
            raise ValueError(f"Unknown device: {device}")
        
        if user_dict:
            self._load_user_dict(user_dict, default_freq)
        
        # 根据设备迁移模型
        if use_cuda:
            self._ltp.to("cuda")
            self.device = "cuda"
        else:
            self.device = "cpu"

        print((f"[INFO] LTP initialized, torch device = {self.device}"))

    def _load_user_dict(self, path: str, default_freq: int):
        """
        从文件加载用户自定义词典
        格式：词语 权重（默认2）
             词语一
             词语二 3
             词语三 5
        """
        count = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                word = parts[0]
                freq = int(parts[1]) if len(parts) > 1 else default_freq

                self._ltp.add_words(word, freq)
                count += 1

        print(f"[INFO] Loaded {count} words from user dictionary: {path}")

    def tokenize(self, text: str) -> List[Tuple[str, str]]:
        """
        对文本进行分词并标注词性

        :param text: 输入原始文本
        :return: 由 (词语, 词性) 构成的列表
        """
        if not text or not text.strip():
            return []

        output = self._ltp(
            [text],
            tasks=["cws", "pos"]
        )  

        words = output["cws"][0]
        poses = output["pos"][0]

        return list(zip(words, poses))
