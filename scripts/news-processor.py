import glob
import json
import pymongo
import logging
import os

from pymongo import MongoClient
from bson.objectid import ObjectId

news_file = open('/Users/federicoperezinvidio/Projects/illinois/newsfeat/news.dat', "w+")
meta_file = open('/Users/federicoperezinvidio/Projects/illinois/newsfeat/metadata.dat', "w+")
client = MongoClient()
db = client.newsfeat
news = db.news
count = 1
for filename in glob.iglob('/Users/federicoperezinvidio/Projects/illinois/newsfeat/news-please/data/2018/11/16/**/*.json', recursive=True):
    #print(filename)
    with open(filename) as data_file:
        file_json = json.loads(data_file.read())
        #print(file_json["url"])
        text = file_json["text"]
        if isinstance(text, str) and "Sorry! We're currently performing maintenance on the site." not in text:
            print("Parsing doc #", count)
            #print(text[0:50])
            count = count + 1
            if count > 0:
                # file_json["giveme5w1h"] = extract_article(file_json)
                # post_id = news.insert_one(file_json).inserted_id
                found_one = news.find_one({"text": file_json["text"]})
                if found_one is not None:
                    dynam = open('/Users/federicoperezinvidio/Projects/illinois/newsfeat/data/' + str(count) + ".txt",
                                 "w+")
                    dynam.write("%s" % file_json["title"])
                    #dynam.write("\n%s" % found_one.get('_id'))
                    news_file.write("%s\n" % text.replace("\n", ""))
                    meta_file.write("%s\n" % found_one.get('_id'))
news_file.close()