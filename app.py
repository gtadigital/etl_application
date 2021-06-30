from flask import Flask
from flask import render_template
import os
import person_parser
import archival_object_parser
import built_works_parser
import group_parser
import place_parser
from flask_bootstrap import Bootstrap
from flask import request
from flask import redirect, url_for,  flash
from werkzeug.utils import secure_filename

#imports for download function:
import flask as fl
import zipfile
import io
import pathlib
import shutil

import time

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "secret key"
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.xml', '.rdf']
app.config['UPLOAD_PATH_PERSON'] = 'input/person/'
app.config['UPLOAD_PATH_PLACE'] = 'input/place/'
app.config['UPLOAD_PATH_BW'] = 'input/built_works/'
app.config['UPLOAD_PATH_AO'] = 'input/archival_object/'
app.config['UPLOAD_PATH_GROUP'] = 'input/group/'
#app.config['DOWNLOAD_PATH'] = 'output/person/'
app.config['UPLOAD_PATH_ZIP'] = 'input/zip/'

ALLOWED_EXTENSIONS = set(['xml', 'rdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def unzip_file(src_path, dst_dir):
    r = zipfile.is_zipfile(src_path)
    if r:
        fz = zipfile.ZipFile(src_path, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        return "Please upload zip file"

# Replace the existing home function with the one belowaboabo
@app.route("/")
def home():
    return render_template("home.html")

    
#Person Parser
@app.route('/person_parser/', methods = ['GET', 'POST'])
def person_page():
    if request.method == 'POST':
        #return person_parser.parser_person()
        person_parser.parser_person()
        return redirect(url_for('person'))
    
@app.route("/person/")
def person():
    return render_template("person.html")

@app.route('/person/', methods=['POST'])
def person_upload_file():
    if request.method == 'POST':

        start_time = time.time()
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            ret_list = file.filename.rsplit(".", maxsplit=1)
            if len(ret_list) == 2 and ret_list[1] == "zip":
                file_path = os.path.join(app.config['UPLOAD_PATH_ZIP'], file.filename) #store zip file in fip folder
                file.save(file_path)
                unzip_file(file_path, os.path.join(app.config['UPLOAD_PATH_PERSON'], file.filename)) #unzip zip file and store files in usual folder
                os.remove(file_path) # delete zip file from zip folder
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_PERSON'], filename))
       
        end_time = time.time()
        total_time= end_time - start_time
        print(f"duration of upload: {total_time}")
        flash('File(s) successfully uploaded')
        return redirect(url_for('person'))
    
@app.route('/download_files_person/', methods=['POST'])
def person_download_files():
    base_path = pathlib.Path('./output/person/')

    data_file = io.BytesIO()
    with zipfile.ZipFile(data_file, 'w') as zf:
        for f in base_path.glob("**/*.xml"):
            zf.write(f)

    data_file.seek(0)

    shutil.rmtree('./output/person')
    shutil.rmtree('./input/person')
    os.makedirs('./output/person')
    os.makedirs('./input/person')
    return fl.send_file(data_file, attachment_filename='person.zip', as_attachment=True)

#Place Parser
@app.route('/place_parser/', methods = ['GET', 'POST'])
def place_page():
    if request.method == 'POST':
        #return place_parser.parser_place()
        place_parser.parser_place()
        return redirect(url_for('place'))
    
@app.route("/place/")
def place():
    return render_template("place.html")

@app.route('/place/', methods=['POST'])
def place_upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            ret_list = file.filename.rsplit(".", maxsplit=1)

            if len(ret_list) == 2 and ret_list[1] == "zip":
                file_path = os.path.join(app.config['UPLOAD_PATH_ZIP'], file.filename) #store zip file in fip folder
                file.save(file_path)
                unzip_file(file_path, os.path.join(app.config['UPLOAD_PATH_PLACE'], file.filename)) #unzip zip file and store files in usual folder
                os.remove(file_path) # delete zip file from zip folder
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_PLACE'], filename))

        flash('File(s) successfully uploaded')
        return redirect(url_for('place'))
    
@app.route('/download_files_place/', methods=['POST'])
def place_download_files():
    base_path = pathlib.Path('./output/place/')

    data_file = io.BytesIO()
    with zipfile.ZipFile(data_file, 'w') as zf:
        for f in base_path.glob("**/*.xml"):
            zf.write(f)

    data_file.seek(0)

    shutil.rmtree('./output/place')
    shutil.rmtree('./input/place')
    os.makedirs('./output/place')
    os.makedirs('./input/place')
    return fl.send_file(data_file, attachment_filename='place.zip', as_attachment=True)

#archival_object Parser
@app.route('/archival_object_parser/', methods = ['GET', 'POST'])
def archival_object_page():
    if request.method == 'POST':
        #return archival_object_parser.parser_archival_object()
        archival_object_parser.parser_archival_object()
        return redirect(url_for('archival_object'))
    
@app.route("/archival_object/")
def archival_object():
    return render_template("archival_object.html")

@app.route('/archival_object/', methods=['POST'])
def archival_object_upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            ret_list = file.filename.rsplit(".", maxsplit=1)

            if len(ret_list) == 2 and ret_list[1] == "zip":
                file_path = os.path.join(app.config['UPLOAD_PATH_ZIP'], file.filename) #store zip file in fip folder
                file.save(file_path)
                unzip_file(file_path, os.path.join(app.config['UPLOAD_PATH_AO'], file.filename)) #unzip zip file and store files in usual folder
                os.remove(file_path) # delete zip file from zip folder
                
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_AO'], filename))

        flash('File(s) successfully uploaded')
        return redirect(url_for('archival_object'))
    
@app.route('/download_files_archival_object/', methods=['POST'])
def archival_object_download_files():
    base_path = pathlib.Path('./output/archival_object/')

    data_file = io.BytesIO()
    with zipfile.ZipFile(data_file, 'w') as zf:
        for f in base_path.glob("**/*.xml"):
            zf.write(f)

    data_file.seek(0)

    shutil.rmtree('./output/archival_object')
    shutil.rmtree('./input/archival_object')
    os.makedirs('./output/archival_object')
    os.makedirs('./input/archival_object')
    return fl.send_file(data_file, attachment_filename='archival_object.zip', as_attachment=True)

#built_works Parser
@app.route('/built_works_parser/', methods = ['GET', 'POST'])
def built_works_page():
    if request.method == 'POST':
        #return built_works_parser.parser_built_works()
        built_works_parser.parser_built_works()
        return redirect(url_for('built_works'))
    
@app.route("/built_works/")
def built_works():
    return render_template("built_works.html")

@app.route('/built_works/', methods=['POST'])
def built_works_upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            
            ret_list = file.filename.rsplit(".", maxsplit=1)
            if len(ret_list) == 2 and ret_list[1] == "zip":
                file_path = os.path.join(app.config['UPLOAD_PATH_ZIP'], file.filename) #store zip file in fip folder
                file.save(file_path)
                unzip_file(file_path, os.path.join(app.config['UPLOAD_PATH_BW'], file.filename)) #unzip zip file and store files in usual folder
                os.remove(file_path) # delete zip file from zip folder
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_BW'], filename))

        flash('File(s) successfully uploaded')
        return redirect(url_for('built_works'))
    
@app.route('/download_files_built_works/', methods=['POST'])
def built_works_download_files():
    base_path = pathlib.Path('./output/built_works/')

    data_file = io.BytesIO()
    with zipfile.ZipFile(data_file, 'w') as zf:
        for f in base_path.glob("**/*.xml"):
            zf.write(f)

    data_file.seek(0)

    shutil.rmtree('./output/built_works')
    shutil.rmtree('./input/built_works')
    os.makedirs('./output/built_works')
    os.makedirs('./input/built_works')
    return fl.send_file(data_file, attachment_filename='built_works.zip', as_attachment=True)


#group Parser
@app.route('/group_parser/', methods = ['GET', 'POST'])
def group_page():
    if request.method == 'POST':
        #return group_parser.parser_group()
        group_parser.parser_group()
        return redirect(url_for('group'))
    
@app.route("/group/")
def group():
    return render_template("group.html")

@app.route('/group/', methods=['POST'])
def group_upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            ret_list = file.filename.rsplit(".", maxsplit=1)
            if len(ret_list) == 2 and ret_list[1] == "zip":
                file_path = os.path.join(app.config['UPLOAD_PATH_ZIP'], file.filename) #store zip file in fip folder
                file.save(file_path)
                unzip_file(file_path, os.path.join(app.config['UPLOAD_PATH_GROUP'], file.filename)) #unzip zip file and store files in usual folder
                os.remove(file_path) # delete zip file from zip folder
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_GROUP'], filename))

        flash('File(s) successfully uploaded')
        return redirect(url_for('group'))
    
@app.route('/download_files_group/', methods=['POST'])
def group_download_files():
    base_path = pathlib.Path('./output/group/')

    data_file = io.BytesIO()
    with zipfile.ZipFile(data_file, 'w') as zf:
        for f in base_path.glob("**/*.xml"):
            zf.write(f)

    data_file.seek(0)

    shutil.rmtree('./output/group')
    shutil.rmtree('./input/group')
    os.makedirs('./output/group')
    os.makedirs('./input/group')
    return fl.send_file(data_file, attachment_filename='group.zip', as_attachment=True)

    



