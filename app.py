from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource, Api
from json import dumps, loads
import boto3

from faker import Faker
fake = Faker()


bookTable = boto3.resource('dynamodb').Table('Books')
app = Flask(__name__)
api = Api(app)

import logging	
import sys	
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def genLogs(requestName):
    for i in range(100):
        print("Request for " + requestName)
        print (fake.email()) 
        print(fake.country()) 
        print(fake.name()) 
        print(fake.text()) 
        print(fake.url())

class Books(Resource):
    def get(self):
        genLogs('books_get')
        resp = bookTable.scan()
        return jsonify(resp['Items'])
    def post(self):
        genLogs('books_post')
        with bookTable.batch_writer() as batch:
            batch.put_item(Item=request.json)
        return jsonify({'data':request.json,'status':'success'})

class Book(Resource):
    def get(self):
        genLogs('book_get')
        if ('author' in request.args) and ('title' in request.args):
            try:
                resp = bookTable.get_item(Key={"Author": request.args['author'], "Title": request.args['title']})
                return jsonify(resp['Item'])
            except:
                return jsonify({})
        else:
            return {"msg":"Pass Author and Title to query"}

api.add_resource(Books, '/books')
api.add_resource(Book, '/book') 

@app.route('/front/<path:path>')
def send_assets(path):
    return send_from_directory('build', path)

@app.route('/')
def index():
    print('angular app is deployed for user ip') 
    return send_from_directory("build","index.html")

if __name__ == '__main__':
     app.run()