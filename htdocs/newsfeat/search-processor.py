import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import codecs

ix = open_dir("idx")
query_str = "Trump"
topN = 10

with ix.searcher(weighting=scoring.Frequency) as searcher:
    query = QueryParser("content", ix.schema).parse(query_str)
    results = searcher.search(query, limit=topN)
    for i in range(topN):
        print(results[i]['title'], str(results[i].score),
              results[i]['textdata'])
