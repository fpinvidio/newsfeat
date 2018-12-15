import json
import time
import metapy
import pymongo
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId

class Searcher:
    """
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        self.idx = metapy.index.make_inverted_index('config.toml')
        self.default_ranker = metapy.index.OkapiBM25()

    def search(self, request):
        """
        Accept a JSON request and run the provided query with the specified
        ranker.
        """
        client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/')
        db = client.newsfeat
        news = db.news

        start = time.time()
        query = metapy.index.Document()
        query.content(request['query'])
        ranker = self.default_ranker
        response = {'query': request['query'], 'results': []}

        for num, (d_id, _) in ranker.score(self.idx, query, 25):
            original_id = self.idx.metadata(d_id).get('path').strip()
            result = news.find({'_id': ObjectId(original_id)})
            for doc in result:
                response['results'].append(doc)

        response['elapsed_time'] = time.time() - start
        return json.dumps(response, indent=2)