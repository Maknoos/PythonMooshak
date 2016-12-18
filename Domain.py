import subprocess
import re
import os
import difflib
import json
from subprocess import TimeoutExpired  # for some reason this isn't included when importing subprocess


class compileTimeException(Exception):
    pass

# Main data structure used to store problems on runtime
answerDict = {}

# Runs a list of inputs through a file and returns the differences in outputs as a html table
def runInputFile(pairs, inputFile, timeLimit):
    differences = []
    runString = inputFileToExe(inputFile)
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        try:
            output = compilationProcess.communicate(input=currInput, timeout=timeLimit)[0].decode()
        except TimeoutExpired:
            compilationProcess.kill()
            raise
        result = compare(output, pair[1])

        if result != "":
            differences.append(result)

    return differences

# We take in the 'Answer' file and the inputs to run tests with
# we compile and run the answer file with the inputs and generate tuples of
# input to output pairings which we later use to compare
def generateAnswers(inputFile, input,language):
    answers = []
    compile(inputFile,getFileLanguage(inputFile))

    runString = inputFileToExe(inputFile)
    for inp in input:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = compilationProcess.communicate(input=inp.encode(), timeout=5)[0].decode()
        answers.append((inp, output))
    return answers

# Clean up function that removes files we are done with(.exe mostly)
# Python files are also removed but this is arguable
def removeFile(inputFile):
    if inputFile.endswith('.py'):
        os.remove(inputFile)
        return
    else:
        os.remove(inputFileToExe(inputFile))
# Get which programming language a file is written in
def getFileLanguage(inputFile):
    return re.search('\.[^.]*$', inputFile).group()


# Simple function that changes the file extensions of .cpp and .c to .exe files
# both for clean up purposes and also for simpler "run" code
def inputFileToExe(inputFile):
    if inputFile.endswith(".cpp"):
        return re.sub(".cpp$", ".exe", inputFile)
    elif inputFile.endswith(".py"): #py scripts dont run as exe
        return ["python3", inputFile]
    elif inputFile.endswith(".c"):
        return re.sub(".c$", ".exe", inputFile)
    else:
        return None

# takes in the output from the compiled program and compares it to a file with correct output
# returns a html table that we render that displays the differences
def compare(obtained, expected):
    if(obtained == expected):
        return ""
    else:
        difference = difflib.HtmlDiff().make_table(obtained.splitlines(), expected.splitlines())
        return difference

# The main function in the Domain script , takes a code file compiles it, runs it and performs
# all the necessary checks,
def testFile(problemID, inputFile):
    updateData()
    result = ""
    feedBack = []
    answers = answerDict[problemID]['Answers']
    timeout = answerDict[problemID]['Timeout']
    checkMemory = answerDict[problemID]['Valgrind']
    language = answerDict[problemID]['Language']
    try:
       compile(inputFile, language)
    except compileTimeException as compileError:
        return errorHandle(("Compile Time error", [str(compileError)]),inputFile)
    try:
        feedBack = runInputFile(answers, inputFile, timeout)
    except TimeoutExpired:
        return errorHandle(("Time limit exceeded", []), inputFile)

    if len(feedBack)!=0:
        result = "Wrong Answer"
    elif checkMemory:
        feedBack = valgrindCheck(inputFile)
        if len(feedBack) != 0:
            result = "Memory error"
    else:
        result = "Accepted"
    removeFile(inputFile)
    return result, feedBack

# Simple wrapping function for removing a file when we hit an exception to avoid repeated code
def errorHandle(tuple, file):
    removeFile(file)
    return tuple

# This function creates a "problem". The file from the user is compiled & run with the given test cases and
# the results  are stored with the input as tuples. after running the .exe file is deleted. User can choose
# whether they want valgrind to be used or even how long for timeout.
def addProblem(problemName, problemDescription, inputFile, testCases, language, valgrind = False, timeout = 10):

    ID = len(answerDict.keys())
    answerDict[ID] = {}
    initProblemDicts(answerDict[ID])

    answerDict[ID]['Name'] = problemName
    answerDict[ID]['Description'] = problemDescription
    answerDict[ID]['Answers'] = generateAnswers(inputFile, testCases, language)
    answerDict[ID]['Timeout'] = int(timeout)
    answerDict[ID]['Valgrind'] = valgrind
    answerDict[ID]['Language'] = language
    removeFile(inputFile)
    saveToFile()

# Initialize the dictionary with more dictionaries
def initProblemDicts(dict):
    dict['Name'] = {}
    dict['Description'] = {}
    dict['Answers'] = {}
    dict['Timeout'] = {}
    dict['Valgrind'] = {}
    dict['Language'] = {}

# A function that returns a dictionary containing the name , description and the language
# for a specific problem
def getNameDescAndLang(ID):
    updateData()
    data = {}
    data.setdefault('Name', answerDict[ID]['Name'])
    data.setdefault('Description', answerDict[ID]['Description'])
    data.setdefault('Language', answerDict[ID]['Language'])
    return data

# returns tuple of keys and name of problem
def getDictKeysAndName():
    updateData()
    return [(x, answerDict[x]['Name']) for x in answerDict]

# Fill dictionary with data(problems) from the .json file
def updateData():
    global answerDict
    with open('AnswerDictionary.json', 'r') as f:
        answerDict = json.load(f)

# Saves the dictionary into a .json file
def saveToFile():
    with open('AnswerDictionary.json', 'w') as f:
        json.dump(answerDict, f)

# Runs Valgrind on the program  and returns the valgrind message if the program has memory leaks
def valgrindCheck(inputFile):
    inputFile = inputFileToExe(inputFile)
    if ".py" in inputFile:
        return ""
    memoryProcess = subprocess.Popen(["valgrind","--leak-check=yes",inputFile], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = memoryProcess.communicate()[1].decode()

    if hasErrors(output):
        return [output]
    else:
        return ""

#  returns true if a valgrind message has more than 0 errors
def hasErrors(output):
    lines = output.splitlines()
    errorcount = lines[-1].split(":")[1]
    return (not "0" in errorcount)

# compiles c/c++ code by running the gcc/g++ compiler in the command line using subprocess
def compile(inputFile,language):
    exeFile = inputFileToExe(inputFile)
    if language == ".cpp":
        compiler = r"/usr/bin/g++"
    elif language == ".py": # doesn't need compiling
        return
    else:
        compiler = r"/usr/bin/gcc"
    compilationProcess = subprocess.Popen([compiler, inputFile, "-o", exeFile], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error = compilationProcess.communicate()[1].decode()
    if error != "":
        raise compileTimeException(error)


