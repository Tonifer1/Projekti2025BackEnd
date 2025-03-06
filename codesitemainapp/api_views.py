# Api funktiot

# Djangon Kirjastot
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Luokat , Moduulit
from . import serializers
from .models import Aihealue, Ketju, Vastaus, Notes, User
from .serializers import AihealueSerializer, KetjuSerializer, VastausSerializer, NotesSerializer, UserSerializer, SignupSerializer
from .permissions import IsAdminOrSuperuser  # Tuotu erillisestä permissions-tiedostosta

# DRF kirjastot
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

#parantaa yhteensopivuutta kun siirretään moduli alemmaksi
from rest_framework.decorators import api_view, permission_classes

#Autentikaatio token evästeet
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


#kirjautuminen
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')
        return response
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if User.objects.filter(username=request.data.get('username')).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=request.data.get('email')).exists():
        return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    response.set_cookie('access_token', '', httponly=True, secure=True, samesite='Lax')
    response.set_cookie('refresh_token', '', httponly=True, secure=True, samesite='Lax')
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            RefreshToken(refresh_token).blacklist()
    except Exception:
        pass
    return response


# Käyttäjä määritykset
class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Estetään muut kuin adminit ja superuserit muokkaamasta is_superuser-kenttää
        if request.method == 'PATCH' and 'is_superuser' in request.data:
            return request.user.is_superuser
        return True
 
#profiilit käyttäjät
      
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSuperuserOrReadOnly]
    

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Adminit näkevät kaikki käyttäjät
            return User.objects.all()
        # Tavalliset käyttäjät näkevät vain omat tietonsa
        return User.objects.filter(id=user.id)

    def is_superuser(self, request):
        # Tarkistetaan, onko käyttäjä superuser
        return Response({"is_superuser": request.user.is_superuser})
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Foorumi alue
class AihealueViewSet(viewsets.ModelViewSet):
    queryset = Aihealue.objects.all()
    serializer_class = AihealueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrSuperuser]  # Aiheiden luonti vain adminin luvilla

    def perform_create(self, serializer):
        serializer.save()


# Foorumin ketjut jotka lisätään aihealueen alle
class KetjuViewSet(viewsets.ModelViewSet):
    queryset = Ketju.objects.all()
    serializer_class = KetjuSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()



class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(kayttaja=self.request.user)
        return super().perform_create(serializer)

#Notes osio
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user                # Haetaan kirjautunut käyttäjä
        return Notes.objects.filter(user=user)  # Suodatetaan vain käyttäjän omat muistiot

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Tallennetaan muistiot kirjautuneelle käyttäjälle



class NotesByTag(APIView):
    def get(self, request, tag):
        notes = Notes.objects.filter(tags=tag)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)   
