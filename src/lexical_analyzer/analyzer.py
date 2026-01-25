from dataclasses import replace
from typing import Iterable, List
from lexical_analyzer.token import Token
from lexical_analyzer.result import AnalysisResult
from lexical_analyzer.pos_mapper import normalize_pos

class LexicalAnalyzer:
    """
    词汇分析器

    功能：
        - 按词性分组
        - 统计每个词性的词频和高频词
    """
    def __init__(self, tokenizer, stopwords=None, pos_whitelist=None, pos_blacklist=None, pos_mapper=None):
        self.tokenizer = tokenizer
        self.stopwords = stopwords or set()
        self.pos_whitelist = pos_whitelist or set()
        self.pos_blacklist = pos_blacklist or set()
        self.pos_mapper = pos_mapper or normalize_pos
    def analyze(
        self, 
        text: str,
    ) -> AnalysisResult:
        """
        对文本进行词汇分析，返回结构化结果
        """
        # text = text.replace("\n", " ").strip()
        all_tokens: List[Token] = []

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            tokens = self._tokenize(line)
            tokens = self._pos_process(tokens)
            all_tokens.extend(tokens)

        return self._build_result(all_tokens)
    
    def _tokenize(self, text: str) -> List[Token]:
        raw_tokens = self.tokenizer.tokenize(text)  # List[Tuple[str, str]]
        # 转换为 Token 对象
        return [Token(word=w, pos=p) for w, p in raw_tokens]
    
    def _pos_process(self, tokens: Iterable[Token]) -> List[Token]:
        
        return [replace(token, pos=self.pos_mapper(token.pos)) for token in tokens]
    
    def _build_result(self, tokens: List[Token]) -> AnalysisResult:
        
        filtered_tokens = []
        
        for t in tokens:
            pos_str = t.pos.value if hasattr(t.pos, "value") else str(t.pos)

            if t.word in self.stopwords:
                continue
            if self.pos_whitelist and pos_str not in self.pos_whitelist:
                continue
            if self.pos_blacklist and pos_str in self.pos_blacklist:
                continue
            filtered_tokens.append(t)
        return AnalysisResult.from_tokens(filtered_tokens)