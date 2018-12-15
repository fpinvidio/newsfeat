import metapy
import pymongo
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
db = client.newsfeat
news = db.news
idx = metapy.index.make_inverted_index('config.toml')
ranker = metapy.index.OkapiBM25()
query = metapy.index.Document()
query.content("london")
top_docs = ranker.score(idx, query, num_results = 25)
for num, (d_id, _) in enumerate(top_docs):
    original_id = idx.metadata(d_id).get('path').strip()
    result = news.find({'_id': ObjectId(original_id)})
    for doc in result:
        print(doc["title"])
