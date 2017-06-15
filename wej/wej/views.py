# wej/views.py
from django.template.context import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, render_to_response,redirect
from wej.models import User, Restaurant, RestaurantMenu, Menu, Rate, SearchKeyword
from django.db.models import Avg
import logging
import json
import re

logger = logging.getLogger('django')
responseFalse = {'resultStatus':False}

def searchkeywordlist(request):

    if request.method == 'GET':
        responseData = {}

        searchKeywordList = SearchKeyword.objects.order_by('-searchCount')
        if len( searchKeywordList ) > 10:
            searchKeywordList = searchKeywordList[:10]

        keywordList = []
        for searchKeyword in searchKeywordList:
            keywordList.append( searchKeyword.searchKeyword )

        responseData['keywordList'] = keywordList

        return render(request, 'search_keyword_list.html', responseData)

def searchkeywordView(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        responseData = {}

        if not keyword:
            return render(request, 'search_keyword_result.html', responseFalse)

        restaurantList = Restaurant.objects.filter(keyword__icontains=keyword)
        if len( restaurantList ) > 0:
            searchkeywordFilter = SearchKeyword.objects.filter(searchKeyword=keyword)

            if len( searchkeywordFilter ) > 0:
                searchKeyword = SearchKeyword.objects.get(searchKeyword=keyword)
            else :
                searchKeyword = SearchKeyword.objects.create(searchKeyword=keyword)

            searchKeyword.searchCount += 1
            searchKeyword.save()

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
                'imgurl' : restaurant.restaurantImg,
                'rate' : rateAvg
            } )

        responseData['keyword'] = keyword
        responseData['storeList'] = storeList

        return render(request, 'search_keyword_result.html', responseData)

def bestrestaurant(request):
    ''' 가게 리스트를 조회한다 '''
    if request.method == 'GET':
        responseData = {}

        restaurantList = Restaurant.objects.order_by( '-viewCount' )

        if len( restaurantList ) > 10:
            restaurantList = restaurantList[:10]

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
                'imgurl': restaurant.restaurantImg,
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
            'imgurl': restaurant.restaurantImg,
            'rate': rateAvg
        }

        restaurantMenuList = RestaurantMenu.objects.filter(restaurantId = restaurant)

        menuList = []
        for restaurantMenu in restaurantMenuList:
            menuRate = Rate.objects.filter(restaurantId=restaurant.restaurantId, restaurantMenuId=restaurantMenu.pk)
            if len( menuRate ) > 0:
                rate = float( menuRate.aggregate(Avg('rate'))['rate__avg'] )
            else:
                rate = 0

            menuList.append({
                'number' : restaurantMenu.pk,
                'name' : restaurantMenu.menuId.menuName,
                'price' : restaurantMenu.price,
                'imgurl' : restaurantMenu.restaurantMenuImg,
                'rate' : rate
            })

        responseData['menulist'] = menuList

        return render(request, 'search_restaurant.html', responseData)

