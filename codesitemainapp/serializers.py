#Serializers luokat, joilla kootaan tai puretaan JSON tiedot
from .models import Ketju, Aihealue, Vastaus, Notes, CustomUser

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import authenticate


# Customoitu käyttäjäserializer joka perustuu CustomUser modelliin models.py
class CustomUserSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields =("id", "email", "username")

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")
        extra_kwargs = {"password":{"write_only":True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

#Kirjautuminen
class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")


# Foorumi luokkien serializerit
class AihealueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aihealue
        fields = '__all__'


class KetjuSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    aihealue = serializers.PrimaryKeyRelatedField(queryset=Aihealue.objects.all())
    aihealue_data = AihealueSerializer(source='aihealue', read_only=True)

    class Meta:
        model = Ketju
        fields = '__all__'


class VastausSerializer(serializers.ModelSerializer):
    replier = CustomUserSerializer(read_only=True)
    ketju = serializers.PrimaryKeyRelatedField(queryset=Ketju.objects.all())
    ketju_data = KetjuSerializer(source='ketju', read_only=True)

    class Meta:
        model = Vastaus
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True} #aseta owner
        }

