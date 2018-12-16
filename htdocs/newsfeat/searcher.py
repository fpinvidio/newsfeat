import json
from bson import json_util
import time

from pymongo import MongoClient
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir

class Searcher:
    """
    Wraps the MeTA search engine and its rankers.
    """
    def __init__(self, idx_path):
        """
        Create/load a MeTA inverted index based on the provided config file and
        set the default ranking algorithm to Okapi BM25.
        """
        self.ix = open_dir(idx_path)

    def search(self, search_term):
        topN = 10
        client = MongoClient('mongodb://newsfeat:N3usF3at@ds043062.mlab.com:43062/newsfeat')
        db = client.newsfeat
        news = db.news
        response = {'query': search_term, 'results': []}
        start = time.time()
        with self.ix.searcher(weighting=scoring.Frequency) as searcher:
            query = QueryParser("content", self.ix.schema).parse(search_term)
            results = searcher.search(query, limit=topN)
            count = len(results) if len(results) < topN else topN
            for i in range(count):
                result = news.find({'file_path': results[i]['title']})
                for doc in result:
                    response['results'].append(doc)
        response['elapsed_time'] = time.time() - start
        return json.dumps(response,default=json_util.default)
