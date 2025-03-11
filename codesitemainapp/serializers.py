#Serializers luokat, joilla kootaan tai puretaan JSON tiedot
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ketju, Aihealue, Vastaus, Notes, CustomUser


# Customoitu käyttäjäserializer joka perustuu CustomUser modelliin models.py
class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','email','username']

#Tunnusten luonti
class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','username','password']
        extra_kwargs = {'password':{'write_only':True}}

        def create(self, valitaded_data):
            user = CustomUser.objects.create_user(**valitaded_data)
            return user


# Foorumi
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

