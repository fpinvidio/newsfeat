import json
from bson import json_util
import time
import metapy

from pymongo import MongoClient
from searcher import Searcher
from indexer import Indexer
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    searcher = Searcher("/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/idx")
    return searcher.search(request.args.get('query'))

@app.route('/search_index')
def search_index():
    indexer = Indexer("data", "/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/idx")
    return indexer.index()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
