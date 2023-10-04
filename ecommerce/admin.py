from django.contrib import admin

from ecommerce.models import Product, ProductCart, Cart, Client, \
    Category, Subcategory, Order



admin.site.register(Order)
admin.site.register(ProductCart)
admin.site.register(Product)


class SubcategoryInline(admin.StackedInline):
    model = Subcategory
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]
admin.site.register(Category, CategoryAdmin)


admin.site.register(Client)



class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 0
    
class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [ProductCartInline,]
admin.site.register(Cart, CartAdmin)
