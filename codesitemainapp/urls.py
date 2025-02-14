from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import AihealueViewSet,KetjuViewSet,VastausViewSet,NoteViewSet,UserViewSet

# REST API reitit objektien hakuun JSON muodossa, määritetty api_views tiedostossa.
router = DefaultRouter()
router.register(r'Aiheet',AihealueViewSet )
router.register(r'Ketjut',KetjuViewSet )
router.register(r'Vastaukset',VastausViewSet )
router.register(r'Notes',NoteViewSet )
router.register(r'Users', UserViewSet)

# URLS, suorat reitit
urlpatterns = [
    path('api/', include(router.urls)),
]