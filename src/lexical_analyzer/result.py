from dataclasses import dataclass
from typing import List, Dict
from collections import Counter
from lexical_analyzer.token import Token

@dataclass # 装饰器，自动生成 __init__ 和 __repr__ 方法
class AnalysisResult:
    tokens: List[Token] # 分词后的token列表
    pos_groups: Dict[str, List[Token]] = None # 按词性分组的token列表
    freq_groups: Dict[str, Counter] = None # 按词性分组的词频

    def __post_init__(self): # 初始化后调用，用于初始化pos_groups和freq_groups
        if self.pos_groups is None:
            self.pos_groups = {}
            for t in self.tokens:
                self.pos_groups.setdefault(t.pos, []).append(t)

        if self.freq_groups is None:
            self.freq_groups = {}
            for pos, group_tokens in self.pos_groups.items():
                counter = Counter(t.word for t in group_tokens)
                self.freq_groups[pos] = counter

    @classmethod # 类方法，不需要实例化就可以调用
    def from_tokens(cls, tokens: List[Token]) -> "AnalysisResult":
        return cls(tokens=tokens)
    
    def top_k(self, k: int | None = None) -> Dict[str, List[tuple]]:
        """
        返回每个词性下最常出现的前 k 个词
        """
        result = {}
        for pos, counter in self.freq_groups.items():
            result[pos] = counter.most_common(k)
        return result