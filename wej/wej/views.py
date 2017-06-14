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
    ''' 가게 리스트를 조회한다 '''
    if request.method == 'GET':
        responseData = {}

        restaurantList = Restaurant.objects.order_by( 'viewCount' )
        if len( restaurantList ) > 10:
            restaurantList = restaurantList[10:]

        storeList = []

        for restaurant in restaurantList:
            RateResult = Rate.objects.filter( restaurantId=restaurant.restaurantId )
            if len( RateResult ) > 0:
                rateAvg = float( RateResult.aggregate( Avg('rate') )['rate__avg'] )
            else:
                rateAvg = 0

            storeList.append( {
                'storeId' : restaurant.restaurantId,
                'storeName': restaurant.restaurantName,
                'callNumber' : restaurant.callNumber,
                'viewCount' : restaurant.viewCount,
                'rate' : rateAvg
            } )

        responseData['storeList'] = storeList

        return render(request, 'bestrestaurant.html', responseData)

def searchrestaurant(request):
    ''' 가게 정보 검색한다 '''
    if request.method == 'GET':
        storeId = int( request.GET.get('storeid', '0') )

        responseData = {}

        restaurant = Restaurant.objects.get(restaurantId=storeId)
        restaurant.viewCount += 1
        restaurant.save()

        RateResult = Rate.objects.filter(restaurantId=restaurant.restaurantId)
        if len(RateResult) > 0:
            rateAvg = float(RateResult.aggregate(Avg('rate'))['rate__avg'])
        else:
            rateAvg = 0

        responseData['store'] = {
            'storeId' : restaurant.restaurantId,
            'storeName': restaurant.restaurantName,
            'callNumber' : restaurant.callNumber,
            'viewCount' : restaurant.viewCount,
            'rate': rateAvg
        }

        restaurantMenuList = RestaurantMenu.objects.filter(restaurantId = restaurant)

        menuList = []
        for restaurantMenu in restaurantMenuList:
            menuList.append({
                'number': restaurantMenu.pk,
                'name': restaurantMenu.menuId.menuName,
                'price': restaurantMenu.price,
                'imgurl': 'http://placehold.it/320x150'
            })

        responseData['menulist'] = menuList
        #     [
        #     {},
        #     {'number':2, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
        #     {'number':3, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
        #     {'number':4, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
        #     {'number':5, 'name':'감자탕', 'price':7000, 'imgurl':'http://placehold.it/320x150' },
        # ]

        return render(request, 'search_restaurant.html', responseData)

def ratestore(request):
    ''' 평점을 입력한다 '''

    if request.method == 'GET':
        storeId = request.GET.get('store_id', '')
        menuId = request.GET.get('store_id', '')

        responseData = {}

        return HttpResponse(json.dumps(responseData), content_type="application/json")

    if request.method == 'POST':
        storeId = request.GET.get('store_id', '')
        menuId = request.GET.get('menu_id', '')

        responseData = {}

        return  HttpResponse(json.dumps(responseData), content_type="application/json")

def login(request):
    ''' 로그인 '''

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
    ''' 회원가입 '''

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
    ''' 로그아웃 '''

    if request.method == 'GET':
        request.session['user_id'] = ''

        return HttpResponse(status=200)

def addDatabasePageView(request):
    ''' 데이터베이스 저장 화면 이동 '''

    if request.method == 'GET':
        if request.session['user_id'] and request.session['user_id'] == 'admin':
            return render(request, 'add_database.html', {})
        else:
            return redirect('/')

def saveDatabase(request):
    ''' 데이터를 저장한다 '''

    if request.method == 'GET':
        type = request.GET.get('data_type', '')

        if type == 'store':
            return storeDataSave( request.GET.get('name',''), request.GET.get('call_number', ''), request.GET.get('keyword', ''))
        elif type == 'menu':
            return menuDataSave( request.GET.get('name','') )
        elif type == 'store_menu':
            return restaurantMenuDataSave( int(request.GET.get('store_id','')), int(request.GET.get('menu_id','')), int(request.GET.get('price','0')) )
        else:
            return HttpResponse(status=404)

def storeDataSave( name='', callNumber='', keyword='', img=None):
    ''' 가게정보를 저장한다 '''

    logger.debug('name={}, callNumber={}, keyword={}'.format(name, callNumber, keyword) )

    if name == '':
        return HttpResponse(status=404)

    restaurant = Restaurant.objects.create(retaueantName=name, keyword=keyword, callNumber=callNumber)

    if restaurant:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

def menuDataSave( name ):
    ''' 메뉴명을 저장 한다 '''

    logger.debug('name={}'.format( name ))

    if name == '':
        return HttpResponse(status=404)

    menu = Menu.objects.create(menuName=name)

    if menu:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

def loadStoreMenuInfo(request):
    ''' 가게정보와 메뉴 정보를 구한다. '''

    if request.method == 'GET':
        restaurantList = Restaurant.objects.all()

        storelist = []
        for restaurant in restaurantList:
            storelist.append({
                'id': restaurant.restaurantId,
                'name': restaurant.restaurantName
            })

        menuList = Menu.objects.all()

        menulist = []
        for menu in menuList:
            menulist.append({
                'id': menu.menuId,
                'name': menu.menuName
            })

        return HttpResponse(json.dumps({'storelist':storelist, 'menulist':menulist}), content_type="application/json")

def restaurantMenuDataSave( restaurantId, menuId, price ):
    ''' 가게 메뉴 정보를 저장한다 '''

    logger.debug('restaurantId={}, menuId={}, price={}'.format(restaurantId, menuId, price))

    restaurant = Restaurant.objects.get(restaurantId=restaurantId)
    menu = Menu.objects.get(menuId=menuId)

    if not restaurant or not menu or price == 0:
        return HttpResponse(status=404)

    restaurantMenu = RestaurantMenu.objects.create(restaurantId=restaurant, menuId=menu, price=price)

    if restaurantMenu:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)