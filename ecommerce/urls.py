from django.urls import path

from ecommerce import views

urlpatterns = [
    # display 
    path('categories/', views.categories),
    path('category/<int:category_id>/', views.category_detail),
    path('products/', views.products),
    # shop
    path('cart/add/<int:product_id>/', views.add_product_into_cart),

]
