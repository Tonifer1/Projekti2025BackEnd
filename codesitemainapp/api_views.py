#Api funktiot

#Djangon Kirjastot
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

#luokat , Moduulit
from . import serializers
from .models import Aihealue,Ketju,Vastaus,User
from .serializers import AihealueSerializer,KetjuSerializer,VastausSerializer
from .serializers import UserSerializer
from .permissions import IsAdminOrSuperuser #tuotu erillisestä permissions tiedostosta

#DRF kirjastot
from rest_framework import viewsets, permissions
from rest_framework.response import Response

#Funktiot


#Käyttäjä määritykset
class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Estetään muut kuin adminit ja superuserit muokkaamasta is_superuser kenttää
        if request.method == 'PATCH':
            if 'is_superuser' in request.data:
                if not request.user.is_superuser:
                    return False
        return True

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
        is_superuser = request.user.is_superuser
        return Response({"is_superuser": is_superuser})



#Foorumi alue.
class AihealueViewSet(viewsets.ModelViewSet):
    queryset = Aihealue.objects.all()
    serializer_class = AihealueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrSuperuser] # aiheiden luonti vain adminin luvilla

    def perform_create(self, serializer):
        serializer.save()

# foorumin ketjut jotka lisätään aihealueen alle
class KetjuViewSet(viewsets.ModelViewSet):
    queryset = Ketju.objects.all()
    serializer_class = KetjuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # voidaan rajoittaa spammausta, eli kontrolli kirosanoille yms, kokeellinen, toisaalta suodatus toimii paremmin frontin puolella.
    # sanoja voidaan lisätä, poistaa tarpeen mukaan.
    FORBIDDEN_WORDS = ["spam", "väärä aihe", "kielletty sana"]

    def perform_create(self, serializer):
        nimi = serializer.validated_data.get("nimi", "").lower()
        sisalto = serializer.validated_data.get("sisalto", "").lower()
        if any(word in nimi for word in self.FORBIDDEN_WORDS) or any(word in sisalto for word in self.FORBIDDEN_WORDS):
            raise serializers.ValidationError("Ketjun nimi tai sisältö sisältää aiheeseen sopimattomia sanoja.")
        serializer.save()

class VastausViewSet(viewsets.ModelViewSet):
    queryset = Vastaus.objects.all()
    serializer_class = VastausSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return super().perform_create(serializer)