import subprocess

def compileCPlus():
    compilationProcess = subprocess.Popen([r"/usr/bin/g++","test.cpp","-o","output.exe"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    compilationProcess.communicate()
    compilationProcess = subprocess.Popen(["./output.exe"],stdout=subprocess.PIPE)
    output = compilationProcess.stdout.read()

    return output

#compileCPlus()