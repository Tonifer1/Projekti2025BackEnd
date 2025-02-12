from django.contrib import admin
from .models import Aihealue,Ketju,Vastaus,Notes,Tags

admin.site.register(Aihealue)
admin.site.register(Ketju)
admin.site.register(Vastaus)
admin.site.register(Notes)
admin.site.register(Tags)