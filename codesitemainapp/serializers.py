#Serializers luokat, joilla kootaan tai puretaan JSON tiedot



from rest_framework import serializers
from .models import Ketju, Aihealue, Vastaus, Notes
from django.contrib.auth.models import User

# Käyttäjäserializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser']

# Foorumi
class AihealueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aihealue
        fields = '__all__'


class KetjuSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    aihealue = serializers.PrimaryKeyRelatedField(queryset=Aihealue.objects.all())
    aihealue_data = AihealueSerializer(source='aihealue', read_only=True)

    class Meta:
        model = Ketju
        fields = '__all__'


class VastausSerializer(serializers.ModelSerializer):
    replier = UserSerializer(read_only=True)
    ketju = serializers.PrimaryKeyRelatedField(queryset=Ketju.objects.all())
    ketju_data = KetjuSerializer(source='ketju', read_only=True)

    class Meta:
        model = Vastaus
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'header', 'content', 'created', 'updated', 'tags', 'owner']

#Tunnusten luonti
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data.get('first_name', ''),  # Oikea tapa käyttää get()
        last_name=validated_data.get('last_name', '')     # Oikea tapa käyttää get()
    )
        user.set_password(validated_data['password'])
        user.save()
        return user