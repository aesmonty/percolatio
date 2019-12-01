# Documentation: https://docs.djangoproject.com/en/2.2/ref/urls/

from django.urls import path, include
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Percolatio LTD",
        default_version='v1',
        description="Percolation Private API",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT Licence"),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('conduit.apps.ping.urls', namespace='ping')),
    path('admin/', admin.site.urls),

    path('api/', include('conduit.apps.articles.urls', namespace='articles')),
    path('api/', include('conduit.apps.authentication.urls',
                         namespace='authentication')),
    path('api/', include('conduit.apps.foundations.urls', namespace='foundations')),
    path('api/', include('conduit.apps.grants.urls', namespace='grants')),
    path('api/', include('conduit.apps.profiles.urls', namespace='profiles')),

    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui')
]
