#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from flask import Flask, jsonify, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)

cors = CORS(app)

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
        toReturn = "nothing"
        print("hey print")
        os.popen('echo "hi echo" ')
        zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
        zip_ref.extractall('./cache/' + filename)
        zip_ref.close()
        stream = os.popen('ipfs add -r ./cache/' + filename + '/')
        #stream = os.popen('echo ' + filename)
        output = stream.read()
        arrayOutput = output.split(" ")
        toReturn = output
        #toReturn = arrayOutput[-2]
        #return a response that is a json object with the hash of the file
        # except:
        #     print("shit")
        #     os.popen('echo "shit man" ')
        # finally:
        #     print("well")
        
        return jsonify(
                cid= "" + toReturn + ""
            )
        return "o my"
        return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('index.html')

@app.route('/getScreenShot', methods=['GET', 'POST'])
def getScreenShot():
    cid = request.form['cid']
    # if user does not select file, browser also
    # submit a empty part without filename
    if cid == '':
        flash('No CID passed')
        return redirect(request.url)
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('http://35.232.44.3:8080/ipfs/' + cid + '/')

    element = driver.find_element_by_tag_name("canvas")
    location = element.location
    size = element.size

    driver.save_screenshot("imageCache/screenshot_" + cid + ".png")

    stream = os.popen("ipfs add -r ./imageCache/screenshot_" + cid + ".png")
    output = stream.read()
    arrayOutput = output.split(" ")
    toReturn = output
    return jsonify(
                cid= "" + toReturn + ""
            )




if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)
