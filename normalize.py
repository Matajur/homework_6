import re

# normalization of file names

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "c", "ch", "sh", "sch", "", "y", "", "e", "ju", "ja", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    norm_name = name.translate(TRANS)
    dot_position = norm_name.rfind('.')
    if dot_position == -1:
        norm_name = re.sub(r'\W', '_', norm_name)
    else:
        norm_name = re.sub(
            r'\W', '_', norm_name[:dot_position]) + norm_name[dot_position:]
    return norm_name
