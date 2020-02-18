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
    totalTypesCounterMostCommon = sorted(totalTypesCounter.most_common(), key=lambda i: (i[1], i[0]), reverse=True)
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
                if norm != '':
                    fileCounter.update([norm,])
    return fileCounter

def normalizeRegex(word):
    normL = word.strip().lower()
    normLP = re.sub('[^\s\w\'-]','', normL) # punctuation without \' and -
    normLPD = re.sub('[\d]','', normLP) # remove digit
    normLPDA = re.sub('[\']','ʼ', normLPD) # replace apostrophe
    return normLPDA

if __name__ == '__main__':
    main()
