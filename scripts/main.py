from enum import Enum
from lexical_analyzer.tokenizer_ltp import LTPTokenizer
from lexical_analyzer.analyzer import LexicalAnalyzer
from lexical_analyzer.io.data_loader import TextLoader
from lexical_analyzer.io.config_loader import config_loader

def main():
    text = TextLoader.load_from_file("data/NeZha2.txt")
    stopwords = config_loader("resources/stopwords.txt")
    pos_whitelist = config_loader("resources/pos_whitelist.txt")
    pos_blacklist = config_loader("resources/pos_blacklist.txt")

    tokenizer = LTPTokenizer()
    analyzer = LexicalAnalyzer(tokenizer, stopwords, pos_whitelist, pos_blacklist)

    result = analyzer.analyze(text)

    for token in result.tokens:
        print(token.word, token.pos.value)

    top_words = result.top_k(k=None)

    for pos, items in top_words.items():
        pos_str = pos.value if isinstance(pos, Enum) else pos
        print(pos_str, items)

if __name__ == "__main__":
    main()