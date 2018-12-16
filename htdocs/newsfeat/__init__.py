from bson.objectid import ObjectId
from pymongo import MongoClient
from searcher import Searcher
from recommender import Recommender
from indexer import Indexer
from flask import Flask
from flask import render_template
from flask import request
import constants

app = Flask(__name__)

@app.route('/')
def index():
    """
        Index route for rendering the index.html template
    """
    return render_template('index.html')

@app.route('/search')
def search():
    """
        Route used for searching. Receives a query param and returns a json with all the results.
    """
    searcher = Searcher(constants.INDEX_PATH)
    return searcher.search(request.args.get('query'))

@app.route('/recommend')
def recommend():
    """
        Route used for recommending. Receives a user_id param for specifying the user and returns a json with all the results.
    """
    recommender = Recommender()
    user_id = int(request.args.get('user_id'))-1
    return recommender.recommend([user_id])

@app.route('/news/<string:id>/like', methods=['POST'])
def like_news(id):
    """
        POST Route used for liking an article. An id param is used for specifying
        the article and a user_id param is for identifying the user.
    """
    client = MongoClient(constants.MONGODB_CLIENT)
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
    """
        POST Route used for disliking an article. An id param is used for specifying
        the article and a user_id param is for identifying the user.
    """
    client = MongoClient(constants.MONGODB_CLIENT)
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
    """
        Additional route used for indexing the dataset.
    """
    indexer = Indexer(constants.CORPUS_NAME, constants.INDEX_PATH)
    return indexer.index()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
