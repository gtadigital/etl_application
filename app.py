from flask import Flask
from flask import render_template
from datetime import datetime
import re
import os
import person_parser
from flask import request
from flask import redirect, url_for, abort, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "secret key"
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.xml', '.rdf']
app.config['UPLOAD_PATH'] = 'input/person/'
#app.config['DOWNLOAD_PATH'] = 'output/person/'

ALLOWED_EXTENSIONS = set(['xml', 'rdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/person_parser/', methods = ['GET', 'POST'])
def dynamic_page():
    if request.method == 'POST':
        #return person_parser.parser_person()
        person_parser.parser_person()
        return redirect(url_for('person'))
    
@app.route("/person/")
def person():
    return render_template("person.html")

@app.route('/person/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        flash('File(s) successfully uploaded')
        return redirect(url_for('person'))


