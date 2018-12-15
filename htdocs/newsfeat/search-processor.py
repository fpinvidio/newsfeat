from searcher import Searcher

searcher = Searcher()
search_data = {'query': 'London'}#request.args.get('query')}
#print(search_data)
results = searcher.search(search_data)
print(results)
