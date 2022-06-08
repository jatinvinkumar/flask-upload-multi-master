#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import the json object from constants.json file
import os
import zipfile
import time
from flask import Flask, jsonify, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
from web3 import Web3
import json
  
# Opening JSON file
f = open('constants.json')
  
# returns JSON object as 
# a dictionary
CONST = json.load(f)
  
# Iterating through the json
# list
for i in CONST['const']:
    print(i)

ip = CONST["const"]
print(ip)
  
# Closing file
f.close()

def scrapeImage(url):

    #set webdriver options
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    #install driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    #ip = CONST["const"].get("SERVER_IP")
    #port = CONST["const"]["PORT_NUMBER"]
    driver.get('http://35.239.82.129:8080/ipfs/QmR1dDnSXz98vYXf4eL7kiR5qUEWCjJ3F96ts1Y7cfaqFH/?seed=Qmd286K6pohQcTKYqnS1YhWrCiS4gz7Xi34sdwMe9USZ7u')


    element = driver.find_element_by_tag_name("canvas")
    injected_javascript = (
        'var dataURL = canvas.toDataURL("png");'
        'return "dataURL";'
    )

    location = element.location
    size = element.size
    print("")
    print("sup nerd")
    os.popen('echo "hi echo" ')
    #driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
    driver.set_script_timeout(10)
    screenshot = driver.execute_script('return canvas.toDataURL("png")')
    
    time.sleep(2)
    return screenshot
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

print(scrapeImage(123))

# UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
# cid = "fuckYou"

# def scrapeImageLegacy(url):
    
#     #driver = webdriver.Chrome(ChromeDriverManager().install())
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("start-maximized")
#     options.add_argument("disable-infobars")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--headless");
#     options.add_argument("--disable-gpu");
#     options.add_argument("--disable-dev-shm-usage");
#     driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
#     driver.get(url)

#     element = driver.find_element_by_tag_name("canvas")

#     location = element.location
#     size = element.size
#     print("sup nerd")
#     os.popen('echo "hi echo" ')
#     driver.save_screenshot(os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
#     time.sleep(2)
#     stream = os.popen("ipfs add " + os.path.join(UPLOAD_FOLDER, "screenshot_" + cid + ".png"))
#     #stream = os.popen("ipfs add screenshot_QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn.png")
#     #stream = os.popen('echo "bruh"')
#     output = stream.read()
#     print("hello there")
#     print(output)
#     arrayOutput = output.split(" ")
#     toReturn = output
#     return "" + toReturn  + ""
            

# #print(scrapeImageLegacy("http://35.193.145.29:8080/ipfs/QmR1dDnSXz98vYXf4eL7kiR5qUEWCjJ3F96ts1Y7cfaqFH/?seed=Qmd286K6pohQcTKYqnS1YhWrCiS4gz7Xi34sdwMe9USZ7u"))

# def getTokenInfo(tokenAddress, seed):
#     #tokenAddress = request.args.get("tokenAddress")
#     #cid = request.args.get("cid")
#     #seed = request.args.get("seed")
#     infura_url = 'https://rinkeby.infura.io/v3/ce27477f441742249fa8614a3b3872de'
#     web3 = Web3(Web3.HTTPProvider(infura_url))
#     tokenAddress = Web3.toChecksumAddress(tokenAddress)

#     abi = json.loads('[{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"string","name":"baseSiteURI","type":"string"},{"internalType":"string","name":"seed","type":"string"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"royaltyRate","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_baseSiteURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_price","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_royaltyRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_seed","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"create","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"imageURI","type":"string"}],"name":"formatTokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInfo","outputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"string","name":"imgUri","type":"string"},{"internalType":"string","name":"baseSiteURI","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"uint256","name":"curSupply","type":"uint256"}],"internalType":"struct GenerativeTokenInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIterations","outputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"string","name":"tokenURI","type":"string"},{"internalType":"address","name":"owner","type":"address"}],"internalType":"struct TokenInfo[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
#     address = tokenAddress

#     contract = web3.eth.contract(address=address, abi=abi)

#     #need to put .call() at the end to call the smart contract
#     contractInfo = contract.functions.getInfo().call()

#     #convert supply to Wei witch is 18 decimal places)
#     print('contract info: ', contractInfo)
# #getTokenInfo()
