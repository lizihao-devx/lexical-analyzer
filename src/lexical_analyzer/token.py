from dataclasses import dataclass
from .pos import NormalizedPOS


@dataclass(frozen=True)
class Token:
    """
    分析流程中的最小语义单元
    """
    word: str           # 词语本身
    pos: NormalizedPOS  # 归一化后的词性
