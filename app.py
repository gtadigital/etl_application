from flask import Flask
from flask import render_template
from datetime import datetime
import re
import person_parser
from flask import request

app = Flask(__name__)

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
        return person_parser.parser_person()

@app.route("/person/")
def person():
    return render_template("person.html")


