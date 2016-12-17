import os
from flask import Flask, render_template, request, redirect, Markup
from werkzeug.utils import secure_filename
from Domain import testFile, getDictKeysAndName, getNameAndDescription

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['cpp', 'c'])          # haegt ad setja fleiri endingar

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    problems = getDictKeysAndName()
    problems = sorted(problems, key= lambda x : int(x[0]))
    return render_template('index.html', problems=problems)

@app.route("/createProblem")
def createProblem():
    return render_template('createProblem.html')

@app.route("/handin/<pid>")
def handin(pid):
    result = getNameAndDescription(pid)
    return render_template('handin.html', pid=pid, result=result)

# athuga med villumedhondlun
@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(app.config['UPLOAD_FOLDER'], 'uploads')

    if not os.path.isdir(target):
        os.mkdir(target)

    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)        # redirecta aftur á upphafsidu?

    file = request.files['file']
    pid = request.form['pid']               # senda með

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)

        # senda a domain og fa nidurstodur tilbaka
        ans, testC = testFile(pid, destination)

        if ans == 'Accepted':
            return render_template("answer.html", answer=ans)

        for i in testC:
            testC = i

        if ans == 'Memory error':
            testC = testC.replace('\n', '<br/>')
            testC = Markup('<p>' + testC + '</p>')
            return render_template("answer.html", answer=ans, testCases=testC)

        if testC:
            testC = testC.replace('\n', '')
            testC = Markup(testC)

        return render_template("answer.html", answer = ans, testCases = testC)

if __name__ == "__main__":
    app.run()