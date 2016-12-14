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
    compilationProcess = subprocess.Popen(["./output.exe"], stdout=subprocess.PIPE,stdin="test")
    output = compilationProcess.stdout.read()

def removeFile(inputFile):
    os.remove(inputFile)

def testFile(inputFile,testStrings):
    compileCPlus(inputFile)
    runCPlus()
    removeFile()
    pass

print (compileCPlus())

print(platform.system())

def maggi():
    compileCPlus()
    compilationProcess = subprocess.Popen(["./output.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    dummystring = "test"
    compilationProcess.communicate(input=dummystring.encode())
    output = compilationProcess.stdout.read()
    print(output)

maggi()


