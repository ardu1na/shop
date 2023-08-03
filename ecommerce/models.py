from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=200)


class Subcategory(models.Model):
    name = models.CharField(max_length=200)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')






class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')

class Location(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')

class PayMethod(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pay_methods')







class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts')
    total = models.PositiveIntegerField(default=0)



class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    ammount = models.PositiveSmallIntegerField(default=1)
    


