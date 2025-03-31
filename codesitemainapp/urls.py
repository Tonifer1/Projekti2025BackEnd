from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (AihealueViewSet,KetjuViewSet,VastausViewSet,PasswordResetAPIView,CustomPasswordResetCompleteView,
NoteViewSet, NotesByTag, UserInfoView, UserRegistrationView,
LoginView, LogoutView, CookieTokenRefreshView)

from django.contrib.auth import views as auth_views


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

    path('password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
        
]