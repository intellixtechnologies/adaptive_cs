import json
from flask import Flask,request,make_response,jsonify
import requests
from threading import Thread

app = Flask(__name__)
@app.route('/test')
def test():
    return 'VoxImplant API is up . Try the POST method now...'


@app.route('/getPhoneNumber', methods=['POST']) #allow POST requests
def getPhoneNumber():
    req_data = request.get_json()
    phone_num = req_data['phone_num']
    return make_response(jsonify({'fulfillmentText':text }))


@app.route('/getPhoneNumber', methods=['POST']) #allow POST requests
def sendemail():
    req_data = request.get_json()
    phone_num = req_data['phone_num']
    req = {"phone": phone_num}
    email_id = getCustomerRecordFromDB(req))['EMAIL']
    return make_response(jsonify({'email_id': email}))

def run():
    app.run(host='0.0.0.0',port=8888)

t = Thread(target=run)
t.start()