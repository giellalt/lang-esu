# runTest.py
# python3 runTest.py esu.gen.hfst esu.pairs.gold/Ch2.In-Chapter-Examples.tsv

import sys
import os
import subprocess
import json


def makeDirs(filename):
    directoryname = os.path.dirname(filename)
    if not os.path.exists(directoryname):
        os.makedirs(directoryname)
    return filename

def readTestFile(filename):
    testFile = []
    with open(filename, 'r') as f:
        testFile = [[x.strip() for x in line.split() if x != ''] for line in f]
        if len(testFile[0]) >= 3:
            testFile = tuple([[x[0], x[1], int(x[2]), json.loads(x[3])] for x in testFile])
    return testFile

def writeTestFile(outputTest, dirname, filename):
    outputFile = ["\t".join([t[0], t[1], str(t[2]), json.dumps(t[3], ensure_ascii=False)]) for t in outputTest]
    with open(os.path.join(dirname, filename), 'w') as out:
        out.write("\n".join(outputFile))

def runTests(testFile):
    testFileData = readTestFile(testFile)
    print("\n########## {} ##########".format(testFile))
    currentTests = []
    for underlying, surface in testFileData:
        completedProcess = subprocess.run(["echo \"{}\" | hfst-lookup {}".format(underlying, hfstName)], shell=True, capture_output=True)
        processResults = [line.decode("utf-8") for line in completedProcess.stdout.split()][1::3]

        testResultCode = -1
        if "+?" in processResults[0]:
            testResultCode = 0              # 0 = no output
            print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))
        elif surface in processResults:
            if len(processResults) == 1:
                testResultCode = 1          # 1 = just one answer and correct
            else:
                testResultCode = 3          # 3 = multiple outputs, including correct
        else:
            testResultCode = 2              # 2 = multiple outputs, none correct
            print("\t".join([underlying, surface, str(testResultCode), json.dumps(processResults, ensure_ascii=False)]))

        outputTest = (underlying, surface, testResultCode, processResults)
        currentTests.append(outputTest)
    return currentTests

def compareTests(previousTests, currentTests):
    changesCount = 0
    for i in range(len(currentTests)):
        if previousTests[i][0] == currentTests[i][0] and previousTests[i][1] == currentTests[i][1]:
            if previousTests[i][2] != currentTests[i][2]:
                changesCount += 1
                print("{}\t{}\t{} -> {}\t{} -> {}".format(currentTests[i][0], currentTests[i][1], \
                                                          previousTests[i][2], currentTests[i][2], \
                                                          json.dumps(previousTests[i][2], ensure_ascii=False), json.dumps(outputTest[i][2], ensure_ascii=False)))
    print("Previous tests Passed: {}/{}".format([x[2] for x in previousTests].count(1) + [x[2] for x in previousTests].count(3) , len(previousTests)))
    print("Prev -> Curr Count: {}".format(changesCount))


if __name__ == "__main__":
    testDir = "esu.pairs.test"
    hfstName = sys.argv[1]
    testFiles = sys.argv[2:]
    makeDirs(os.path.join(testDir, "blah"))

    for testFilePath in testFiles:
        testFile = os.path.basename(testFilePath)
        currentTests = runTests(testFilePath)
        print("########## {} SUMMARY ##########".format(testFile))
        print("Current tests Passed: {}/{}".format([x[2] for x in currentTests].count(1) + [x[2] for x in currentTests].count(3) , len(currentTests)))
        if os.path.exists(os.path.join(testDir, testFile)):
            previousTests = readTestFile(os.path.join(testDir, testFile))
            compareTests(previousTests, currentTests)
        writeTestFile(currentTests, testDir, testFile)














