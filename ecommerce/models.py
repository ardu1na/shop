from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class ModelBase(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    date_deleted = models.DateTimeField(editable=False, null=True)
    state = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.state == False:
            self.date_deleted = timezone.now() 
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True
        
class Category(ModelBase):
    name = models.CharField(max_length=200)

    
    def __str__(self):
        return self.name
    
class Subcategory(ModelBase):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    def __str__(self):
            return self.name     

    
class Client(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    def __str__(self):
        return self.user.get_full_name()
    
class Location(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')

class PayMethod(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pay_methods')

class Product(ModelBase):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    
    price = models.IntegerField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
    
class Cart(ModelBase):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts')
    total = models.PositiveIntegerField(default=0)


    def __str__(self):
        date_time = self.date_created.strftime('%H:%M %d/%m')
        return f'{self.client} Cart - {date_time}'
    
    def save(self, *args, **kwargs):
        
        products = self.products.all()
        total = 0
        for product in products:
            total += product.subtotal

        self.total = total
        super().save(*args, **kwargs)

       
class ProductCart(ModelBase):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    ammount = models.PositiveSmallIntegerField(default=1)
    subtotal = models.IntegerField(default=0)


    def __str__(self):
        date_time = self.date_created.strftime('%H:%M %d/%m')
        return f'{self.product} ({self.ammount} u.) ${self.subtotal}'
    
    def save(self, *args, **kwargs):
        if self.ammount != 0:
            self.subtotal = self.product.price * self.ammount
        else:
            self.subtotal = 0
        super().save(*args, **kwargs)

@receiver(post_save, sender=ProductCart)
@receiver(post_delete, sender=ProductCart)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    products = cart.products.all()
    total = 0
    for product in products:
        total += product.subtotal

    cart.total = total
    cart.save()