def ratestore(request):
    ''' 평점을 입력한다 '''

    if request.method == 'GET':
        restaurantId = int( request.GET.get('store_id', '0') )
        rmenu_id = int( request.GET.get('menu_id', '0') )
        rateScore = float( request.GET.get('rate', '0') )

        logger.debug("ratestore = {}, {}, {}".format(restaurantId, rmenu_id, rateScore))

        restaurant = Restaurant.objects.get(restaurantId=restaurantId)
        restaurantMenu = RestaurantMenu.objects.get(pk=rmenu_id )

        if not restaurant or not restaurantMenu :
            return HttpResponse(json.dumps(responseFalse), content_type="application/json")

        rate = Rate.objects.create(restaurantId=restaurant, restaurantMenuId=restaurantMenu, rate=rateScore)

        if rate:
            return HttpResponse(json.dumps({'resultStatus': True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps( responseFalse ), content_type="application/json")


def login(request):
    ''' 로그인 '''

    if request.method == 'POST':
        id = request.POST.get('id','')
        pw = request.POST.get('pw','')

        user = User.objects.get(id=id)

        if not user.password == pw:
            return HttpResponse(status=404)

        request.session['user_id'] = user.id
        if bool( re.match( 'admin', user.id ) ):
            request.session['is_admin_user'] = True
        else:
            request.session['is_admin_user'] = False

        return HttpResponse(status=200)

def signup(request):
    ''' 회원가입 '''

    if request.method == 'POST':
        id = request.POST.get('id','')
        pw = request.POST.get('pw','')

        if not id or not pw:
            return HttpResponse(status=404)

        if User.objects.get(id=id):
            return HttpResponse(status=404)

        user = User.objects.create(id=id, password=pw)

        if user:
            request.session['user_id'] = user.id
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

def logout(request):
    ''' 로그아웃 '''

    if request.method == 'GET':
        request.session['user_id'] = ''
        request.session['is_admin_user'] = False

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
            return storeDataSave( request.GET.get('name',''), request.GET.get('call_number', ''), request.GET.get('keyword', ''), request.GET.get('img_link','http://placehold.it/320x150'))
        elif type == 'menu':
            return menuDataSave( request.GET.get('name','') )
        elif type == 'store_menu':
            return restaurantMenuDataSave(
                int(request.GET.get('store_id','')), int(request.GET.get('menu_id','')), int(request.GET.get('price','0')), request.GET.get('img_link',''),
                request.GET.get('store_name',''), request.GET.get('menu_name','')
            )
        else:
            return HttpResponse(status=404)

def storeDataSave( name='', callNumber='', keyword='', img='' ):
    ''' 가게정보를 저장한다 '''

    logger.debug('name={}, callNumber={}, keyword={}, img={}'.format(name, callNumber, keyword, img) )
    keyword.replace('\s','')

    if name == '':
        return HttpResponse(status=404)

    restaurant = Restaurant.objects.create(restaurantName=name, keyword=keyword, callNumber=callNumber, restaurantImg=img)

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
        option = request.GET.get('option', 'menu')

        restaurantList = Restaurant.objects.all()

        storelist = []
        for restaurant in restaurantList:
            storelist.append({
                'id': restaurant.restaurantId,
                'name': restaurant.restaurantName
            })

        menulist = []
        if option == 'menu':
            menuList = Menu.objects.all()

            for menu in menuList:
                menulist.append({
                    'id': menu.menuId,
                    'name': menu.menuName
                })
        elif option == 'img':
            restaurantMenuList = RestaurantMenu.objects.all()

            for restaurantMenu in restaurantMenuList:
                restaurant = restaurantMenu.restaurantId
                menu = restaurantMenu.menuId
                name = restaurant.restaurantName + '_' + menu.menuName

                menulist.append({
                    'id' : restaurantMenu.pk,
                    'name' : name
                })

        return HttpResponse(json.dumps({'storelist':storelist, 'menulist':menulist}), content_type="application/json")

def restaurantMenuDataSave( restaurantId, menuId, price, img, restaurantName, menuName ):
    ''' 가게 메뉴 정보를 저장한다 '''

    logger.debug('restaurantId={}, menuId={}, price={}, img={}'.format(restaurantId, menuId, price, img))
    if not img:
        img = 'http://placehold.it/320x150'

    restaurant = Restaurant.objects.get(restaurantId=restaurantId)
    menu = Menu.objects.get(menuId=menuId)

    if not restaurant:
        restaurant = Restaurant.objects.get(restaurantName=restaurantName)

    if not menu:
        menu = Menu.objects.get(menuName=menuName)
        if not menu and restaurant:
            menu = Menu.objects.create(menuName=menuName)

    if not restaurant or not menu or price == 0:
        return HttpResponse(status=404)

    restaurantMenu = RestaurantMenu.objects.create(restaurantId=restaurant, menuId=menu, price=price, restaurantMenuImg=img)

    if restaurantMenu:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)