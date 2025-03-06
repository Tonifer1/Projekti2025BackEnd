from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None
        
        try:
            validated_token = self.get_validated_token(access_token)
        except AuthenticationFailed as e:
            print(f"JWT Authentication failed: {e}")  # Debuggausta varten, poista tuotannossa
            return None
        
        return self.get_user(validated_token), validated_token

