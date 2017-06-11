# wej/views.py
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from wej.models import User

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

def ratestore(request):
    if request.method == 'GET':
        storeId = request.GET.get('store_id', '')
        menuId = request.GET.get('store_id', '')

        responseData = {}


        return HttpResponse(json.loads(responseData), content_type="application/json")

    if request.method == 'POST':
        storeId = request.GET.get('store_id', '')
        menuId = request.GET.get('menu_id', '')

        responseData = {}

        return  HttpResponse(json.loads(responseData), content_type="application/json")

def login(request):

    if request.method == 'POST':
        id = request.POST.get('id','')
        pw = request.POST.get('pw','')

        user = User.objects.get(id=id)

        if user.password == pw:
            request.session['user_id'] = user.id
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

def signup(request):

    if request.method == 'POST':
        id = request.POST.get('id','')
        pw = request.POST.get('pw','')

        User.objects.create(id=id, password=pw)
        user = User.objects.get(id=id)

        if user:
            request.session['user_id'] = user.id
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

def logout(request):

    if request.method == 'GET':
        request.session['user_id'] = ''

        return HttpResponse(status=200)
