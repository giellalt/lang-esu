# runAnalyzer.py
# cut -f2 test/corpus/bible_normalized_1.0.txt | python3 script/runAnalyzer.py -a esu.ana.hfstol -o bible_normalize_out.txt

import sys
import argparse
import subprocess
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("-a","--analyzer", nargs="?", help="hfst analyzer filename")
parser.add_argument('wordfile',  nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="word file, one word per line")
parser.add_argument("-o", "--output",  nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output: word results, one word per line")
args = parser.parse_args()

def main():
    for word in args.wordfile:
        completedProcess = subprocess.run(["echo \"{}\" | hfst-optimized-lookup {}".format(word.strip(), args.analyzer)], shell=True, capture_output=True)
        processResults = [line.decode("utf-8") for line in completedProcess.stdout.split()][1::2]

        if word.strip() == processResults[0]:
            args.output.write("{}\t{}\t{}\n".format(word.strip(),0,"[]"))
        else:
            args.output.write("{}\t{}\t{}\n".format(word.strip(),len(processResults), json.dumps(processResults, ensure_ascii=False)))

if __name__ == '__main__':
    main()