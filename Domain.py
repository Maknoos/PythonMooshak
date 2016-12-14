import subprocess
import platform

def compileCPlus():
    compilationProcess = subprocess.Popen([r"/usr/bin/g++","test.cpp","-o","output.exe"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    compilationProcess.communicate()
    #error = compilationProcess.stderr.read()

    #return output

def runCPlus(pairs,inputFile):
    compilationProcess = subprocess.Popen(["./output.exe"], stdout=subprocess.PIPE,stdin="test")
    output = compilationProcess.stdout.read()

def removeFile(inputFile):
    pass

def testFile(inputFile,testStrings):
    compileCPlus()
    runCPlus()
    removeFile()
    pass

#compileCPlus()

print(platform.system())

compileCPlus()
compilationProcess = subprocess.Popen(["./output.exe"], stdout=subprocess.PIPE,stdin=subprocess.PIPE)
compilationProcess.communicate(input="test")
output = compilationProcess.stdout.read()
print(output)