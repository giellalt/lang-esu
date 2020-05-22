# runTest.py
# python3 script/runTest.py -g esu.gen.hfstol -a esu.ana.hfstol test/esu.pairs.gold/*

# Test Result Code:
#   0 = no output
#   1 = multiple outputs, none correct
#   2 = just one answer and correct
#   3 = multiple outputs, including correct

import sys
import os
import subprocess
import json
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-g","--generator",nargs="?", help="hfst generator filename to run tests with")
parser.add_argument("-a","--analyzer",nargs="?", help="hfst analyzer filename to run tests with")
parser.add_argument("testFiles", nargs='+', help="test filename(s)")
parser.add_argument("-d", "--resultDirectory", default="test/esu.pairs.testResults", help="directory for stored test results")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-v", "--verbose", action="store_true")
group1.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()

def main():
    if args.generator is None and args.analyzer is None:
        print("ERROR: No generator or parser given. Use flags [-g|-a] hfstName")

    if args.generator is not None:
        runTests("gen", args.generator)

    if args.analyzer is not None:
        runTests("ana", args.analyzer)

def runTests(genAna, hfstName):
    if not os.path.exists(args.resultDirectory):
        os.makedirs(args.resultDirectory)

    testsCounter = Counter()
    for testFilePath in args.testFiles:
        testFile = os.path.basename(testFilePath)
        currentTests = runTest(genAna, hfstName, testFilePath)

        filename, file_extension = os.path.splitext(testFile)
        file_extension = file_extension[1:]  # remove period in txt
        testResultFile = ".".join([filename,genAna,file_extension])

        if os.path.exists(os.path.join(args.resultDirectory, testResultFile)):
            previousTests = readPreviousTestFile(os.path.join(args.resultDirectory, testResultFile))
            compareTests(previousTests, currentTests)
        else:
            if not args.quiet:
                print("########## No Previous Test ##########".format(testFile))

        if not args.quiet:
            print("########## {}: {} SUMMARY ##########".format(genAna, testFile))
        passed = [x[2] for x in currentTests].count(2) + [x[2] for x in currentTests].count(3)
        count = len(currentTests)
        if not args.quiet:
            print("Current tests Passed: {}/{}".format(passed, count))
        testsCounter.update([x[2] for x in currentTests])
        
        writeTestFile(currentTests, args.resultDirectory, testResultFile)

    print("\n########## {}: {} TEST SUMMARY ##########".format(genAna, len(args.testFiles)))
    total = sum(testsCounter.values())
    print("Total Passed: {}/{}".format(testsCounter[2]+testsCounter[3], total))
    print("0 - {}".format(testsCounter[0]))
    print("1 - {}".format(testsCounter[1]))
    print("2 - {}".format(testsCounter[2]))
    print("3 - {}".format(testsCounter[3]))


def readTestFile(filename):
    testFile = []
    with open(filename, 'r') as f:
        testFile = [[x.strip() for x in line.split() if x != ''] for line in f]
    return testFile

def readPreviousTestFile(filename):
    testFile = []
    with open(filename, 'r') as f:
        testFile = [[x.strip() for x in line.split('\t') if x != ''] for line in f]
        testFile = [(x[0], x[1], int(x[2]), json.loads(x[3])) for x in testFile]  
    return testFile

def writeTestFile(outputTest, dirname, filename):
    outputFile = ["\t".join([t[0], t[1], str(t[2]), json.dumps(t[3], ensure_ascii=False)]) for t in outputTest]
    with open(os.path.join(dirname, filename), 'w') as out:
        out.write("\n".join(outputFile))

def runTest(genAna, hfstName, testFile):
    testFileData = readTestFile(testFile)
    if not args.quiet:
        print("\n########## {}: {} ##########".format(genAna, testFile))
    currentTests = []
    for underlying, surface in testFileData:
        if genAna == "gen":
            inputstring, outputstring = underlying, surface
        else: # genAna == "ana"
            inputstring, outputstring = surface, underlying

        completedProcess = subprocess.run(["echo \"{}\" | hfst-optimized-lookup {}".format(inputstring.replace("@:","@%:"), hfstName)], shell=True, capture_output=True)
        processResults = [line.decode("utf-8") for line in completedProcess.stdout.split()][1::2]
        processResults = [parse.replace("@%:","@:") for parse in processResults]

        testResultCode = -1
        if inputstring == processResults[0]: # not parseable in input has output 'error error +?' so no parse word is duplicated
            testResultCode = 0               # 0 = no output
            processResults = []              # remove duplicated input 
            if not args.quiet:
                print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
        elif outputstring in processResults:
            if len(processResults) == 1:
                testResultCode = 2          # 2 = just one answer and correct
                if args.verbose:
                    print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
            else:
                testResultCode = 3          # 3 = multiple outputs, including correct
                if args.verbose:
                # if not args.quiet:
                    print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
        else:
            testResultCode = 1              # 1 = multiple outputs, none correct
            if not args.quiet:
                print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))

        outputTest = (underlying, surface, testResultCode, processResults)
        currentTests.append(outputTest)
    return currentTests

def compareTests(previousTests, currentTests):
    changesCount = 0
    if not args.quiet:
        print("########## Previous -> Current Test ##########")
    for i in range(len(currentTests)):
        if previousTests[i][0] == currentTests[i][0] and previousTests[i][1] == currentTests[i][1]:
            if previousTests[i][2] != currentTests[i][2]:
                changesCount += 1
                print("{}\t{}\t{} -> {}\t{} -> {}".format(currentTests[i][0], currentTests[i][1], \
                                                          previousTests[i][2], currentTests[i][2], \
                                                          json.dumps(previousTests[i][3], ensure_ascii=False), json.dumps(currentTests[i][3], ensure_ascii=False)))
            else:
                if args.verbose:
                    print("{}\t{}\t{} -> {}\t{} -> {}".format(currentTests[i][0], currentTests[i][1], \
                                                          previousTests[i][2], currentTests[i][2], \
                                                          json.dumps(previousTests[i][3], ensure_ascii=False), json.dumps(currentTests[i][3], ensure_ascii=False)))
    if not args.quiet:
        print("########## Previous -> Current Test SUMMARY ##########")
        print("Previous tests Passed: {}/{}".format([x[2] for x in previousTests].count(2) + [x[2] for x in previousTests].count(3) , len(previousTests)))
        print("Prev -> Curr Count: {}".format(changesCount))


if __name__ == "__main__":
    main()
