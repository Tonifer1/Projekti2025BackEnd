from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import 

router = DefaultRouter()
router.register(r'-', )
router.register(r'-', )
router.register(r'-', )
router.register(r'-', )

urlpatterns = [
    path('api/', include(router.urls)),
]