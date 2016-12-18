Mini Mooshak - Kristinn Guðmundsson, Magnús Gunnarsson, Ólafur Valur Valdimarsson


We decided to implement a mini version of Mooshak. The code for running the program is contained in two python scripts Domain.py and Interface.py. Interface contains all the Flask code and the front end logic while Domain contains all the subprocesses and the backend logic. Please note that this program does not run on Windows operating systems.

To run the program simply run the Interface.py script ($python3 Interface.py) and the website should now be up on your localhost


The program depends on a few Unix programs to be able to run.
g++ is needed to compile C++ code
gcc is needed to compile C code  
Valgrind is needed to check for memory errors in programs - please note that Valgrind and mac do not always work perfectly together 

The program also relies the following PyPI packages
Flask
Werkzeug

Features of the program/website

-Create and upload problems in C, C++ or Python that users can submit solutions to. Attach your solution and specify inputs and the website will automatically generate input/output pairs. The time limit for the submission can also be specified as well as whether valgrind should check for memory errors. All created problems are stored in a .json file so the data is maintained between runs of the program.

-Submit solutions to problems, the website will post feedback in the following formats
	-Accepted 
	-Wrong Answer (with the difference between the user output and the expected output)
	-Compile Time error (with the error message from standard error)
	-Time limit exceeded (If the solution takes longer to run than the timeout specified)
	-Memory error (If memory check is enabled for the problem, also shows the valgrind error message)


