from django.urls import re_path

from users import views
from users.views import LogoutView

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('logout', LogoutView.as_view(), name="logout"),
    re_path('test_token', views.test_token),

]
