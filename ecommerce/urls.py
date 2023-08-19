from django.urls import path

from ecommerce import views

urlpatterns = [
    # display 
    path('categories/', views.categories),
    path('category/<int:category_id>/', views.category_detail),
    path('products/', views.products),
    path('product/<int:product_id>/', views.product_detail),

    # shop
    path('cart/add/<int:product_id>/', views.add_product_into_cart),
    path('cart/delete/<int:product_id>/', views.delete_product_from_cart),
    path('cart/', views.cart_detail),
    
    # client
    path('profile/', views.client_profile),
    path('profile/update/', views.update_client_profile),
    path('profile/location/', views.add_client_location),


]
