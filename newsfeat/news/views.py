from news.search_engine.searcher import Searcher
from django.shortcuts import render
from django.http import JsonResponse

import random
import pymongo
from pymongo import MongoClient

def index(request):
    context = {
        'latest_question_list': 1,
    }
    return render(request, 'news/index.html', context)

def search(request):
    searcher = Searcher()
    search_data = {'query': request.GET.get('query', '')}
    return JsonResponse(searcher.search(search_data))
