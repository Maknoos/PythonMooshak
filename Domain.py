import subprocess
import platform
import re
import os
import difflib
from subprocess import TimeoutExpired

answerDict = {}

def compileCPlus(inputFile):
    exeFile = inputFileToExe(inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/g++",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error  = compilationProcess.communicate()[1].decode()
    if  error != "":
        raise Exception(error)

    #return output


def runCPlus(pairs,inputFile):
    #runString = "./" + inputFileToExe(inputFile)
    differences = []
    runString = inputFileToExe(inputFile)
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        try:
            output = compilationProcess.communicate(input=currInput,timeout=5)[0].decode()
        except TimeoutExpired:
            compilationProcess.kill()
            raise Exception
        result = compare(output,pair[1])
        if result != "":
            differences.append(result)

    return differences

#input is list of strings to test
def generateAnswers(inputFile, input):
    answers = []
    compileCPlus(inputFile)
    runString = inputFileToExe(inputFile)
    for inp in input:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #currInput = inp.encode()
        try:
            output = compilationProcess.communicate(input=inp.encode(), timeout=5)[0].decode()
            answers.append((inp,output))
        except TimeoutExpired:
            compilationProcess.kill()
            raise Exception
    return answers

def removeFile(inputFile):
    os.remove(inputFileToExe(inputFile))

def inputFileToExe(inputFile):
    return re.sub(".cpp$",".exe",inputFile)

#takes in the output from the compiled program and compares it to a file with correct output
def compare(obtained,expected):
    if(obtained == expected):
        print ("Test case passed!")
        return ""
    else:
        print ("Test case failed!")
        #HTML TABLE if we want

        difference = difflib.HtmlDiff().make_table(obtained.splitlines(), expected.splitlines())
        #difference = difflib.HtmlDiff().make_file(obtained.splitlines(), expected.splitlines())

        #difference = '\n'.join(difflib.Differ().compare(obtained.splitlines(), expected.splitlines()))
        return difference

def testFile(problemID, inputFile):
    result = ""
    feedBack = []
    try:
        compileCPlus(inputFile)
    except Exception as compileError:
        return "Compile Time error" , [str(compileError)]

    try:
        feedBack = runCPlus(answerDict[problemID]['Answers'],inputFile)
    except Exception as TimeOut:
        return("Time limit exceeded",[])
    if len(feedBack)!=0:
        result = "Wrong Answer"
    else:
        result = "Accepted"
    removeFile(inputFile)
    return result, feedBack

#print (compileCPlus())

#we dont save the inputFile for now.. just answers and id of the problem
def createProblem(problemName, problemDescription, inputFile, testCases, valgrind = False, timeout = 0):

    ID = len(answerDict.keys())
    answerDict[ID] = {}
    initProblemDicts(answerDict[ID])

    answerDict[ID]['Name'] = problemName
    answerDict[ID]['Description'] = problemDescription
    answerDict[ID]['Answers'] = generateAnswers(inputFile,testCases)
    answerDict[ID]['Timeout'] = timeout
    answerDict[ID]['Valgrind'] = valgrind
    removeFile(inputFile)


def initProblemDicts(dict):
    dict['Name'] = {}
    dict['Description'] = {}
    dict['Answers'] = {}
    dict['Timeout'] = {}
    dict['Valgrind'] = {}

#print(platform.system())
#returns tuple of keys and name of problem
def getDictKeysAndName():
    return [(x , answerDict[x]['Name']) for x in answerDict]

def initTestData():
    createProblem("Is Palindrome", "..", "./correctIsPalindrome.cpp", ['tacocat', 'not','aaaaa'])
    createProblem("Pogba Goal", "..", "./correctPogba.cpp", ['x', 'k'])
    createProblem("Only Digits", "..", "./correctOnlyDigits.cpp", ['18534', 'asdfd', '1?#3'])


def KG():
    InputFile = "./forever.cpp"
    #InputFile = "./wrongIsPalindrome.cpp"
    #InputFile = "./correctIsPalindrome.cpp"

    #create problem
    initTestData()
    # test problem with id
    problemID = getDictKeysAndName()[0][0]  # hardcoded to test




    print (testFile(problemID, InputFile)[0])

    #compileCPlus(InputFile)
    #runCPlus(answerDict[problemID]['Answers'], InputFile)
    #removeFile(InputFile)
KG()


def maggi():
    #try:
    #   compileCPlus("./test.cpp")
    #except Exception as e:
    #    print(str(e))
    #compilationProcess = subprocess.Popen(["./test.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    #dummystring = ("input").encode()
    #output = compilationProcess.communicate(input=dummystring)[0]
    #print(output)
    #pairs = [("a","a\n"),("b","z"),("c","n")]
    #res  = runCPlus(pairs,"./test.cpp")
    print(testFile("./test.cpp",""))
#maggi()


