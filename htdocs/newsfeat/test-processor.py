import os
from pymongo import MongoClient
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import codecs

root = "data"

client = MongoClient()
db = client.newsfeat
news = db.news
filepaths = [os.path.join(root, i) for i in os.listdir(root)]
for path in filepaths:
    f = open(path, "r")
    content = f.read()
    news.update_one({'title': content}, {"$set": {"file_path": unicode(path.split("/")[1])}})
