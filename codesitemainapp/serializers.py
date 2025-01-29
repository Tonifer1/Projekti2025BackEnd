from rest_framework import serializers
from .models import Category, SubCategory, Article, Ketju, Aihealue, Vastaus
from django.contrib.auth.models import User


# Käyttäjäserializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# Kategoriat
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_data = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'header', 'category', 'category_data']


# Artikkelit
class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    subcategory_data = SubCategorySerializer(source='subcategory', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


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
