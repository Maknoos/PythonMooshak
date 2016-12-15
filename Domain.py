import subprocess
import platform
import re
import os
import difflib
from subprocess import TimeoutExpired

def compileCPlus(inputFile):
    exeFile = inputFileToExe(inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/g++",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    error  = compilationProcess.communicate()[1].decode()
    if  error != "":
        raise Exception(error)

    #return output


def runCPlus(pairs,inputFile):
    #runString = "./" + inputFileToExe(inputFile) #inputFile has to be .cpp?
    differences = []
    runString = inputFileToExe(inputFile) #þegar ég notaði slóð sem byrjaði á ./  annars ekki hægt að vísa í aftari möppur
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        try:
            output = compilationProcess.communicate(input=currInput,timeout=5)[0].decode()
        except TimeoutExpired:
            compilationProcess.kill()
            raise Exception
        result = compare(output,pair[1]) #HARDCODED ANSWER FILE for now, should be determined by which assignment user is handing it
        if result != "":
            differences.append(result)

    return differences


def removeFile(inputFile):
    os.remove(inputFileToExe(inputFile))

def inputFileToExe(inputFile):
    return re.sub(".cpp$",".exe",inputFile)

#takes in the output from the compiled program and compares it to a file with correct output
def compare(obtained,expected):
    if(obtained == expected):
        print ("ACCEPTED!")
        return ""
    else:
        print ("WRONG ANSWER")
        #HTML TABLE if we want
        difference = difflib.HtmlDiff().make_table(obtained.splitlines(), expected.splitlines())

        #difference = '\n'.join(difflib.Differ().compare(obtained.splitlines(), expected.splitlines()))
        return difference

def testFile(inputFile,testStrings):
    result = ""
    feedBack = []

    try:
        compileCPlus(inputFile)
    except Exception as compileError:
        return "Compile Time error" , [str(compileError)]

    try:
        feedBack = runCPlus([("a","a\n")],inputFile)
    except Exception as TimeOut:
        return("Time limit exceeded",[])

    if len(feedBack)!=0:
        result = "Wrong Answer"
    else:
        result = "Accepted"
    removeFile(inputFile)
    return result, feedBack

#print (compileCPlus())

#print(platform.system())
def KG():
    answer = "POGBOOM SCORES INCREDIBLE GOAL\nIBRAKADABRA"
    myTestInputFile = "./pogba.cpp"
    compileCPlus(myTestInputFile)
    runCPlus([("x", answer), ("wrong",answer)], myTestInputFile)
    removeFile(myTestInputFile)
#KG()


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
maggi()


