from lexical_analyzer.tokenizer_ltp import LTPTokenizer
from lexical_analyzer.analyzer import LexicalAnalyzer

text = "我喜欢自然语言处理。"

tokenizer = LTPTokenizer()
analyzer = LexicalAnalyzer(tokenizer)

result = analyzer.analyze(text)

for token in result.tokens:
    print(token)
