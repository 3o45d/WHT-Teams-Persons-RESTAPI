from django.contrib import admin
from django.urls import path, include

from .redoc import api_info

# URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('docs/', api_info.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
