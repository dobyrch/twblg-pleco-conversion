import re
import unicodedata

tone_map = {
    '\u0301': '2', # acute
    '\u0300': '3', # grave
    '\u0302': '5', # circumflex
    '\u0304': '7', # macron
    '\u030D': '8', # vertical line
    # Use 9 to indicate contractions
    # (pronounced with rising tone)
    '\u030B': '9', # double accute
}

d = f"({'|'.join(tone_map)})?"
no_d = ''.join(tone_map)

initial = '(?:b|p|ph|m|t|th|n|j|l|g|k|kh|ng|h|ts|tsh|s)'

final = re.sub('\s+', '', f"""(?:
    a{d}   (?:nn|m|n|ng|p|t|k|h|nnh)? |
    a{d}i  (?:nn|h|nnh)? |
    a{d}u  (?:nn|h|nnh)? |
    e{d}   (?:nn|ng|h|nnh|r)? |
    i{d}   (?:nn|m|n|ng|p|t|k|h|nnh)? |
    ia{d}  (?:nn|m|n|ng|p|t||k|h|nnh)? |
    ia{d}u (?:nn|h)? |
    io{d}  (?:ng|k|h)? |
    iu{d}  (?:nn|n|h|nnh)? |
    o{d}   (?:nn|m|ng|p|k|h|nnh)? |
    o{d}o  (?:h)? |
    u{d}   (?:n|t|h)? |
    ua{d}  (?:nn|n|ng|t|h)? |
    ua{d}i (?:nn|nnh)? |
    ue{d}  (?:h)? |
    u{d}i  (?:nn|h)? |
    n{d}g  (?:h)? |
    m{d}   (?:h)? |

    au{d}  (?:h)? |
    o{d}e  (?:h)? |
    oo{d}  (?:h)? |
    u{d}a  (?:nn|n|t|h)? |
    u{d}e  (?:h)? |
    ui{d}  (?:nn|h)?
)""")

tai_lo = re.compile(f"""
        (?<=[^a-z{no_d}])
        ({initial}?{final})
        (?=[^a-z{no_d}]|$)
    """, re.VERBOSE | re.IGNORECASE)


def tone_diacritic_to_number(string):
    # Add space since look-behind requires fixed-with pattern
    # (i.e. can't match [^a-z]|^)
    string = ' ' +  unicodedata.normalize('NFD', string)
    search_start = 1

    while match := tai_lo.search(string, search_start):
        search_start = match.end()
        word = re.sub(d, '', match[0])

        if word[1:].isupper():
            continue

        diacritic =  ''.join(match.groups(default='')[1:])
        assert len(diacritic) <= 1

        number = tone_map.get(diacritic)
        if not number:
            if word[-1] in 'ptkh':
                number = '4'
            else:
                number = '1'

        string = string[:match.start()] + word + number + string[match.end():]

    # Drop the extra space added at the beginning
    return string[1:]
