from .serializers import *
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Message, ChatGroup
from .serializers import InboxSerializer, MessageSerializer
from django.db.models import Q, Max, Subquery, OuterRef
from ProfileManager.models import UserProfile
from ProfileManager.serializers import FriendsListSerializer
from django.core.validators import ValidationError
from datetime import datetime


class InboxManagerView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InboxSerializer

    def get(self, request):
        ## get all messages between connected user and others
        # messages = Message.objects.filter(
        #     Q(sent_to=request.user) | Q(sent_by=request.user),
        # ).order_by("-sent_at")
        last_messages = UserProfile.objects.filter(
            Q(receiver__sent_by=request.user) | Q(sender__sent_to=request.user)).distinct().annotate(
            last_message=Subquery(Message.objects.filter(
                Q(sent_by=OuterRef("pk"), sent_to=request.user) | Q(sent_by=request.user,
                                                                    sent_to=OuterRef("pk"))).order_by(
                "-sent_at").values("id"))).values_list("last_message", flat=True)
        user_groups = request.user.chat_groups.all().values("group")
        chat_group_last_messsage_id = ChatGroup.objects.filter(id__in=user_groups).annotate(
            last_message=Subquery(Message.objects.filter(group=OuterRef('pk')).values("id"))).values_list("last_message", flat=True)
        messages = Message.objects.filter(id__in=list(last_messages) + list(chat_group_last_messsage_id)).order_by("-sent_at")
        return Response(self.serializer_class(messages, many=True, context={"request": self.request}).data)


class InboxMessagesManagerView(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        data = request.query_params.dict()
        user_id = data.get("user_id", None)
        if user_id:
            user_obj = UserProfile.objects.get(id=user_id)
            messages = Message.objects.filter(Q(sent_by=user_id, sent_to=request.user) | Q(
                sent_by=request.user, sent_to=user_id)).order_by("sent_at")
            return Response({
                "user_info": FriendsListSerializer(user_obj, context={"request": self.request}).data,
                "messages": self.serializer_class(messages, many=True, context={"request": self.request}).data
            })


    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(
                         data=self.request.data,
                         context={'request': self.request}
                     )
        if serializer.is_valid():
            serializer.create(self.request.data)
            return Response({"success": True})
        raise ValidationError(serializer.error_messages)

    # def get_queryset(self):
    #     data = self.request.query_params.dict()
    #     user_id = data.get("user_id", None)
    #     print("user id :", user_id)
    #
    #     if user_id:
    #         active_user_id = self.request.user.id
    #         return self.queryset.filter(Q(sent_by=user_id, sent_to=active_user_id) | Q(
    #             sent_by=active_user_id, sent_to=user_id)).order_by("sent_at")
    #     else:
    #         # query = """
    #         #     SELECT * FROM chatmanager_message
    #         #     WHERE id IN
    #         #      (
    #         #          SELECT id FROM chatmanager_message
    #         #          WHERE sent_to_id=29 OR sent_by_id=29 GROUP BY sent_by_id, sent_to_id
    #         #      )
    #         #      ORDER BY sent_at DESC
    #         #
    #         # """
    #         # messages = Message.objects.raw(query)
    #
    #         messages = Message.objects.filter(
    #             Q(sent_to=self.request.user) | Q(sent_by=self.request.user),
    #         ).distinct().order_by("-sent_at")
    #
    #         return (messages)


class MarkSeenMessageManagerView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request):

        # user_id = request.data["user_id"]
        # try:
        #     other_user = UserProfile.objects.get(id=user_id)
        # except:
        #     return Response({"Error": "Unknown user."})
        #
        # messages = Message.objects.filter(
        #     Q(sent_by=request.user, sent_to=other_user) | Q(sent_by=other_user, sent_to=request.user), is_seen=False
        # ).order_by("-sent_at")
        #
        # if messages:
        #     last_message = messages[0]
        #     if last_message.sent_by == other_user:
        #         print("")
        #         other_user_messages = Message.objects.filter(is_seen=False, sent_by=other_user, sent_to=request.user)
        #         if other_user_messages:
        #             other_user_messages.update(is_seen=True, seen_at=datetime.now())

        return Response({"success": True})