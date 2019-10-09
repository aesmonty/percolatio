from django.urls import path, include

from .views import ProfileRetrieveAPIView, FollowingAPIView

app_name = 'profiles'

urlpatterns = [
    path('profiles/<username>/', ProfileRetrieveAPIView.as_view()),
    path('profiles/<username>/following/', FollowingAPIView.as_view()),
]
