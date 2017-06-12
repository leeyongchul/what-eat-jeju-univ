# wej/views.py
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response,redirect
from wej.models import User, Restaurant, RestaurantMenu, Menu, Rate
from django.db.models import Avg
import logging
import json

logger = logging.getLogger('django')

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

        restaurantList = Restaurant.objects.order_by( 'viewCount' )
        if len( restaurantList ) > 10:
            restaurantList = restaurantList[10:]

        storeList = []

        for restaurant in restaurantList:
            RateResult = Rate.objects.filter( restaurantId=restaurant.id )
            if len( RateResult ) > 0:
                rateAvg = float( RateResult.aggregate( Avg('rate') )['rate__avg'] )
            else:
                rateAvg = 0

            storeList.append( {
                'storeId' : restaurant.id,
                'storeName': restaurant.name,
                'callNumber' : restaurant.callNumber,
                'viewCount' : restaurant.viewCount,
                'rate' : rateAvg
            } )

        responseData['storeList'] = storeList

        return render(request, 'bestrestaurant.html', responseData)


def searchrestaurant(request):
    if request.method == 'GET':
        storeId = int( request.GET.get('storeid', '0') )

        responseData = {}

        restaurant = Restaurant.objects.get(id=storeId)
        restaurant.viewCount += 1
        restaurant.save()

        RateResult = Rate.objects.filter(restaurantId=restaurant.id)
        if len(RateResult) > 0:
            rateAvg = float(RateResult.aggregate(Avg('rate'))['rate__avg'])
        else:
            rateAvg = 0

        responseData['store'] = {
            'storeId' : restaurant.id,
            'storeName': restaurant.name,
            'callNumber' : restaurant.callNumber,
            'viewCount' : restaurant.viewCount,
            'rate': rateAvg
        }

        # {'storeId':8, 'storeName':'store1','callNumber':'000-0000-0000', 'searchCount':10, 'rate':4.5}

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

def addDatabasePageView(request):

    if request.method == 'GET':
        if request.session['user_id'] and request.session['user_id'] == 'admin':
            return render(request, 'add_database.html', {})
        else:
            return redirect('/')

def saveDatabase(request):

    if request.method == 'GET':
        type = request.GET.get('data_type', '')

        if type == 'store':
            return storeDataSave( request.GET.get('name',''), request.GET.get('call_number', ''), request.GET.get('keyword', ''))
        elif type == 'menu':
            ''
        elif type == 'store_menu':
            ''
        else:
            return HttpResponse(status=404)

def storeDataSave( name='', callNumber='', keyword='', img=None):

    logger.debug('name={}, callNumber={}, keyword={}', name, callNumber, keyword)

    if name == '':
        return HttpResponse(status=404)

    restaurant = Restaurant.objects.create(name=name, keyword=keyword, callNumber=callNumber)

    if restaurant:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)