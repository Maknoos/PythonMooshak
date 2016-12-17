import subprocess
import platform
import re
import os
import difflib
import json
from subprocess import TimeoutExpired #for some reason this isn't included when importing subprocess

class compileTimeException(Exception):
    pass

answerDict = {}

def compileCPlus(inputFile):
    exeFile = inputFileToExe(inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/g++",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error  = compilationProcess.communicate()[1].decode()
    if  error != "":
        raise compileTimeException(error)

    #return output


def runCPlus(pairs,inputFile,timeLimit):
    #runString = "./" + inputFileToExe(inpuls
    # tFile)
    differences = []
    runString = inputFileToExe(inputFile)
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        try:
            output = compilationProcess.communicate(input=currInput,timeout=timeLimit)[0].decode()
        except TimeoutExpired:
            compilationProcess.kill()
            raise
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
    if ".cpp" in inputFile: #hvað ef hún heitir asshole.cpp.c?
        return re.sub(".cpp$",".exe",inputFile)
    else:
        return re.sub(".c$", ".exe", inputFile)
    #ATH skrifa sem snyrtilegri lausn

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
        #print(difference)
        return difference

def testFile(problemID, inputFile):
    init()
    result = ""
    feedBack = []
    answers = answerDict[problemID]['Answers']
    timeout = answerDict[problemID]['Timeout']
    checkMemory = answerDict[problemID]['Valgrind']
    language  = answerDict[problemID]['Language']
    try:
        if language == ".cpp": #sameina i fall med language sem parameter
            compileCPlus(inputFile)
        else:
            compileC(inputFile)
    except compileTimeException as compileError:
        return "Compile Time error" , [str(compileError)]
    try:
        feedBack = runCPlus(answers,inputFile,timeout)
    except TimeoutExpired:
        return("Time limit exceeded",[])
    if len(feedBack)!=0: #gera hjalparfall
        result = "Wrong Answer"
    elif checkMemory:
        feedBack = valgrindCheck(inputFile)
        if len(feedBack) != 0:  #gera hjalparfall
            result = "Memory error"
    else:
        result = "Accepted"
    removeFile(inputFile)
    return result, feedBack

#print (compileCPlus())

#we dont save the inputFile for now.. just answers and id of the problem
def createProblem(problemName, problemDescription, inputFile, testCases, valgrind = False, timeout = 10):

    ID = len(answerDict.keys())
    answerDict[ID] = {}
    initProblemDicts(answerDict[ID])

    answerDict[ID]['Name'] = problemName
    answerDict[ID]['Description'] = problemDescription
    answerDict[ID]['Answers'] = generateAnswers(inputFile,testCases)
    answerDict[ID]['Timeout'] = timeout
    answerDict[ID]['Valgrind'] = valgrind
    answerDict[ID]['Language'] = re.search('\.[^.]*$',inputFile).group()
    removeFile(inputFile)


def initProblemDicts(dict):
    dict['Name'] = {}
    dict['Description'] = {}
    dict['Answers'] = {}
    dict['Timeout'] = {}
    dict['Valgrind'] = {}
    dict['Language'] = {}

def getNameAndDescription(ID):
    init()
    data = {}
    data.setdefault('Name',answerDict[ID]['Name'])
    data.setdefault('Description',answerDict[ID]['Description'])
    return data
    #Hardcoded for now

    #data = {}
    #data.setdefault('Name',"Placeholder name")
    #data.setdefault('Description',"This is a random line of text that should be replaced with real data before the assignment is handed in")
    #return data

#print(platform.system())
#returns tuple of keys and name of problem
def getDictKeysAndName():
    init()
    return [(x , answerDict[x]['Name']) for x in answerDict] #needs to be sorted by keys..

def initTestData():
    createProblem("Is Palindrome", "..", "./correctIsPalindrome.cpp", ['tacocat', 'not','aaaaa'])
    createProblem("Pogba Goal", "..", "./correctPogba.cpp", ['x', 'k'])
    createProblem("Only Digits", "..", "./correctOnlyDigits.cpp", ['18534', 'asdfd', '1?#3'])

def init():
    global answerDict
    with open('AnswerDictionary.json', 'r') as f:
        answerDict = json.load(f)
def exitAndSave():
    with open('AnswerDictionary.json', 'w') as f:
        json.dump(answerDict, f)
def KG():

    #InputFile = "./leak.cpp"

    #InputFile = "./test.cpp"

    #InputFile = "./forever.cpp"
    #InputFile = "./wrongIsPalindrome.cpp"
    InputFile = "./correctIsPalindrome.cpp"

    #create problem
    #initTestData()

    init()
    print("hi")

    # test problem with id
    problemID = getDictKeysAndName()[0][0]  # hardcoded to test
    print(answerDict)


    compileCPlus(InputFile)
    print (testFile('0', InputFile)[0])
    exitAndSave()
    #print (valgrindCheck(InputFile))
    #runCPlus(answerDict[problemID]['Answers'], InputFile)
    #removeFile(InputFile)



def valgrindCheck(inputFile):
    #ATH ./
    inputFile = inputFileToExe(inputFile)
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


def compileC(inputFile):
    exeFile = inputFileToExe(inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/gcc",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error  = compilationProcess.communicate()[1].decode()
    if  error != "":
        raise compileTimeException(error)
    #sameina með C++


def maggi():
    init()
    print(testFile("0","./gylfi.c"))
    pass
    #compileCPlus("./test.cpp")
    #compileC("gylfi.c")
    #pairs = [("a", "a\n"), ("b", "HelloWorld"), ("c", "n")]
    #res  = runCPlus(pairs,"./gylfi.c")
    #compilationProcess = subprocess.Popen(["./test.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    #dummystring = ("input").encode()
    #output = compilationProcess.communicate(input=dummystring)[0]
    #print(output)
    #process = subprocess.Popen(["valgrind","--leak-check=yes","./test.exe"],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    #output = process.communicate()[1]
    #fail = valgrindCheck("./test.cpp")
    #success = valgrindCheck("./noerrors.cpp")
    #print("success"+success+"success")
    #print("fail"+fail+"fail")
#maggi()


#KG()