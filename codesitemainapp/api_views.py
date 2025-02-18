# Api funktiot

# Djangon Kirjastot
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Luokat , Moduulit
from . import serializers
from .models import Aihealue, Ketju, Vastaus, Notes, User
from .serializers import AihealueSerializer, KetjuSerializer, VastausSerializer, NotesSerializer, UserSerializer
from .permissions import IsAdminOrSuperuser  # Tuotu erillisestä permissions-tiedostosta

# DRF kirjastot
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

# Käyttäjä määritykset
class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Estetään muut kuin adminit ja superuserit muokkaamasta is_superuser-kenttää
        if request.method == 'PATCH' and 'is_superuser' in request.data:
            return request.user.is_superuser
        return True
    
class NotesByTag(APIView):
    def get(self, request, tag):
        notes = Notes.objects.filter(tags=tag)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSuperuserOrReadOnly]
    
    '''
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
        '''


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
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        serializer.save()


class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(kayttaja=self.request.user)
        return super().perform_create(serializer)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [permissions.AllowAny]
