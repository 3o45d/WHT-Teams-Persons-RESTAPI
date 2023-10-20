from django.urls import path, include
from rest_framework import routers

from api.views import PersonViewSet, TeamViewSet

router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'teams', TeamViewSet)
# router.register(r'teammembers', TeamMemberViewSet)

urlpatterns = [
    path('', include(router.urls))
]
