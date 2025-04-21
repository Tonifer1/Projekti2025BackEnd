from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser

from .permissions import IsAdminOrSuperuser  # Tuotu erillisestä permissions-tiedostosta
from .models import Aihealue, Ketju, Vastaus, Notes, CustomUser
from .serializers import AihealueSerializer, KetjuSerializer, VastausSerializer, NotesSerializer, CustomUserSerializer, RegisterUserSerializer, LoginUserSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer

from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator  #lyhyt kestoinen palautukseen tarkoitettu auth token
from django.contrib.auth.views import PasswordResetCompleteView
from django.shortcuts import redirect
from django.contrib import messages

# API Controllerit

class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user

class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "user": CustomUserSerializer(user).data},
                                status=status.HTTP_200_OK)
            
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    @method_decorator(never_cache)
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)

        response.set_cookie(key="access_token", value="", httponly=True, secure=True, samesite="None", max_age=0)
        response.set_cookie(key="refresh_token", value="", httponly=True, secure=True, samesite="None", max_age=0)
        
        #pakotetaan selain poistamaan kaikki
        response["Cache-Control"] = "no-store, no-cache, must-revalitade, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        
        return response     

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response({"error":"Refresh token not provided"}, status= status.HTTP_401_UNAUTHORIZED)
    
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({"message": "Access token token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        except InvalidToken:
            return Response({"error":"Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
#salasanan palautus

class PasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)

            # Tokenin ja UID:n luonti
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Salasanan palautuslinkki
            reset_link = f"https://blue-wave-09f686903.6.azurestaticapps.net/reset-password-form/{uid}/{token}/"

            mail_subject = 'Salasanan palautuspyyntö'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            # Sähköpostin lähetys
            send_mail(mail_subject, message, 'admin@gmail.com', [email])

            return Response({"message": "Salasanan palautuslinkki on lähetetty sähköpostiin."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Salasana vaihdettu onnistuneesti."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Salasanan palautus oli onnistunut. Voit kirjautua sisään uudella salasanallasi.')

          

# Foorumi alue controllerit
class AihealueViewSet(viewsets.ModelViewSet):
    queryset = Aihealue.objects.all()
    serializer_class = AihealueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrSuperuser]  # Aiheiden luonti vain adminin luvilla


# Foorumin ketjut jotka lisätään aihealueen alle
class KetjuViewSet(viewsets.ModelViewSet):
    queryset = Ketju.objects.all().order_by('-created') # Tämä määrittää, mitä tietoja haetaan
    serializer_class = KetjuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
    
    def get_queryset(self):
        queryset = Ketju.objects.all()
        
        # Suodatetaan 'aihealue' parametrin mukaan
        aihealue = self.request.query_params.get('aihealue', None)
        if aihealue:
            queryset = queryset.filter(aihealue=aihealue)
        
        return queryset


#Ketjujen yksittäiset vastaukset (reply)
class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(replier=self.request.user)

#Notes osio
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()  # Oletusarvoinen queryset
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Suodatetaan muistiot käyttäjän mukaan
        return Notes.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

#Muistiinpanot

class NotesByTag(APIView):
    def get(self, request, tag):
        notes = Notes.objects.filter(tags=tag)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)   