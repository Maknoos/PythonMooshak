import os
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from Domain import compileCPlus

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['cpp']) # haegt ad setja fleiri endingar

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    target = os.path.join(app.config['UPLOAD_FOLDER'], 'uploads')

    if not os.path.isdir(target):
        os.mkdir(target)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)        # redirecta aftur á upphafsidu?

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            destination = "/".join([target, filename])

            file.save(destination)

            # senda a domain og fa nidurstodur tilbaka
            # compileCPlus()

            return render_template("complete.html")

if __name__ == "__main__":
    app.run()