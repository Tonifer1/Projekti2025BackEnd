from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('',include('codesitemainapp.urls'))   #edelleen ohajus codesitemainapp urls.py:hn.
]
