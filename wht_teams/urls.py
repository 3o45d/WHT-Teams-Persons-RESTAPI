from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view, ReDocRenderer
from drf_yasg import openapi

# Redoc
ReDocRenderer.template = 'wht_teams/redoc/custom_redoc.html'
with open('templates/wht_teams/redoc/description.html') as f:
    description = f.read()

api_info = get_schema_view(
    openapi.Info(
        title="WHT Teams API",
        default_version='v1',
        description=description,
        contact=openapi.Contact(email="31545d@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True
)

# URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('docs/', api_info.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
