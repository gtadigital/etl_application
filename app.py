from flask import Flask
from flask import render_template
from datetime import datetime
import re
import os
import person_parser
from flask import request
from flask import redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.xml', '.rdf']
app.config['UPLOAD_PATH'] = 'input/person/'

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
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('person'))


