#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
import time
from flask import Flask, jsonify, request, redirect, url_for, flash, render_template, send_file,  make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
from web3 import Web3
import urllib.parse
import random
from flask_cors import CORS
import base64

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
CORS(app)

# cors = CORS(app)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#define and initiate the JSON const object 
# Opening JSON file
#f = open('./constants.json')

f = open(os.path.join(UPLOAD_FOLDER, 'constants.json'))
  
# returns JSON object as 
# a dictionary
CONST = json.load(f)
CONST = CONST['const'][0]
  
# Closing file
f.close()

@app.route('/file', methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload_file():
    # return jsonify(
    #             cid= "sup kid"
    #         )
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
        websiteCID = ""
        try:
            arrayOutput = output.split(" ")
            websiteCID = arrayOutput[-2]
        except:
            websiteCID = ""
        #toReturn = arrayOutput[-2]
        #return a response that is a json object with the hash of the file
        # except:
        #     print("shit")
        #     os.popen('echo "shit man" ')
        # finally:
        #     print("well")
        
        return jsonify(
                cid= "" + websiteCID + ""
            )
        return "o my"
        return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('index.html')

@app.route('/getScreenShot', methods=['GET', 'POST'])
def getScreenShot():
    cid = request.form['cid']
    seed = request.form['seed']
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
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('http://35.232.44.3:8080/ipfs/' + cid + '/?seed=' + seed)

    element = driver.find_element_by_tag_name("canvas")

    location = element.location
    size = element.size
    print("sup nerd")
    os.popen('echo "hi echo" ')
    driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    time.sleep(2)
    stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
    #stream = os.popen('echo "bruh"')
    output = stream.read()
    print("hello there")
    print(output)
    arrayOutput = output.split(" ")
    toReturn = output
    return jsonify(
                cid= "" + toReturn  + ""
            )

@app.route('/getMetaData', methods=['GET', 'POST'])
def getMetaData():
    #https://rinkeby.infura.io/v3/ce27477f441742249fa8614a3b3872de
    tokenAddress = request.args.get("tokenAddress")
    #cid = request.args.get("cid")
    seed = request.args.get("seed")
    infura_url = 'https://rinkeby.infura.io/v3/ce27477f441742249fa8614a3b3872de'
    web3 = Web3(Web3.HTTPProvider(infura_url))
    tokenAddress = Web3.toChecksumAddress(tokenAddress)

    abi = json.loads('[{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"string","name":"baseSiteURI","type":"string"},{"internalType":"string","name":"seed","type":"string"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"royaltyRate","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_baseSiteURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_price","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_royaltyRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_seed","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"create","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"imageURI","type":"string"}],"name":"formatTokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInfo","outputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"string","name":"imgUri","type":"string"},{"internalType":"string","name":"baseSiteURI","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"curSupply","type":"uint256"}],"internalType":"struct GenerativeTokenInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIterations","outputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"string","name":"tokenURI","type":"string"},{"internalType":"address","name":"owner","type":"address"}],"internalType":"struct TokenInfo[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    address = tokenAddress

    contract = web3.eth.contract(address=address, abi=abi)

    #need to put .call() at the end to call the smart contract
    contractInfo = contract.functions.getInfo().call()

    #convert supply to Wei witch is 18 decimal places)
    print('contract info: ', contractInfo)

    cid = contractInfo[2].split("/ipfs/")[-1]

    print("features bitch: " , cid)

    # if user does not select file, browser also
    # submit a empty part without filename
    # if cid == '':
    #     flash('No CID passed')
    #     return redirect(request.url)
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('http://35.232.44.3:8080/ipfs/' + cid)

    features = driver.execute_script("return window.$features")

    print("features data", features)

    element = driver.find_element_by_tag_name("canvas")

    location = element.location
    size = element.size
    print("sup nerd")
    os.popen('echo "hi echo" ')
    driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    time.sleep(2)
    stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
    #stream = os.popen('echo "bruh"')
    output = stream.read()
    print("hello there")
    print(output)
    arrayOutput = []
    imageCID = ""
    try:
        arrayOutput = output.split(" ")
        imageCID = arrayOutput[-2]
    except:
        imageCID = ""

    imageURL = 'http://35.232.44.3:8080/ipfs/' + imageCID

    # struct GenerativeTokenInfo {
    #     address tokenAddress;
    #     string imgUri;
    #     string baseSiteURI;
    #     string name;
    #     string description;
    #     uint price;
    #     uint maxSupply;
    #     uint curSupply;
    # }

    # return jsonify(
    #             tokenAddress = contractInfo[0],
    #             imgUri = contractInfo[1],
    #             baseSiteURI = contractInfo[2],
    #             name = contractInfo[3],
    #             description = contractInfo[4],
    #             price = contractInfo[5],
    #             maxSupply = contractInfo[6],
    #             curSupply = contractInfo[7],
    #             attributes = features 
    #         )

    return jsonify(
                image = imageURL,
                name = contractInfo[3],
                description = contractInfo[4],
                attributes = features, 
                external_url = contractInfo[2] + "/?seed=" + seed
            )
    
    return "cool"


@app.route('/getMetaDataTest', methods=['GET', 'POST'])
def getMetaDataTest():
    #https://rinkeby.infura.io/v3/ce27477f441742249fa8614a3b3872de

    return jsonify(
                image = "https://picsum.photos/200",
                name = "testington wellsorth",
                description = "testington's scrotum was bitten off by a rabid dog when he was a child. When he grew up, he would go around at night and take the testicles of sleeping dogs. Eventually, he came to be known as the infomous: BOWBOW Testicleton.",
                attributes = "one testicle", 
                external_url = "https://testington.wiki"
            )
    
    return "cool"

# Make new endpoint for metadata

@app.route('/JSgetScreenShot', methods=['GET', 'POST'])
def JSgetScreenShot():
    cid = request.form['cid']
    seed = request.form['seed']
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
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('http://35.232.44.3:8080/ipfs/' + cid + '/?seed=' + seed)

    element = driver.find_element_by_tag_name("canvas")

    injected_javascript = (
        'var dataURL = canvas.toDataURL("png");'
        'return dataURL;'
    )

    location = element.location
    size = element.size
    print("sup nerd")
    os.popen('echo "hi echo" ')
    #driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    screenshot = driver.execute_async_script(injected_javascript)
    time.sleep(2)
    stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, screenshot))
    #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
    #stream = os.popen('echo "bruh"')
    output = stream.read()
    print("hello there")
    print(output)
    arrayOutput = output.split(" ")
    toReturn = output
    return jsonify(
                screenshotData = screenshot
            )

