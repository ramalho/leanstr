import sys
import unicodedata

sample = 'Aé\N{BLACK CHESS ROOK}\N{GRINNING FACE}\uFFFF\U000FFFFF' + chr(sys.maxunicode)

print('witdh byte[0]  bytes       code     char name')

char_width = 0
for i in range(sys.maxunicode + 1):
    c = chr(i)
    try:
        b = c.encode('utf8')
    except UnicodeEncodeError:
        continue
    if len(b) > char_width or c in sample:
        char_width = len(b)
        ustr = f'U+{i:04X}'
        dump = ':'.join(f'{n:02X}' for n in b)
        name = unicodedata.name(c, '(no name)')
        if name == '(no name)':
            c = ' '
        print(f'{char_width:5} {b[0]:08b} {dump:11} {ustr:8} {c:^4} {name}')
