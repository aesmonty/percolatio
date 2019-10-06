# Documentation: https://docs.djangoproject.com/en/2.2/ref/urls/

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ping/', include('conduit.apps.ping.urls', namespace='ping')),
    path('api/', include('conduit.apps.articles.urls', namespace='articles')),
    path('api/', include('conduit.apps.authentication.urls',
                         namespace='authentication')),
    path('api/', include('conduit.apps.profiles.urls', namespace='profiles')),
]