#helper functions

def scrapeImageLegacy(url):
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(url)

    element = driver.find_element_by_tag_name("canvas")

    location = element.location
    size = element.size
    print("sup nerd")
    os.popen('echo "hi echo" ')
    driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + "cid" + ".png"))
    time.sleep(2)
    stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, "screenshot_" + "cid"+ ".png"))
    #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
    #stream = os.popen('echo "bruh"')
    output = stream.read()
    print("hello there")
    print(output)
    arrayOutput = output.split(" ")
    toReturn = output
    return "" + toReturn  + ""

def scrapeImage(url):
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(url)

    element = driver.find_element_by_tag_name("canvas")

    location = element.location
    size = element.size
    print("sup nerd")
    os.popen('echo "hi echo" ')
    #generate random string
    driver.set_script_timeout(10)
    screenshot = driver.execute_script('return canvas.toDataURL("png")')
    screenshotData = screenshot.split('data:image/png;base64,')[1]
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(screenshotData))

    #driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + "123" + ".png"))
    time.sleep(2)
    stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, "imageToSave.png"))
    #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
    #stream = os.popen('echo "bruh"')
    output = stream.read()
    print("hello there")
    print(output)
    arrayOutput = output.split(" ")[1]
    toReturn = output
    return send_file(os.path.join(UPLOAD_FOLDER, "imageToSave.png"))

def scrapeMetaData(canvasURI, generatorInfoOnChain):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(canvasURI)

    features = driver.execute_script("return window.$features")

    print("features data", features)

    element = driver.find_element_by_tag_name("canvas")

    #contract address + tokenID
    canvasURIEscaped = urllib.parse.quote(canvasURI)
    canvasURIEscaped = canvasURIEscaped.replace("/", "%2F")
    #streamimageURL = CONST["ROOT_PATH"] + "getTokenImage/" + canvasURIEscaped
    seed = canvasURI.split("?seed=")[1]
    imageURL = CONST["ROOT_PATH"] + "getTokenImage/" + generatorInfoOnChain[0] + "/" + seed
    
    return {
        "image" : imageURL,
        "external_url" : canvasURI,
        "description" : generatorInfoOnChain[2],
        "name" : generatorInfoOnChain[1],
        "attributes" : features, 
    }
    
            

#notion endpoints le fin
@app.route('/getAllGenerators', methods=['GET', 'POST'])
def getAllGenerators():
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    genftAbi = CONST["GENFT_ABI"]
    genftContract = web3.eth.contract(address=genftContractAddress, abi=genftAbi)
    generatorInfoOnChains = genftContract.functions.getAllGenerators().call()
    result = []
    for generatorInfoOnChain in generatorInfoOnChains:
        generatorInfoProcessed = getGeneratorInfo(generatorInfoOnChain[0])
        result.append(generatorInfoProcessed)
    return make_response(jsonify(result), 200) 

@app.route('/getRandomGenerator', methods=['GET', 'POST'])
def getRandomGenerator():
    allGenerators = getAllGenerators().json

    randomGenerator = random.choice(allGenerators)
    return jsonify(randomGenerator)

