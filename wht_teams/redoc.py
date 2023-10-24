from drf_yasg import openapi
from drf_yasg.views import get_schema_view, ReDocRenderer

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