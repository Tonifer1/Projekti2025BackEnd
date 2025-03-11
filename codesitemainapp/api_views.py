# Api funktiot
# Djangon Kirjastot
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Luokat , Moduulit
from .models import Aihealue, Ketju, Vastaus, Notes
from .serializers import AihealueSerializer, KetjuSerializer, VastausSerializer, NotesSerializer, CustomUserSerializer, RegisterUserSerializer
from .permissions import IsAdminOrSuperuser  # Tuotu erillisestä permissions-tiedostosta

# DRF kirjastot
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

class UserInfoView (RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = ()

    def get_object(self):
        return self.request.user

class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save()



class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(kayttaja=self.request.user)
        return super().perform_create(serializer)

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

class NotesByTag(APIView):
    def get(self, request, tag):
        notes = Notes.objects.filter(tags=tag)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)   
