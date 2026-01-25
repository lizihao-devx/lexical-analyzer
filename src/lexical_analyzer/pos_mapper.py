from .pos import NormalizedPOS

LTP_POS_MAP = {
    # 名词
    "n": NormalizedPOS.NOUN,
    "nh": NormalizedPOS.NOUN,
    "ni": NormalizedPOS.NOUN,
    "ns": NormalizedPOS.NOUN,
    "nt": NormalizedPOS.NOUN,
    "nz": NormalizedPOS.NOUN,

    # 动词
    "v": NormalizedPOS.VERB,
    "vd": NormalizedPOS.VERB,
    "vn": NormalizedPOS.VERB,

    # 形容词 / 副词
    "a": NormalizedPOS.ADJ,
    "d": NormalizedPOS.ADV,

    # 代词 / 数词
    "r": NormalizedPOS.PRON,
    "m": NormalizedPOS.NUM,

    # 专有名词
    "nr": NormalizedPOS.PROPN,
    # 助词
    "u": NormalizedPOS.AUX,

    # 语气词 / 叹词
    "y": NormalizedPOS.PART,
    "e": NormalizedPOS.PART,

    # 连词
    "c": NormalizedPOS.CONJ,

    # 介词
    "p": NormalizedPOS.PREP,

    # 量词
    "q": NormalizedPOS.QTY,

    # 标点
    "wp": NormalizedPOS.PUNCT,
}

def normalize_pos(raw_pos: str) -> NormalizedPOS:
    """
    将任意来源的词性标签归一化为内部标准 POS
    """
    if not raw_pos:
        return NormalizedPOS.OTHER

    return LTP_POS_MAP.get(raw_pos, NormalizedPOS.OTHER)

class RawPOSMapper:
    """保留LTP原始词性全称"""
    # LTP官方词性对照表
    RAW_POS_DICT = {
        "a": "adjective",
        "ni": "organization name",
        "b": "other noun-modifier",
        "nl": "location noun",
        "c": "conjunction",
        "ns": "geographical name",
        "d": "adverb",
        "nt": "temporal noun",
        "e": "exclamation",
        "nz": "other proper noun",
        "g": "morpheme",
        "o": "onomatopoeia",
        "h": "prefix",
        "p": "preposition",
        "i": "idiom",
        "q": "quantity",
        "j": "abbreviation",
        "r": "pronoun",
        "k": "suffix",
        "u": "auxiliary",
        "m": "number",
        "v": "verb",
        "n": "general noun",
        "wp": "punctuation",
        "nd": "direction noun",
        "ws": "foreign words",
        "nh": "person name",
        "x": "non-lexeme",
        "z": "descriptive words",
    }

    @staticmethod # 
    def map(raw_pos: str):
        if not raw_pos:
            return "other"
        return RawPOSMapper.RAW_POS_DICT.get(raw_pos, "other")