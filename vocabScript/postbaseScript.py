
import re
import pdb

outfile = []
lhs, rhs = ["", ""]
with open("YED_postbase.txt") as f:
    for line in f:
        if line.strip() == '':
            continue
        elif line[0] == '#':
            cat = line.strip().split(' ')[1]
            #pdb.set_trace()
            if len(cat) != 2:
                continue
            lhs, rhs = cat # VV, VN, NN, NV
            outfile.append('\nLEXICON {}'.format('NounPostbase' if lhs == 'N' else 'VerbPostbase'))
        else:
            postbase, definition = [x.strip() for x in line.split(" ", maxsplit=1)]
            postbase = re.sub(r'\d', '', postbase)
            if postbase[-1] == "-":
                postbase = postbase[:-1]
                postbase = re.sub(r'-', '–', postbase)
                postbase = re.sub(r'%', r'%%', postbase)
                postbase = re.sub(r':', r'%:', postbase)
                in2out = '-{0}[{1}→{2}]:{0}'.format(postbase, lhs, rhs)
                outstate = 'NounPostbase' if rhs == 'N' else 'VerbPostbase'
                outfile.append('{:45} {}; ! {}'.format(in2out, outstate, definition))
            else:
                postbase = re.sub(r'a\^e\b', 'e', postbase)
                postbase = re.sub(r'\(aq\*\)\b', '(ar*)', postbase)
                postbase = re.sub(r'q\*\b', 'r*', postbase)
                postbase = re.sub(r'q\b', 'r', postbase)
                postbase = re.sub(r'k\b', 'g', postbase)
                postbase = re.sub(r'ta\b', 'te', postbase)
                postbase = re.sub(r'n\b', 'te', postbase)
                postbase = re.sub(r'-', '–', postbase)
                postbase = re.sub(r'%', r'%%', postbase)
                postbase = re.sub(r':', r'%:', postbase)
                in2out = '-{0}[{1}→{2}]:{0}'.format(postbase, lhs, rhs)
                outstate = 'NounPostbase' if rhs == 'N' else 'VerbPostbase'
                outfile.append('{:45} {}; ! {}'.format(in2out, outstate, definition))





with open("esu-postbase.txt", 'w') as f:
    f.write('\n'.join(outfile))