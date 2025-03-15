from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from .serializers import AihealueSerializer, KetjuSerializer, VastausSerializer, NotesSerializer, CustomUserSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Aihealue, Ketju, Vastaus, Notes
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser
from .permissions import IsAdminOrSuperuser  # Tuotu erillisestä permissions-tiedostosta
from rest_framework import status, viewsets, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

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
          

# Foorumi alue controllerit
class AihealueViewSet(viewsets.ModelViewSet):
    queryset = Aihealue.objects.all()
    serializer_class = AihealueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrSuperuser]  # Aiheiden luonti vain adminin luvilla

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)    #asettaa kirjautuneen käyttäjän luojaksi 


# Foorumin ketjut jotka lisätään aihealueen alle
class KetjuViewSet(viewsets.ModelViewSet):
    queryset = Ketju.objects.all()
    serializer_class = KetjuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   #asettaa kirjautuneen käyttäjän luojaksi 


#Ketjujen yksittäiset vastaukset (reply)
class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(kayttaja=self.request.user)

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
