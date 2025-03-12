from django.contrib import admin
from .models import Aihealue,Ketju,Vastaus,Notes,Tags, CustomUser, CustomUserManager

admin.site.register(CustomUser)
admin.site.register(Aihealue)
admin.site.register(Ketju)
admin.site.register(Vastaus)
admin.site.register(Notes)