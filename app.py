#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
            zip_ref.extractall('./cache/' + filename)
            zip_ref.close()
            stream = os.popen('ipfs add -r ./cache/' + filename + '/' + filename[:-4])
            #stream = os.popen('echo ' + filename)
            output = stream.read()
            arrayOutput = output.split(" ")
            toReturn = arrayOutput[-2]
            #return a response that is a json object with the hash of the file
            return toReturn
            
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)
