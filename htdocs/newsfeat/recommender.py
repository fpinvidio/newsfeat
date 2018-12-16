import numpy as np
from pymongo import MongoClient
from lightfm import LightFM
from scipy.sparse import coo_matrix
import json
from bson import json_util

class Recommender:
    """
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        # client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
        client = MongoClient()
        db = client.newsfeat
        news = db.news
        # news.update_many({}, {"$set" : {"user_likes": [0, 0, 0, 0, 0]}})
        train = list(news.find({}, {'user_likes': 1, '_id': 0}))

        def extract_likes(col):
            return col['user_likes']

        def extract_ids(col):
            return col['_id']

        train = map(extract_likes, train)
        train = map(list, zip(*train))
        train = coo_matrix(train)
        model = LightFM(loss='warp')
        model.fit(train, epochs=20)

        items = list(news.find({}, {'_id': 1}))
        items = np.array(map(extract_ids, items))
        self.model = model
        self.items = items
        self.train = train

    def recommend(self, user_ids):
        client = MongoClient()
        db = client.newsfeat
        news = db.news
        # number of users and news in training data
        n_users, n_items = self.train.shape
        # generate recommendations for each user we input
        response = {'results': []}
        for user_id in user_ids:
            # news our model predicts they will like
            scores = self.model.predict(user_id, np.arange(n_items))
            # rank them in order of most liked to least
            top_items = list(self.items[np.argsort(-scores)])
            top_items = top_items[:10]
            top_news = list(news.find({'_id': {'$in': list(top_items)}}))
            response['results'] = top_news
        return json.dumps(response, default=json_util.default)
