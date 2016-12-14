import subprocess
import platform
import re
import os

def compileCPlus(inputFile):
    exeFile = re.sub(".cpp$",".exe",inputFile)  #replace .cpp with .exe
    compilationProcess = subprocess.Popen([r"/usr/bin/g++",inputFile,"-o",exeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    compilationProcess.communicate()

    #return output


def runCPlus(pairs,inputFile):
    runString = "./" + inputFile + ".exe"
    for pair in pairs:
        compilationProcess = subprocess.Popen(runString, stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        currInput = pair[0].encode()
        output = compilationProcess.communicate(input=currInput)[0]
        print(output)
        #setja compare fall her


def removeFile(inputFile):
    os.remove(inputFile)

def testFile(inputFile,testStrings):
    compileCPlus(inputFile)
    runCPlus()
    removeFile()
    pass

#print (compileCPlus())

#print(platform.system())

def maggi():
    compileCPlus()
    #compilationProcess = subprocess.Popen(["./test.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    #dummystring = ("input").encode()
    #output = compilationProcess.communicate(input=dummystring)[0]
    #print(output)
    pairs = [("a","x"),("b","z"),("c","n")]
    runCPlus(pairs,"test")
maggi()


