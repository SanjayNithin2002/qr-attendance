from flask import Flask, render_template, send_file, request
import png
from pyqrcode import QRCode
import pyqrcode
import json
import uuid
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



app = Flask(__name__)
rand = 0

@app.route("/")
def generate_qr():
    global rand 
    rand = uuid.uuid4()
    s = "http://127.0.0.1:5000/qrcode/" + str(rand)
    url = pyqrcode.create(s)
    filename = "lib/{id}.png".format(id=rand)
    url.png(filename, scale = 6)
    return send_file(filename, mimetype='image/gif')
    
@app.route("/qrcode/<string:rand>")
def handle_request(rand):
    string = "lib/{id}.png".format(id=rand)
    return render_template("form.html",string = string)

@app.route("/qrcode/postData" , methods=['POST'])
def handle_post():
    current_data = {
            "name" : request.form['name'],
            "regno" : request.form['regno'],
            "id" : str(rand)
    }
    db.collection("users").add(current_data)
    return render_template("result.html")

@app.route("/view")
def view():
   arr = [doc.to_dict() for doc in db.collection("users").stream()]
   relevant_data = [data for data in arr if data['id'] == str(rand)]
   return render_template("table.html",students = relevant_data)

if __name__ == '__main__':
    app.run(debug=True)
    