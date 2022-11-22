from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', UserProfileManager, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateProfile.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('friends/', FriendsListAPI.as_view()),

]
