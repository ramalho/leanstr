import sanitize

def remove_bom():
    with open('War_and_Peace.txt', 'rb') as fp:
        body = fp.read()
    with open('War_and_Peace.txt', 'wb') as fp:
        fp.write(body[1:])

def find_non_latin1():
    with open('War_and_Peace.txt') as fp:
        lines = []
        for line in fp:
            line = (
                line.replace('’', "'")
                    .replace('‘', "'")
                    .replace('“', '"')
                    .replace('”', '"')
                    .replace('—', '-')
                    .replace('—', '-')
                    .replace('œ', 'oe')
                    .replace('æ', 'ae')
            )
            try:
                line.encode('ascii')
            except UnicodeEncodeError:
                print(line.rstrip())
                for c in line:
                    if ord(c) < 256:
                        print('.', end='')                    
                    else:
                        print('^', end='')
                print()
            lines.append(line)
    with open('War_and_Peace-LATIN-1.txt', 'w', encoding='latin1') as fp:
        fp.write('\n'.join(lines))

def find_non_ascii():
    with open('War_and_Peace-LATIN-1.txt', encoding='latin1') as fp:
        lines = []
        for line in fp:
            line = sanitize.asciize(line)
            try:
                line.encode('ascii')
            except UnicodeEncodeError:
                print(line.rstrip())
                for c in line:
                    if ord(c) < 128:
                        print('.', end='')                    
                    else:
                        print('^', end='')
                print()
            lines.append(line)


def convert_to_ascii():
    with open('War_and_Peace-LATIN-1.txt', encoding='latin-1') as fp:
        text = fp.read()
    with open('War_and_Peace-ASCII.txt', 'w', encoding='ascii') as fp:
        fp.write(sanitize.asciize(text))
    

if __name__=='__main__':
    # remove_bom()
    #find_non_latin1()
    # find_non_ascii()
    convert_to_ascii()
