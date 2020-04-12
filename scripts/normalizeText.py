# normalizeText.py
# python3 normalizeText.py textFile

# Normalize Yup'ik Text

# Input: text file(s) with Yup'ik words
# Output: List of Types and Tokens per type in descending order
#         e.g. tau͡gaam     2020
#.             atqa     17
#              tengssutecuaraliyugnganritarpenga-qaa    1

# Normalization Steps:
# 1. lowercase
# 2. remove punctuation - but keep apostrohpe and hyphen
# 3. convert apostrophe to (U+02BC ʼ) and tiebar (U+0361 u͡g) and voiceless nasals (U+0304 m̄ n̄ and U+035E n͞g)
# 4. reject words with English maybe (?)

import sys
import re
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("textFiles", nargs='+', help="text filenames - 1 or more files")
parser.add_argument("-o", "--output", default="normalizeText.out.txt", help="normalized types and tokens per count from input file(s)")
args = parser.parse_args()


def main():
    totalTypesCounter = Counter()
    for filePath in args.textFiles:
        fileCounter = processFile(filePath)
        totalTypesCounter += fileCounter

    outputLines = []
    totalTypesCounterMostCommon = sorted(totalTypesCounter.most_common(), key=lambda i: (-i[1], i[0]))
    for types, tokens in totalTypesCounterMostCommon:
        outputLines.append("{:>}\t{}".format(tokens,types))

    with open(args.output, 'w') as outFile:
        outFile.write('\n'.join(outputLines))

def processFile(filePath):
    fileCounter = Counter()
    with open(filePath, 'r') as inFile:
        for line in inFile:
            for word in line.split():
                norm = normalizeRegex(word)
                if norm != '' and len(norm) > 1 and not isEnglish(norm):
                    fileCounter.update([norm,])
    return fileCounter

def normalizeRegex(word):
    norm = word.strip().lower()
    norm = re.sub('[^\s\w\'\-̄͡͞ńḿ]','', norm) # punctuation without \' and - and special characters
    norm = re.sub('[\d]','', norm) # remove digits, underscore
    norm = re.sub('^\'','', norm) # remove word initial apostrphe
    norm = re.sub('[\']','ʼ', norm) # convert apostrophe
    return norm

def isEnglish(word):
    for letter in ['b', 'd', 'f', 'h', 'j', 'o', 'x', 'z']:
        if letter in word:
            return True
    if re.search('ee', word) is not None:
        return True
#    for enclitic in ['-am','-amta','-ata','-atam','-gga','-ggem','-gguq','-ima','-kin','-kiq','-llam','-lli','-llu','-mi','-naa','-qaa','-tanem','-tang','-tuq','-wa','-gga']:
    return False


if __name__ == '__main__':
    main()
