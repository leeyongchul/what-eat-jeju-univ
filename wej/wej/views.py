# wej/views.py
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

import json

def searchkeywordlist(request):
    if request.method == 'GET':
        responseData = {}

        responseData['keywordList'] = [
            '정문',
            '후문',
            '식당이름',
            '밥',
            '자장면',
            '면',
            '돈까스',
            '국수',
            '국밥',
            '라면'
        ]

        return render(request, 'search_keyword_list.html', responseData)

def searchkeyword(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        responseData = {}

        responseData['keyword'] = keyword

        return render(request, 'search_keyword_result.html', responseData)

def bestrestaurant(request):
    if request.method == 'GET':
        responseData = {}

        responseData['storeList'] = [
            {'storeId':1, 'storeName':'store1','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':2, 'storeName':'store2','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':3, 'storeName':'store3','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':4, 'storeName':'store4','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':5, 'storeName':'store5','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':6, 'storeName':'store6','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':7, 'storeName':'store7','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
            {'storeId':8, 'storeName':'store8','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5},
        ]

        return render(request, 'bestrestaurant.html', responseData)


def searchrestaurant(request):
    if request.method == 'GET':
        storeId = int( request.GET.get('storeid', '0') )

        responseData = {}

        responseData['store'] = {'storeId':8, 'storeName':'store1','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5}
        responseData['menulist'] = [
            {'number':1, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
            {'number':2, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
            {'number':3, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
            {'number':4, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
            {'number':5, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
        ]

        return render(request, 'search_restaurant.html', responseData)
