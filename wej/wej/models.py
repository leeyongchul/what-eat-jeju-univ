from django.db import models

class User(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)

class Restaurant(models.Model):
    restaurantId = models.AutoField(auto_created=True, primary_key=True)
    restaurantName = models.CharField(max_length=50)
    callNumber = models.CharField(max_length=15, unique=True)
    viewCount = models.IntegerField(default=0)
    restaurantImg = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)


class Rate(models.Model):
    seq = models.AutoField(auto_created=True, primary_key=True)
    restaurantId = models.ForeignKey('Restaurant')
    rate = models.FloatField(default=0)


class Menu(models.Model):
    menuId = models.AutoField(auto_created=True, primary_key=True)
    menuName = models.CharField(max_length=50)


class RestaurantMenu(models.Model):
    restaurantId = models.ForeignKey(Restaurant, related_name='restaurant_rel', unique=False, default=0)
    menuId = models.ForeignKey(Menu, related_name='menu_rel', unique=False, default=0)
    restaurantMenuImg = models.CharField(max_length=100, default='')
    price = models.IntegerField(null=False)


class SearchKeyword(models.Model):
    searchKeyword = models.CharField(max_length=100, primary_key=True)
    searchCount = models.IntegerField(default=0)

