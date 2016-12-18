import subprocess
import re
import os
import difflib
import json
from subprocess import TimeoutExpired  # for some reason this isn't included when importing subprocess


class compileTimeException(Exception):
    pass

answerDict = {}

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

#input is list of strings to test
def generateAnswers(inputFile, input,language):
    answers = []
    compile(inputFile,getFileLanguage(inputFile))

    runString = inputFileToExe(inputFile)
    for inp in input:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = compilationProcess.communicate(input=inp.encode(), timeout=5)[0].decode()
        answers.append((inp,output))
    return answers

def removeFile(inputFile):
    if inputFile.endswith('.py'):
        os.remove(inputFile)
        return
    else:
        os.remove(inputFileToExe(inputFile))
def getFileLanguage(inputFile):
    return re.search('\.[^.]*$',inputFile).group()

def inputFileToExe(inputFile):
    if inputFile.endswith(".cpp"):
        return re.sub(".cpp$",".exe",inputFile)
    elif inputFile.endswith(".py"): #py scripts dont run as exe
        return ["python3", inputFile]
    elif inputFile.endswith(".c"):
        return re.sub(".c$", ".exe", inputFile)
    else:
        return None

#takes in the output from the compiled program and compares it to a file with correct output
def compare(obtained,expected):
    if(obtained == expected):
        return ""
    else:
        return difference

def testFile(problemID, inputFile):
    updateData()
    result = ""
    feedBack = []
    answers = answerDict[problemID]['Answers']
    timeout = answerDict[problemID]['Timeout']
    checkMemory = answerDict[problemID]['Valgrind']
    language  = answerDict[problemID]['Language']
    try:
       compile(inputFile,language)
    except compileTimeException as compileError:
        return errorHandle(("Compile Time error" , [str(compileError)]),inputFile)
    try:
        feedBack = runInputFile(answers, inputFile, timeout)
    except TimeoutExpired:
        return errorHandle(("Time limit exceeded",[]), inputFile)

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

def errorHandle(tuple, file):
    removeFile(file)
    return tuple

def addProblem(problemName, problemDescription, inputFile, testCases, language, valgrind = False, timeout = 10):

    ID = len(answerDict.keys())
    answerDict[ID] = {}
    initProblemDicts(answerDict[ID])

    answerDict[ID]['Name'] = problemName
    answerDict[ID]['Description'] = problemDescription
    answerDict[ID]['Answers'] = generateAnswers(inputFile,testCases,language)
    answerDict[ID]['Timeout'] = int(timeout)
    answerDict[ID]['Valgrind'] = valgrind
    answerDict[ID]['Language'] = language
    removeFile(inputFile)
    saveToFile()

def initProblemDicts(dict):
    dict['Name'] = {}
    dict['Description'] = {}
    dict['Answers'] = {}
    dict['Timeout'] = {}
    dict['Valgrind'] = {}
    dict['Language'] = {}

def getNameDescAndLang(ID):
    updateData()
    data = {}
    data.setdefault('Name',answerDict[ID]['Name'])
    data.setdefault('Description',answerDict[ID]['Description'])
    data.setdefault('Language',answerDict[ID]['Language'])
    return data

#returns tuple of keys and name of problem
def getDictKeysAndName():
    updateData()
    return [(x , answerDict[x]['Name']) for x in answerDict]

def updateData():
    global answerDict
    with open('AnswerDictionary.json', 'r') as f:
        answerDict = json.load(f)
def saveToFile():
    with open('AnswerDictionary.json', 'w') as f:
        json.dump(answerDict, f)

def valgrindCheck(inputFile):
    #ATH ./
    inputFile = inputFileToExe(inputFile)
    if ".py" in inputFile:
        return ""
    memoryProcess = subprocess.Popen(["valgrind","--leak-check=yes",inputFile],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    output = memoryProcess.communicate()[1].decode()

    if hasErrors(output):
        return [output]
    else:
        return ""

def hasErrors(output):
    lines = output.splitlines()
    errorcount = lines[-1].split(":")[1]
    return(not "0" in errorcount)

def compile(inputFile,language):
    exeFile = inputFileToExe(inputFile)
    if language == ".cpp":
        compiler = r"/usr/bin/g++"
    elif language == ".py": #doesnt need compiling, although what about build errors?
        return
    else:
        compiler = r"/usr/bin/gcc"
    compilationProcess = subprocess.Popen([compiler, inputFile, "-o", exeFile], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error = compilationProcess.communicate()[1].decode()
    if error != "":
        raise compileTimeException(error)


