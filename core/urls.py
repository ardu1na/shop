from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import Login, Logout


from . import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce Shop API",
      default_version='v0.1',
      description="Beta version of endpoints",
      contact=openapi.Contact(email="arduinadelbosque@gmail.com"),
   ),
   public=True,
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
    path('api/', include('ecommerce.urls')),


   path('logout/', Logout.as_view(), name = 'logout'),
   path('login/', Login.as_view(), name = 'login'),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('users/',include('users.routers')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
