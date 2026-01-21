# Lexical Analyzer

一个基于 LTP 的中文文本分析器，用于对中文文本进行分词、词性标注、词性归一化以及按词性统计高频词。

## 功能特性

当前已实现
- 基于LTP的中文分词
- 词性标注
- 统一的内部词性枚举
- Token数据结构
- 停用词过滤
- 词性黑白名单
- 按词性分组统计词频
- 按词性输出前K个高频词（自定义个数）

规划中
- `json`格式输出
- 接入`jieba`分词供选择

## 使用方法

### 1.安装依赖

建议使用uv:
```bash
uv sync
```
### 2.本地安装包
```bash
uv pip install -e .
```
### 3.使用命令行工具
```bash
lexical-analyzer --help
```
### 4.使用示例
```bash
lexical-analyzer data/sample.txt --stopwords resources/stopwords.txt --backlist resources/pos_blacklist.txt --topk 5 --out result.csv
```
参数说明：
- `--stopwords`：停用词文件路径
- `--whitelist`：词性白名单文件路径，默认（留空）为resources/pos_whitelist.txt
- `--backlist`：词性黑名单文件路径，默认（留空）为resources/pos_blacklist.txt
- `--topk`：输出前K个高频词，默认（留空）输出全部
- `--out`：导出到csv文件名，默认（留空）输出到终端

## 文件结构
```
lexical-analyzer/
├── README.md
├── pyproject.toml
├── src/
│   ├── lexical_analyzer/
│   │   ├── analyzer.py          # 核心分析流程
│   │   ├── tokenizer.py         # LTP 分词与词性标注
│   │   ├── token.py             # Token 数据结构
│   │   ├── result.py            # AnalysisResult 输出模型
│   │   ├── pos.py               # 统一词性枚举定义
│   │   ├── pos_mapper.py        # 外部词性 → 内部词性映射
│   │   ├── io/
│   │   │   ├── config_loader.py # 加载停用词 / 黑白名单
│   │   │   └── data_loader.py   # 文本加载工具
│   │   └── cli.py               # 命令行工具入口
│   ├── tests/
├── resources/
│   ├── stopwords.txt
│   ├── pos_whitelist.txt
│   └── pos_blacklist.txt
├── scripts/
│   └── main.py                  # 示例入口
├── data/
├── pyproject.toml
├── .python-version
├── .gitignore
└── uv.lock
```

## 设计理念

### 数据流
```
原始文本
  ↓
Tokenizer（分词 + POS）
  ↓
Token（word, pos）
  ↓
POS 归一化
  ↓
过滤（停用词 / 黑白名单）
  ↓
AnalysisResult
  ├─ 按词性分组
  └─ 统计词频 / Top-K

```
### 词性归一化

不同 NLP 工具的词性体系不一致，本项目使用内部统一的 `NormalizedPOS`：
```python
class NormalizedPOS(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJ = "adj"
    ADV = "adv"
    PRON = "pron"
    NUM = "num"
    PROPN = "propn"
    PUNCT = "punct"
    OTHER = "other"

```

### Token是最小语义单元

- 不可变
- 所有分析逻辑围绕Token流进行
```python
@dataclass(frozen=True)
class Token:
    word: str
    pos: NormalizedPOS

```
## 补充信息

- 虚拟环境 Python 版本：`3.10`

- 使用`uv add`添加ltp包会报错，初步判断是默认的`tokenizers==0.10.3`导致。报错提示安装rust进行编译，但安装`rust`后编译过程仍旧会报错。最后实行的解决办法是`uv add ltp "tokenizers>=0.11.0"`

- 本项目使用`src/`布局。

## License
MIT License