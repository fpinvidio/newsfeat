import json
import time
import metapy
import pymongo
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings

if len(sys.argv) != 2:
    print("Usage: {} config.toml".format(sys.argv[0]))
    sys.exit(1)

cfg = sys.argv[1]

idx = metapy.index.make_inverted_index(cfg)
default_ranker = metapy.index.OkapiBM25()

client = MongoClient()
db = client.newsfeat
news = db.news

start = time.time()
query = metapy.index.Document()
query.content("Content")
ranker = default_ranker
response = {'query': "Content", 'results': []}

for num, (d_id, _) in ranker.score(idx, query, 25):
    original_id = idx.metadata(d_id).get('path').strip()
    result = news.find({'_id': ObjectId(original_id)})
    for doc in result:
        response['results'].append(doc)

response['elapsed_time'] = time.time() - start
print(json.dumps(response, indent=2))