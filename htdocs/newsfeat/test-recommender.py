import numpy as np
from pymongo import MongoClient
from lightfm.datasets import fetch_movielens
from lightfm import LightFM
from scipy.sparse import coo_matrix
import scipy.sparse as sparse
import scipy

#client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
client = MongoClient()
db = client.newsfeat
news = db.news
#news.update_many({}, {"$set" : {"user_likes": [0, 0, 0, 0, 0]}})
train = list(news.find({}, {'user_likes': 1, '_id': 0 }))

def extract_likes(col):
    return col['user_likes']
def extract_ids(col):
    return str(col['_id'])

train = map(extract_likes, train)
train = map(list, zip(*train))
train = coo_matrix(train)
model = LightFM(loss='warp')
model.fit(train, epochs=20)

items = list(news.find({}, {'_id': 1 }))
items = np.array(map(extract_ids, items))

def sample_recommendation(model, data, user_ids):
    #number of users and movies in training data
    n_users, n_items = data.shape
    #generate recommendations for each user we input
    for user_id in user_ids:
        #movies our model predicts they will like
        scores = model.predict(user_id, np.arange(n_items))
        #rank them in order of most liked to least
        top_items = items[np.argsort(-scores)]

sample_recommendation(model, train, [4])

