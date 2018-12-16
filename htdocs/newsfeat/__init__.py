from bson.objectid import ObjectId
from pymongo import MongoClient
from searcher import Searcher
from recommender import Recommender
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
    #searcher = Searcher("idx")
    return searcher.search(request.args.get('query'))

@app.route('/recommend')
def recommend():
    recommender = Recommender()
    user_id = int(request.args.get('user_id'))-1
    return recommender.recommend([user_id])

@app.route('/news/<string:id>/like', methods=['POST'])
def like_news(id):
    client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
    #client = MongoClient()
    db = client.newsfeat
    news = db.news
    article = news.find_one({'_id': ObjectId(id)})
    if article is not None:
        user_likes = article['user_likes']
        user_id = int(request.form.get('user_id')) - 1
        user_likes[user_id] = 1
        news.update({'_id': ObjectId(id)}, {"$set": {"user_likes": user_likes}})
        return "{success: true}"
    return "{success: false}"

@app.route('/news/<string:id>/dislike', methods=['POST'])
def dislike_news(id):
    client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
    #client = MongoClient()
    db = client.newsfeat
    news = db.news
    article = news.find_one({'_id': ObjectId(id)})
    if article is not None:
        user_likes = article['user_likes']
        user_id = int(request.form.get('user_id')) - 1
        user_likes[user_id] = -1
        news.update({'_id': ObjectId(id)}, {"$set": {"user_likes": user_likes}})
        return "{success: true}"
    return "{success: false}"


@app.route('/search_index')
def search_index():
    indexer = Indexer("data", "/var/www/cs410.fpinvidio.com/htdocs/newsfeat/htdocs/newsfeat/idx")
    #indexer = Indexer("data", "idx")
    return indexer.index()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
