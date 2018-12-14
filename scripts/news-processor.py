import glob
import json
import pymongo
import logging
import os

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor

from pymongo import MongoClient

def extract_article(news_json):
    extractor = MasterExtractor()
    #doc = Document.from_text(sample["text"], sample["date_publish"])
    doc = Document(news_json["title"], news_json["description"], news_json["text"], news_json["date_publish"])
    # or: doc = Document(title, lead, text, date_publish)
    doc = extractor.parse(doc)
    who = doc.get_top_answer('who').get_parts_as_text() if len(doc.get_answers('who')) > 0 else ""
    what = doc.get_top_answer('what').get_parts_as_text() if len(doc.get_answers('what')) > 0 else ""
    where = doc.get_top_answer('where').get_parts_as_text() if len(doc.get_answers('where')) > 0 else ""
    why = doc.get_top_answer('why').get_parts_as_text() if len(doc.get_answers('why')) > 0 else ""
    how = doc.get_top_answer('how').get_parts_as_text() if len(doc.get_answers('how')) > 0 else ""
    return {'who': who, 'what': what, 'where': where, 'why': why, 'how': how}

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
                try:
                    #file_json["giveme5w1h"] = extract_article(file_json)
                    #post_id = news.insert_one(file_json).inserted_id
                    found_one = news.find_one({"text": file_json["text"]})
                    if found_one is not None:
                        news_file.write("%s\n" % text.replace("\n", ""))
                        meta_file.write("%s\n" % found_one.get('_id'))
                except:
                    print("Exceptuib")
                    pass
news_file.close()