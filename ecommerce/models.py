from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

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
    
    brand = models.CharField(max_length=200, null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    image = models.ImageField(blank=True, null=True, upload_to="products")

    stock = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=False)
    
    

    def save(self, *args, **kwargs):
        if self.stock < 1:
            self.available = False
        super().save(*args,**kwargs)
    
        
    def __str__(self):
        return self.name
    
    

class Client(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    name = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=750, null=True, blank=True)

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
@receiver(post_save, sender=User)
def create_client_on_new_user(sender, instance, created, **kwargs):    
    try:
        client = Client.objects.get(user=instance)
    except Client.DoesNotExist:
        client = Client.objects.create(user=instance)
       
    
    
    
    
    
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
        
    def clean(self):
        if self.ammount > self.product.stock:
            raise ValidationError("La cantidad solicitada excede la cantidad disponible.")

    def save(self, *args, **kwargs):
        if self.ammount != 0:
            self.subtotal = self.product.price * self.ammount
        self.clean()
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
    
    sended = models.BooleanField(default=False)
    
    closed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.paid and self.sended and not self.closed:
            self.closed = True
            self.decrease_product_stock()
        super().save(*args, **kwargs)

    @property
    def client_address(self):
        return self.cart.client.address

    def decrease_product_stock(self):
        products_in_order = self.cart.products.all()
        for product_in_order in products_in_order:
            product = product_in_order.product
            product.stock -= product_in_order.ammount
            product.save()
    
    def __str__(self):
        if self.closed == True:
            done = "Done"
        else:
            done = "Not Closed"
        return f'{self.cart.client} Cart - {done}'
    
    
    @property
    def products(self):
        
        cart_products = self.cart.products.all()
        products = []
        for product in cart_products:
            products.append(product.product)
        return products
    
    
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
