from lexical_analyzer.tokenizer import LTPTokenizer
import json

if __name__ == "__main__":
    tokenizer = LTPTokenizer()

    text = "我现在正使用哈工大的LTP进行中文分词和词性标注。"
    result = tokenizer.tokenize(text)

    # json_str = json.dumps(result, ensure_ascii=False, indent=4)

    print(f"原文本：\n{text}")
    # print(f"执行分词和词性标注：\n{json_str}")
    print(f"执行分词和词性标注：\n{result}")