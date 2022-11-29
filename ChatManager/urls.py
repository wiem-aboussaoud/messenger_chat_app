
from django.urls import path, include

from .views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

app_name = "ClientManager"

router.register('inbox', InboxManagerView, basename='inbox')

urlpatterns = [

    path('', include(router.urls)),
    path('message/mark_seen/', MarkSeenMessageManagerView.as_view()),

]



