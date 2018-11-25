import glob
import json
import pymongo
from pymongo import MongoClient

news_file = open('/Users/federicoperezinvidio/Projects/illinois/newsfeat/news.dat', "w+")
meta_file = open('/Users/federicoperezinvidio/Projects/illinois/newsfeat/metadata.dat', "w+")
client = MongoClient()
db = client.newsfeat
news = db.news
for filename in glob.iglob('/Users/federicoperezinvidio/Projects/illinois/newsfeat/news-please/data/2018/11/16/**/*.json', recursive=True):
    #print(filename)
    with open(filename) as data_file:
        file_json = json.loads(data_file.read())
        #print(file_json["url"])
        text = file_json["text"]
        if isinstance(text, str):
            post_id = news.insert_one(file_json).inserted_id
            news_file.write("%s\n" % text.replace("\n", ""))
            meta_file.write("%s\n" % post_id)
news_file.close()