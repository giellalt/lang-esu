# runTest.py
# python3 runTest.py esu.gen.hfst esu.pairs.gold/*

import sys
import os
import subprocess
import json
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("hfstName", help="hfst filename to run tests with")
parser.add_argument("testFiles", nargs='+', help="test filenames - 1 or more files")
parser.add_argument("-d", "--resultDirectory", default="esu.pairs.test", help="directory for stored test results")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()


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

def runTests(testFile):
    testFileData = readTestFile(testFile)
    if not args.quiet:
        print("\n########## {} ##########".format(testFile))
    currentTests = []
    for underlying, surface in testFileData:
        completedProcess = subprocess.run(["echo \"{}\" | hfst-lookup {}".format(underlying.replace("@:","@%:"), args.hfstName)], shell=True, capture_output=True)
        processResults = [line.decode("utf-8") for line in completedProcess.stdout.split()][1::3]

        testResultCode = -1
        if "+?" in processResults[0]:
            testResultCode = 0              # 0 = no output
            if not args.quiet:
                print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
        elif surface in processResults:
            if len(processResults) == 1:
                testResultCode = 1          # 1 = just one answer and correct
                if args.verbose:
                    print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
            else:
                testResultCode = 3          # 3 = multiple outputs, including correct
                if args.verbose:
                # if not args.quiet:
                    print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
        else:
            testResultCode = 2              # 2 = multiple outputs, none correct
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
        print("Previous tests Passed: {}/{}".format([x[2] for x in previousTests].count(1) + [x[2] for x in previousTests].count(3) , len(previousTests)))
        print("Prev -> Curr Count: {}".format(changesCount))


if __name__ == "__main__":
    if not os.path.exists(args.resultDirectory):
        os.makedirs(args.resultDirectory)

    testsCounter = Counter()
    for testFilePath in args.testFiles:
        testFile = os.path.basename(testFilePath)
        currentTests = runTests(testFilePath)

        if os.path.exists(os.path.join(args.resultDirectory, testFile)):
            previousTests = readPreviousTestFile(os.path.join(args.resultDirectory, testFile))
            compareTests(previousTests, currentTests)
        else:
            if not args.quiet:
                print("########## No Previous Test ##########".format(testFile))

        if not args.quiet:
            print("########## {} SUMMARY ##########".format(testFile))
        passed = [x[2] for x in currentTests].count(1) + [x[2] for x in currentTests].count(3)
        count = len(currentTests)
        if not args.quiet:
            print("Current tests Passed: {}/{}".format(passed, count))
        testsCounter.update([x[2] for x in currentTests])
        
        writeTestFile(currentTests, args.resultDirectory, testFile)

    print("\n########## {} TEST SUMMARY ##########".format(len(args.testFiles)))
    total = sum(testsCounter.values())
    print("Total Passed: {}/{}".format(testsCounter[1]+testsCounter[3], total))
    print("0 - {}".format(testsCounter[0]))
    print("1 - {}".format(testsCounter[1]))
    print("2 - {}".format(testsCounter[2]))
    print("3 - {}".format(testsCounter[3]))
