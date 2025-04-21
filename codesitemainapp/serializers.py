#Serializers luokat, joilla kootaan tai puretaan JSON tiedot
from .models import Ketju, Aihealue, Vastaus, Notes, CustomUser
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# Customoitu käyttäjäserializer joka perustuu CustomUser modelliin models.py
class CustomUserSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields =("id", "email", "id", "is_superuser", "is_staff", "username")
        #fields =("__all__")

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

#Salasanan palautus
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Sähköpostiosoitetta ei löydy.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"uid": "Virheellinen UID."})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError({"token": "Virheellinen tai vanhentunut token."})

        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        return self.user



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
