from django.contrib import admin
from django.urls import path
from ecommerce.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),


]
