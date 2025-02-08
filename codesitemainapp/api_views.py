from django.contrib.auth import authenticate, login, logout
from . import serializers
from .models import Aihealue,Ketju,Vastaus
from .serializers import AihealueSerializer,KetjuSerializer,VastausSerializer
from .serializers import UserSerializer
from .permissions import IsAdminOrSuperuser #tuotu erillisestä permissions tiedostosta

from django.http import JsonResponse

from rest_framework import viewsets, permissions

#Foorumin aihe alueet.
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

    # voidaan rajoittaa spammausta, eli kontrolli jos uutta ketjua yritetään luoda "väärän" aihealueen alle
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