# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:44:27 2020

@author: Stone
"""

import os
from flask import Flask, render_template, request, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Body = None
Face = None
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = "static"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/photos", methods = ["GET","POST"])
def photos(msg = None):

    if msg != None:
        flash(msg)   
    return render_template("photos.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/check", methods = ["GET" , "POST"])
def check():
    if request.method == "POST":
        if 'Body_pic' not in request.files:
            msg = 'No file part'
            return  photos(msg)
        global Body 
        Body = request.files['Body_pic']
        global Face
        Face = request.files['Face_pic']
        if Body.filename == '':
            msg = 'No selected file in Body'
            return photos(msg)
        if Face.filename == '':
            msg = 'No selected file in Face'
            return photos(msg)
        
        if Body and Face:
            if not allowed_file(Body.filename):
                msg = 'Invalid data type in Body'
                return photos(msg)
            if not allowed_file(Face.filename):
                msg = 'Invalid data type in Face'
                return photos(msg)

            Bodyname = secure_filename(Face.filename)
            Body.save(os.path.join(app.config['UPLOAD_FOLDER'], Bodyname))
            Facename = secure_filename(Face.filename)
            Face.save(os.path.join(app.config['UPLOAD_FOLDER'], Facename))

            return processing()
        return photos(None)
    else:
        return render_template("Error.html")



@app.route("/processing", methods = ["GET","POST"])
def processing():
    if request.method == "POST":
        return render_template("processing.html", Body = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Body.filename)), Face = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(Face.filename)))

    elif Body == None or Face == None:
        return render_template("Error.html")

@app.route("/Sample3D")
def Sample3D():
    return render_template("Sample3D.html")