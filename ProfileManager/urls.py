from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateProfile.as_view()),
    path('login/', UserLoginApiView.as_view()),

]