@app.route('/getGeneratorInfo/<generatorAddress>', methods=['GET', 'POST'])
def getGeneratorInfo(generatorAddress):
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    generatorAbi = CONST["GENERATOR_ABI"]
    generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    generatorInfoOnChain = generatorContract.functions.getGeneratorInfo().call()
    canvasURI = generatorInfoOnChain[3] + "?seed=" + generatorInfoOnChain[4]
    previewMetaData =  scrapeMetaData(canvasURI, generatorInfoOnChain)
    return {
        "contactAddress" : generatorInfoOnChain[0],
        "name" : generatorInfoOnChain[1],
        "description" : generatorInfoOnChain[2],
        "canvasBaseURI" : generatorInfoOnChain[3],
        "previewSeed" : generatorInfoOnChain[4],
        "price" : generatorInfoOnChain[5],
        "curSupply" : generatorInfoOnChain[6],
        "maxSupply" : generatorInfoOnChain[7],
        "royaltyRate" : generatorInfoOnChain[8],
        "previewMetadata" : previewMetaData,
    }

@app.route('/getIterations/<generatorAddress>', methods=['GET', 'POST'])
def getIterations(generatorAddress):
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    generatorAbi = CONST["GENERATOR_ABI"]
    generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    tokenInfoOnChains = generatorContract.functions.getIterations().call()
    result = []
    for tokenInfoOnChain in tokenInfoOnChains:
        tokenInfoProcessed = getTokenInfo(generatorAddress, tokenInfoOnChain[0])
        result.append(tokenInfoProcessed)
    return jsonify(result)

@app.route('/getTokenInfo/<generatorAddress>/<tokenID>', methods=['GET', 'POST'])
def getTokenInfo(generatorAddress, tokenID):
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    generatorAbi = CONST["GENERATOR_ABI"]
    generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    tokenInfoOnChain = generatorContract.functions.getTokenInfo(int(tokenID)).call()
    metaData = getTokenMetadataTest(generatorContractAddress, tokenID)
    #return  metaData
    result = {
        "tokenID": tokenInfoOnChain[0],
        "tokenURI": tokenInfoOnChain[1],
        "owner": tokenInfoOnChain[2],
        "metadata": metaData,
    }
    return result

@app.route('/getTokenImage/<generatorAddress>/<seed>', methods=['GET', 'POST'])
def getTokenImage(generatorAddress, seed):
    # infura_url = CONST["INFURA_URL"]
    # web3 = Web3(Web3.HTTPProvider(infura_url))
    # generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    # genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    # generatorAbi = CONST["GENERATOR_ABI"]
    # generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    # generatorInfoOnChain = generatorContract.functions.getGeneratorInfo().call()
    
    # canvasURI = generatorInfoOnChain[3] + "?seed=" + seed
    
    url = "http://35.239.82.129:8080/ipfs/QmR1dDnSXz98vYXf4eL7kiR5qUEWCjJ3F96ts1Y7cfaqFH/?seed=Qmd286K6pohQcTKYqnS1YhWrCiS4gz7Xi34sdwMe9USZ7u"
    return scrapeImage(url)

@app.route('/getTokenMetadata/<generatorAddress>/<tokenID>', methods=['GET', 'POST'])
def getTokenMetadata(generatorAddress, tokenID):
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    generatorAbi = CONST["GENERATOR_ABI"]
    genftAbi = CONST["GENFT_ABI"]
    
    genftContract = web3.eth.contract(address=genftContractAddress, abi=genftAbi)
    generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    
    generatorInfoOnChain = generatorContract.functions.getGeneratorInfo().call()
    #return jsonify(generatorInfoOnChain)
    tokenInfoOnChain = generatorContract.functions.getTokenInfo(int(tokenID)).call()
    #return jsonify(tokenInfoOnChain)
    tokenURI = tokenInfoOnChain[1]
    seed = tokenURI.split("&seed=")[1] 
    canvasBaseURI = generatorInfoOnChain[3]
    scrapedMetaData = scrapeMetaData(canvasBaseURI + "?seed=" + seed, generatorInfoOnChain)
    
    return scrapedMetaData

def getTokenMetadataTest(generatorAddress, tokenID):
    infura_url = CONST["INFURA_URL"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    generatorContractAddress = Web3.toChecksumAddress(generatorAddress)
    genftContractAddress = Web3.toChecksumAddress(CONST["GENFT_CONTRACT_ADDRESS"])
    generatorAbi = CONST["GENERATOR_ABI"]
    genftAbi = CONST["GENFT_ABI"]
    
    genftContract = web3.eth.contract(address=genftContractAddress, abi=genftAbi)
    generatorContract = web3.eth.contract(address=generatorContractAddress, abi=generatorAbi)
    
    generatorInfoOnChain = generatorContract.functions.getGeneratorInfo().call()
    #return jsonify(generatorInfoOnChain)
    tokenInfoOnChain = generatorContract.functions.getTokenInfo(int(tokenID)).call()
    #return jsonify(tokenInfoOnChain)
    tokenURI = tokenInfoOnChain[1]
    seed = tokenURI.split("&seed=")[1] 
    canvasBaseURI = generatorInfoOnChain[3]
    scrapedMetaData = scrapeMetaData(canvasBaseURI + "?seed=" + seed, generatorInfoOnChain)
    
    return scrapedMetaData






if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)


