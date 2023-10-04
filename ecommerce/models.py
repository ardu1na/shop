from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import CustomUser
class ModelBase(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        abstract = True
        
class Category(ModelBase):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, null=True, blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    
class Subcategory(ModelBase):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    def __str__(self):
            return self.name     
    
    class Meta:
        verbose_name_plural = "Subcategories"


class Product(ModelBase):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    
    price = models.IntegerField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    image = models.ImageField(blank=True, null=True, upload_to="media")

    available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class ProductImage(ModelBase):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, null=True, upload_to="products")
    alt = models.CharField(max_length=50, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.alt is None:
            self.alt = f'product {self.product.name}'
        super().save(*args,**kwargs)
    
    
    def __str__ (self):
        
        return self.alt

## TODO: clean phone number    
class Client(ModelBase):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    name = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.name and self.lastname:
            return f'{self.name} {self.lastname}'
        elif self.name:
            return f'{self.name}'
        
        elif self.lastname:
            return f'{self.lastname}'
        else:
            return self.user.username
        
    @property
    def email(self):
        return self.user.email
        
        
        
        
# Signal function to create a client
@receiver(post_save, sender=CustomUser)
def create_client_on_new_user(sender, instance, created, **kwargs):    
    try:
        client = Client.objects.get(user=instance)
    except Client.DoesNotExist:
        client = Client.objects.create(user=instance)
       
class Location(ModelBase):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')
    
    address = models.CharField(max_length=450, null=True, blank=True)
    address_number = models.PositiveSmallIntegerField(null=True, blank=True)
    apartament =  models.CharField(null=True, blank=True, max_length=500)
    country = models.CharField(null=True, blank=True, max_length=200)
    state = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(null=True, blank=True, max_length=200)
    post_code = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank= True)
    is_home = models.BooleanField(default=False)
    
    def __str__ (self):
        return f'{self.client} address'
    
    
    
    
    
class PayMethod(ModelBase):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pay_methods')

    def __str__(self):
        return f'{self.client} paymethod'
    
    
    
    
    
    
class Cart(ModelBase):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts')
    total = models.PositiveIntegerField(default=0)
    done = models.BooleanField(default=False)
    products_q = models.SmallIntegerField(default=0)
    
    def __str__(self):
        date_time = self.date_created.strftime('%H:%M %d/%m')
        return f'{self.client} Cart - {date_time}'
    
   
       
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
def update_cart(sender, instance, **kwargs):
    cart = instance.cart
    products = cart.products.all()
    total = 0
    q = 0
    for product in products:
        total += product.subtotal
        q += product.ammount
    cart.total = total
    cart.products_q = q    
    cart.save()




 
class Order(ModelBase):   
    cart = models.OneToOneField(Cart, related_name="order", on_delete=models.CASCADE)
    
    paid = models.BooleanField(default=False)
    paymethod = models.ForeignKey(PayMethod, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    
    shipping_address = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    sended = models.BooleanField(default=False)
    
    closed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.paid == True and self.sended == True:
            self.closed == True
        super().save(*args, **kwargs)

    
    def __str__(self):
        if self.closed == True:
            done = "Done"
        else:
            done = "Not Closed"
        return f'{self.cart.client} Cart - {done}'
    
    
    @property
    def products(self):
        
        return [cart_product.product for cart_product in self.cart.products.select_related('product').all()]

    
    
    @property
    def total(self):
        
        return self.cart.total


@receiver(post_save, sender=Cart)
def create_order_on_cart_done(sender, instance, created, **kwargs):
    if instance.done:
        # Check if an Order already exists for this Cart
        try:
            order = Order.objects.get(cart=instance)
        except Order.DoesNotExist:
            # Create a new Order for the Cart
            order = Order.objects.create(cart=instance)
