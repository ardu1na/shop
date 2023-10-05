from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ecommerce.resources import ProductResource
from ecommerce.models import Product, ProductCart, Cart, Client, \
    Category, Order

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
admin.site.register(Product, ProductAdmin)



admin.site.register(Order)
admin.site.register(ProductCart)


admin.site.register(Category)


admin.site.register(Client)



class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 0
    
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [ProductCartInline,]
admin.site.register(Cart, CartAdmin)
