from enum import Enum


class NormalizedPOS(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJ = "adj"
    ADV = "adv"
    PRON = "pron"
    NUM = "num"
    PROPN = "propn"
    AUX = "aux"        # 助词（的、了、得）
    PART = "part"     # 语气词（啊、吗、吧）
    CONJ = "conj"     # 连词（和、但）
    PREP = "prep"     # 介词（在、从、给）
    QTY = "qty"       # 量词（个、次、回）
    PUNCT = "punct"
    OTHER = "other"

class RawPOS(str, Enum):
    generalNoun = "generalNoun"
    personName = "personName"
    directorName = "directorName"
    locationNoun = "locationNoun"
    organizationName = "organizationName"
    geographicalName = "geographicalName"