from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class ModelBase(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="fecha de creación")
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        abstract = True
        
class Category(ModelBase):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, null=True, blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"
        
        
        
class Product(ModelBase):
    name = models.CharField(max_length=200, verbose_name="nombre")
    description = models.CharField(max_length=3000, verbose_name="descripción")
    
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="precio")
    
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name="marca")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="categoría")

    image = models.ImageField(blank=True, null=True, upload_to="products", verbose_name="imagen")
    stock = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    available = models.BooleanField(default=False, verbose_name="disponible")
    
    

    def save(self, *args, **kwargs):
        if self.stock < 1:
            self.available = False
        else:
            self.available = True
        super().save(*args,**kwargs)
    
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Producto"
    

class Client(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', verbose_name="usuario")
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name="nombre")
    lastname = models.CharField(max_length=200, blank=True, null=True, verbose_name="apellido")
    phone = models.CharField(max_length=200, blank=True, null=True, verbose_name="teléfono")
    address = models.CharField(max_length=750, null=True, blank=True, verbose_name="dirección")

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
        
        
    class Meta:
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"
    
        
# Signal function to create a client
@receiver(post_save, sender=User)
def create_client_on_new_user(sender, instance, created, **kwargs):    
    try:
        client = Client.objects.get(user=instance)
    except Client.DoesNotExist:
        client = Client.objects.create(user=instance)
       
    
    
    
    
    
class Cart(ModelBase):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts', verbose_name="cliente")
    total = models.PositiveIntegerField(default=0, null=True, blank=True)
    done = models.BooleanField(default=False, verbose_name="cerrado")
    products_q = models.SmallIntegerField(default=0, null=True, blank=True, verbose_name="cantidad")
    
    def __str__(self):
        date_time = self.date_created.strftime('%H:%M %d/%m')
        return f'{self.client} Cart - {date_time}'
    
    class Meta:
        verbose_name_plural = "Carrito"
        verbose_name = "Carritos"
    
       
class ProductCart(ModelBase):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products', verbose_name="carrito")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', verbose_name="productos")
    ammount = models.PositiveSmallIntegerField(default=1, verbose_name="cantidad")
    subtotal = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return f'{self.product} ({self.ammount} u.) ${self.subtotal}'
        
    def clean(self):
        if self.ammount > self.product.stock:
            raise ValidationError("La cantidad solicitada excede la cantidad disponible.")

    def save(self, *args, **kwargs):
        if self.ammount != 0:
            self.subtotal = self.product.price * self.ammount
        self.clean()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Producto en Carrito"
        verbose_name = "Productos en carrito"
    
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
    cart = models.OneToOneField(Cart, related_name="order", on_delete=models.CASCADE, verbose_name="carrito")
    
    paid = models.BooleanField(default=False, verbose_name="pagado")
    
    sended = models.BooleanField(default=False, verbose_name="enviado")
    
    closed = models.BooleanField(default=False, verbose_name="cerrado")
    
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
    
    
    class Meta:
        verbose_name_plural = "Órdenes de compra"
        verbose_name = "Orden de compra"


@receiver(post_save, sender=Cart)
def create_order_on_cart_done(sender, instance, created, **kwargs):
    if instance.done:
        # Check if an Order already exists for this Cart
        try:
            order = Order.objects.get(cart=instance)
        except Order.DoesNotExist:
            # Create a new Order for the Cart
            order = Order.objects.create(cart=instance)
