from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from .api_views import AihealueViewSet,KetjuViewSet,VastausViewSet,NoteViewSet,UserViewSet,NotesByTag,login_view,logout_view, user_profile_view

#jwt importit start
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#jwt import end

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

    path('api/login/', login_view, name='api_login'),   #muutettu jwt auth
    path('api/logout/', logout_view, name='api_logout'),
    path('api/profile/', api_views.user_profile_view, name='user-profile'),
    path('api/signup/', api_views.signup, name='signedup'),



    #jwt 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #jwt

    #feed
    #path('', views.feed, name='feed'),
]