"""wej URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from wej import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.searchkeywordlist, name="search_keyword_list"),
    url(r'^searchkeyword/$', views.searchkeywordView, name="search_keyword"),
    url(r'^bestrestaurant/$', views.bestrestaurant, name="best_restaurant"),
    url(r'^searchrestaurant/$', views.searchrestaurant, name="search_restaurant"),
    url(r'^ratestore/$', views.ratestore, name="search_restaurant"),
    url(r'^login/$', views.login, name="login"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^adddatabaseview/$', views.addDatabasePageView, name="add_database_view"),
    url(r'^savedatabase/$', views.saveDatabase, name="save_database"),
    url(r'^loadstoremenuinfo/$', views.loadStoreMenuInfo, name="load_store_menu_info"),
    url(r'^updateimg/$', views.updateImg, name="update_img"),

]
