from news.lib.search_engine.searcher import Searcher
from django.http import JsonResponse

def index(request):
    searcher = Searcher()
    search_data = {'query': request.GET.get('query', '')}
    return JsonResponse(searcher.search(search_data))
