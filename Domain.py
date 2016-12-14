import subprocess
import platform

def compileCPlus():
    compilationProcess = subprocess.Popen([r"/usr/bin/g++","test.cpp","-o","output.exe"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    compilationProcess.communicate()
    compilationProcess = subprocess.Popen(["./output.exe"],stdout=subprocess.PIPE)
    output = compilationProcess.stdout.read()

    return output

def runCPlus(pairs,inputFile):
    pass

def removeFile(inputFile):
    pass

def testFile(inputFile,testStrings):
    compileCPlus()
    runCPlus()
    removeFile()
    pass

#compileCPlus()

print(platform.system())