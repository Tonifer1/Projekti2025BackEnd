from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import AihealueViewSet,KetjuViewSet,VastausViewSet,NoteViewSet

# REST API reitit objektien hakuun JSON muodossa, määritetty api_views tiedostossa.
router = DefaultRouter()
router.register(r'Aiheet',AihealueViewSet )
router.register(r'Ketjut',KetjuViewSet )
router.register(r'Vastaukset',VastausViewSet )
router.register(r'Notes',NoteViewSet )

# URLS, suorat reitit
urlpatterns = [
    path('api/', include(router.urls)),
]