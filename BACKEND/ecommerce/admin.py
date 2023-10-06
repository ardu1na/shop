from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ecommerce.resources import ProductResource
from ecommerce.models import Product, ProductCart, Cart, Client, \
    Category, Order


admin.site.site_header = 'E&J'
admin.site.index_title = 'E&J Administración'
admin.site.site_title = 'E&J'



class ProductInline(admin.StackedInline):
    model = Product
    extra = 0

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource

admin.site.register(Product, ProductAdmin)



admin.site.register(Order)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ProductInline,]

admin.site.register(Category, CategoryAdmin)


admin.site.register(Client)



class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 0
    
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [ProductCartInline,]
admin.site.register(Cart, CartAdmin)
