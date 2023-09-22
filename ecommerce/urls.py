from django.urls import path, include
from rest_framework import routers

from ecommerce import views
from ecommerce.viewsets import ProductViewSet, CategoryViewSet, CartViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'carts', CartViewSet)

urlpatterns = [
  
   
    path('users/profile/', views.client_profile),
    path('users/profile/update/', views.update_client_profile),
    path('users/profile/location/', views.add_client_location),

    path('ecommerce/', include(router.urls)),

]
