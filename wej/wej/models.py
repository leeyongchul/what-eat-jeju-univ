from django.db import models

class User(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)

class Restaurant(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    callNumber = models.CharField(max_length=15, unique=True)
    viewCount = models.IntegerField(default=0)
    restaurantImg = models.CharField(max_length=100) #comment img로 바꿀것
    keyword = models.CharField(max_length=100)


class Rate(models.Model):
    seq = models.AutoField(auto_created=True, primary_key=True)
    restaurantId = models.ForeignKey('Restaurant')
    rate = models.FloatField(default=0)


class Menu(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)


class RestaurantMenu(models.Model):
    restaurantId = models.ForeignKey('Restaurant')
    menuId = models.ForeignKey('Menu')
    price = models.IntegerField(null=False)