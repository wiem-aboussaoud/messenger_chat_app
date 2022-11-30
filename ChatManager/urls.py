
from django.urls import path, include

from .views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

app_name = "ClientManager"

# router.register('inbox', InboxManagerView, basename='inbox')
router.register('inbox/messages', InboxMessagesManagerView, basename='messages')

urlpatterns = [

    path('', include(router.urls)),
    path('inbox/', InboxManagerView.as_view()),
    path('message/mark_seen/', MarkSeenMessageManagerView.as_view()),

]



