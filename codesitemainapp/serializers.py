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
    author = UserSerializer(read_only=True)
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
        fields = ['id', 'header', 'content', 'created', 'updated', 'tags']