<<<<<<< HEAD
from flask import Flask, request, make_response, url_for, send_file
import flask
import base64
from PIL import Image
import io
import os
from os import path
import json
import string
import random
import requests
import http.client
from datetime import datetime, timedelta
from pytz import timezone
import pytz

app = Flask(__name__)

    
def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def testmatch(image, latitude, longitude):
    
    conn = http.client.HTTPSConnection("api.kairos.com")

    payload = "{\n\t\"image\" : \""+image+"\",\n    \"gallery_name\":\"mugshots\"\n}"

    headers = {
        'content-type': "text/plain",
        'app_id': "e71c42d9",
        'app_key': "0b4faa77a1a481cc52721a2294fe2825",
        'cache-control': "no-cache",
        'postman-token': "5e0fe798-c015-03ad-f032-271801ba406e"
        }

    conn.request("POST", "/recognize", payload, headers)
    
    res = conn.getresponse()
    data = res.read()

    #return(json.loads(data.decode("utf-8"))['images'][0]['candidates'][0]['subject_id'])
    if 'Errors' in json.loads(data.decode("utf-8")):
        print('not a match')
        return("test")
    else:
        filename = os.path.join(app.static_folder, 'data.json')
        name = json.loads(data.decode("utf-8"))['images'][0]['candidates'][0]['subject_id']
        with open('data.json') as file:
            data2 = json.load(file)
        with open('felons.json') as file:
            felons = json.load(file)
            
        object_data = {}
        
        for key in felons:
            if key["name"] == name:
                print('match found')
                object_data = key
        
        print(object_data)
        
        object_data['lat'] = latitude
        object_data['long'] = longitude
        
        now_utc = datetime.now(timezone('UTC'))
        fullTime = now_utc.astimezone(timezone('US/Pacific'))
        if fullTime.minute < 10:
            time = str(fullTime.hour) + ':0' + str(fullTime.minute)
        else:
            time = str(fullTime.hour) + ':' + str(fullTime.minute)
        object_data['time'] = time
        
        appendData = True
        for key in data2:
            if key["name"] == name and key["time"] == time:
                appendData = False
        
        if appendData:
            data2.append(object_data)
            with open("data.json","wt") as fo:
                fo.write(json.dumps(data2))
    
@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/image/<path:path>")
def image(path):
   return(send_file(path))



@app.route('/upload', methods=['POST'])
def upload():
    testmatch(request.form['image'], request.form['longitude'], request.form['latitude'])
    return("test")

    
@app.route('/felonies', methods=['GET'])
def felonies():
    return(send_file('data.json'))
     

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
=======
from flask import Flask, request
import base64
from PIL import Image
import io

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/upload', methods=['POST']) 
def upload():
	string = base64.b64decode(request.form['image'])
	image = Image.open(io.BytesIO(string))
	return "nothing";

if __name__ == "__main__":
    app.run()
>>>>>>> 55196a6012411b50f58cedb6b6defb11f6ee1e53



