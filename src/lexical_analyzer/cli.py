import argparse
import csv
from lexical_analyzer.ltp_tokenizer import LTPTokenizer
from lexical_analyzer.analyzer import LexicalAnalyzer
from lexical_analyzer.io.data_loader import TextLoader
from lexical_analyzer.io.config_loader import config_loader

def main():
    parser = argparse.ArgumentParser(
        description="Lexical Analyzer - Chinese text word/pos frequency analysis"
    )
    parser.add_argument("file", type=str, help="Path to the text file to analyze")
    parser.add_argument("--stopwords", type=str, default="resources/stopwords.txt", help="Path to stopwords file")
    parser.add_argument("--whitelist", type=str, default="resources/pos_whitelist.txt", help="Path to POS whitelist file")
    parser.add_argument("--blacklist", type=str, default="resources/pos_blacklist.txt", help="Path to POS blacklist file")
    parser.add_argument("--topk", type=int, default=None, help="Show top k frequent words per POS (default: all)")
    parser.add_argument("--out", type=str, default="", help="Output CSV file path")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default=None, help="Device to run LTP on (e.g., 'cpu' or 'cuda'; default: auto)")

    args = parser.parse_args()

    text = TextLoader.load_from_file(args.file)
    stopwords = config_loader(args.stopwords) if args.stopwords else set()
    pos_whitelist = config_loader(args.whitelist) if args.whitelist else set()
    pos_blacklist = config_loader(args.blacklist) if args.blacklist else set()

    tokenizer = LTPTokenizer(device=args.device)
    analyzer = LexicalAnalyzer(tokenizer, stopwords, pos_whitelist, pos_blacklist)

    result = analyzer.analyze(text)
    top_words = result.top_k(args.topk)

    # 打印到终端
    for pos, items in top_words.items():
        pos_str = pos.value if hasattr(pos, "value") else str(pos)
        print(f"{pos_str}: {items}")

    # 输出 CSV
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["POS", "Word", "Frequency"])
            for pos, items in top_words.items():
                pos_str = pos.value if hasattr(pos, "value") else str(pos)
                for word, freq in items:
                    writer.writerow([pos_str, word, freq])
        print(f"分析结果已保存到 {args.out}")
