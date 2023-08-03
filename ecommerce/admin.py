from django.contrib import admin

from ecommerce.models import Product, ProductCart, Cart, Client, Category, Subcategory, Location, PayMethod


admin.site.register(Product)
admin.site.register(ProductCart)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Location)
admin.site.register(PayMethod)
admin.site.register(Client)