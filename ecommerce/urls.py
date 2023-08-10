from django.urls import path

from ecommerce import views

urlpatterns = [
    path('categories/', views.categories),
    path('category/<int:category_id>/', views.category_detail),
    path('products/', views.products),

]
