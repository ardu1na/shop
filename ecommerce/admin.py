from django.contrib import admin

from ecommerce.models import Product, ProductCart, Cart, Client, Category, Subcategory, Location, PayMethod, Order


admin.site.register(Product)
admin.site.register(Order)

class SubcategoryInline(admin.StackedInline):
    model = Subcategory
    extra = 0
    

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]
admin.site.register(Category, CategoryAdmin)


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0
    

class PayInline(admin.StackedInline):
    model = PayMethod
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    inlines = [LocationInline, PayInline]
admin.site.register(Client, ClientAdmin)



class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 0
    
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [ProductCartInline,]
admin.site.register(Cart, CartAdmin)
