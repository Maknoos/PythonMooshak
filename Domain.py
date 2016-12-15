import subprocess
import platform
import re
import os
import difflib

def compileCPlus(inputFile):
    exeFile = inputFileToExe(inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/g++",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    compilationProcess.communicate()

    #return output


def runCPlus(pairs,inputFile):
    #runString = "./" + inputFileToExe(inputFile) #inputFile has to be .cpp?
    differences = []
    runString = inputFileToExe(inputFile) #þegar ég notaði slóð sem byrjaði á ./  annars ekki hægt að vísa í aftari möppur
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        output = compilationProcess.communicate(input=currInput)[0].decode()
        #setja compare fall her
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
    feedBack = ""
    compileCPlus(inputFile)
    feedBack = runCPlus([("a","b")],inputFile)
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
    #compileCPlus("./test.cpp")
    #compilationProcess = subprocess.Popen(["./test.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    #dummystring = ("input").encode()
    #output = compilationProcess.communicate(input=dummystring)[0]
    #print(output)
    #pairs = [("a","a\n"),("b","z"),("c","n")]
    #res  = runCPlus(pairs,"./test.cpp")
    print(testFile("./test.cpp",""))
maggi()


