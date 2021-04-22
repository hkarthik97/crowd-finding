from flask import Flask, render_template, request, url_for, redirect,jsonify,make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from time import time
import json
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://karthik:karthik@cluster0.dva2k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app,tls=True,tlsAllowInvalidCertificates=True)

todos = mongo.db.People

@app.route('/test')
def test():
    # saved_todos = todos.find()
    # print(saved_todos)
    datas = todos.find().sort("_id", -1).limit(1)
    wificount = datas[0]["Devices"]
    return render_template('base.html', wificount=wificount)
@app.route('/')
def index():
    saved_todos = todos.find()
    print(saved_todos)
    return render_template('index.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))

@app.route('/data')
def data():
    datas = todos.find().sort("_id", -1).limit(1)
    wificount = datas[0]["Devices"]
    data = [time() * 1000, wificount]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
if __name__ == '__main__':
    app.debug = True
    app.run()