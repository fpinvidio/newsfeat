import json
from bson import json_util
import time
import metapy

from pymongo import MongoClient
from searcher import Searcher
from flask import Flask
from flask import render_template
from flask import request

import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import codecs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    ix = open_dir("idx")
    query_str = request.args.get('query')
    topN = 10
    client = MongoClient()
    db = client.newsfeat
    news = db.news
    response = {'query': query_str, 'results': []}
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=topN)
        count = len(results) if len(results) < 10 else 10
        for i in range(count):
            result = news.find({'file_path': results[i]['title']})
            for doc in result:
                response['results'].append(doc)
    return json.dumps(response,default=json_util.default)

@app.route('/search_index')
def search_index():
    root = "data"
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), \
                    content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists("idx"):
        os.mkdir("idx")

    # Creating a index writer to add document as per schema
    ix = create_in("idx", schema)
    writer = ix.writer()

    filepaths = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepaths:
        with codecs.open(path, "r", "utf-8") as f:
            content = f.read()
            writer.add_document(title=unicode(path.split("/")[1]), path=unicode(path.split("/")[0]), \
                                content=content, textdata=content)
    writer.commit()
    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
