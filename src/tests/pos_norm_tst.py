from lexical_analyzer.pos_mapper import normalize_pos
from lexical_analyzer.pos import NormalizedPOS

assert normalize_pos("n") == NormalizedPOS.NOUN
assert normalize_pos("v") == NormalizedPOS.VERB
assert normalize_pos("xxx") == NormalizedPOS.OTHER

print("All tests passed!")