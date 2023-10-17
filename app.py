import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from http import client
from pymongo import MongoClient
from datetime import datetime


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary/show', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary/save', methods=['POST'])
def save_diary():
  
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    # Input Gambar
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    date_up = today.strftime('%Y-%m-%d')
    filename = f'static/{mytime}.{extension}'
    
    # Input Profile
    profile = request.files["profile_give"]
    extension2 = profile.filename
    filename2 = f'static/{extension2}'
    file.save(filename)
    profile.save(filename2)

    doc = {
        'profile':filename2,
        'image':filename,
        'date':date_up,
        'title':title_receive,
        'content':content_receive,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

