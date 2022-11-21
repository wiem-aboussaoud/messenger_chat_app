from .serializers import *
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserCreateProfile(APIView):
    """Handle create new profile"""

    serializer_class = UserCreateProfileSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"success": True})


class UserLoginApiView(ObtainAuthToken):

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustumAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response([
            {
                'token': token.key
            },
            {
                'id': token.user.id,
                'username': token.user.username,
                'email': token.user.email,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'is_superuser': token.user.is_superuser
            }
        ])


class FriendsListAPI(APIView):

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    serializer_class = FriendsListSerializer

    def get(self, request):
        friends = UserProfile.objects.filter(is_superuser=False)
        serializer = FriendsListSerializer(friends, many=True, context={"request": self.request})
        return Response(serializer.data)