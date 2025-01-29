from django.db import models
from django.contrib.auth.models import User

#Pohja , lisätään toimintoja tarvittaessa.
#deveploment
# Artikkelit
class Category(models.Model):
    header = models.TextField()


class SubCategory(models.Model):
    header = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories") 


class Article(models.Model):  
    header = models.TextField()
    content = models.TextField()
    additional_content = models.TextField(blank=True, null=True)  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles") 
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="articles")


# Foorumi
class Aihealue(models.Model):  
    header = models.TextField()


class Ketju(models.Model):
    header = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_threads") #jos käyttäjä poistetaan niin ks käyttäjän julkaisut poistuu
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    aihealue = models.ForeignKey(Aihealue, on_delete=models.CASCADE, related_name="threads")  


class Vastaus(models.Model):  
    content = models.TextField()
    replier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_replies") #jos käyttäjä poistetaan niin ks käyttäjän julkaisut poistetaan.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ketju = models.ForeignKey(Ketju, on_delete=models.CASCADE, related_name="replies")  #jos alkuperäinen julkaisu poistetaan sen julkaisun vastaukset poistetaan.