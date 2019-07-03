# vocabScript.py
# Lonny Strunk

import sys
import json
import re

def readDictionaryJson(filename):
    nouns = []
    verbs = []
    particles = []
    other = []
    particleNames = ["adverbial particle", "exclamatory particle", "\"addtionalInfo\": [\"particle", "conjunctive particle", "interjectional particle", "interrogative particle", "\"addtionalInfo\": [\"semi-particle", "\"addtionalInfo\": [\"functionally a particle", "predicative particle", "# particle", "addtionalInfo\": [\"essentially a particle", "imperative particle"]
    with open(filename, 'r') as f:
        for line in f:
            dictionary = json.loads(line)
            if any(particle in line for particle in particleNames):
                for wordDef in dictionary["keywordgloss"]:
                    if len(wordDef) == 1:
                            particles.append("{:22} EncliticOrEnd; ! ".format(re.sub(r'[0-9]', '', wordDef[0])))
                    else:
                        for word in wordDef[0]:
                            particles.append("{:22} EncliticOrEnd; ! {}".format(re.sub(r'[0-9]', '', word), "; ".join(wordDef[1]) if len(wordDef) == 2 else ""))
            else:
                for wordDef in dictionary["keywordgloss"]:
                    if len(wordDef) == 1:
                        other.append(line)
                    else:
                        for word in wordDef[0]:
                            if word[-1] == "-":
                                verbs.append("{:22} VerbPostbase; ! {}".format(re.sub(r'[0-9]', '', word), "; ".join(wordDef[1])))
                            else:
                                nouns.append("{:22} NounPostbase; ! {}".format(re.sub(r'[0-9]', '', word), "; ".join(wordDef[1])))

    return nouns, verbs, particles, other


if __name__ == "__main__":
    filename = sys.argv[1] # "YED_2012.json"
    nouns, verbs, particles, other = readDictionaryJson(filename)

    with open('esu-nouns.txt', 'w') as out:
        out.write("\n".join(nouns))
    with open('esu-verbs.txt', 'w') as out:
        out.write("\n".join(verbs))
    with open('esu-particles.txt', 'w') as out:
        out.write("\n".join(particles))
    with open('esu-other.txt', 'w') as out:
        out.write("".join(other))