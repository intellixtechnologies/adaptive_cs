from flask import Flask,request,make_response,jsonify
from threading import Thread
import dialogflow_methods as d
import json
import requests
import helper.py

app = Flask(__name__) #create the Flask app
@app.route('/test')
def test():
    return 'DialogFlow Adaptive CS Demo API is up . Try the POST method now...'


@app.route('/dialogflowFulfillment', methods=['POST']) #allow POST requests
def dialogflowFulfillment():
    req_data = request.get_json()
    inputText = req_data['chatinput']
    sessionID = req_data['sessionid']
    userName = req_data['Name']
    userPhone = req_data['phone']
    return d.detect_intent_texts(inputText,sessionID, userName,userPhone)

def run():
    app.run(host='0.0.0.0',port=5555)

t = Thread(target=run)
t.start()