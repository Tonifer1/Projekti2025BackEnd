from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (AihealueViewSet,KetjuViewSet,VastausViewSet,
NoteViewSet, NotesByTag, UserInfoView, UserRegistrationView,
LoginView, LogoutView, CookieTokenRefreshView)

#jwt import end

# REST API reitit objektien hakuun JSON muodossa, määritetty api_views tiedostossa.
router = DefaultRouter()
router.register(r'Aiheet',AihealueViewSet )
router.register(r'Ketjut',KetjuViewSet )
router.register(r'Vastaukset',VastausViewSet )
router.register(r'Notes',NoteViewSet )

# URLS, suorat reitit
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='user-login'),   #muutettu jwt auth
    path('api/logout/', LogoutView.as_view(), name='user-logout'),
    path('api/profile/', UserInfoView.as_view(), name='user-info'),
    path('api/signup/', UserRegistrationView.as_view(), name='register-user'),
    path('api/refresh/', CookieTokenRefreshView.as_view(), name='token-refresh'),

]