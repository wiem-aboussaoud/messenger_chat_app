from .serializers import *
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, View
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import *


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
        current_site = get_current_site(request)
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
                'image': current_site.domain + token.user.image.url if token.user.image else None
            }
        ])



class UserProfileManager(viewsets.ModelViewSet):
    """Handle update and delete profiles"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated, UpdateOwnProfile,)

    def get_queryset(self):
          return UserProfile.objects.filter(username=self.request.user.username)

class FriendsListAPI(APIView):

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    serializer_class = FriendsListSerializer

    def get(self, request):
        friends = UserProfile.objects.filter(is_superuser=False)
        serializer = FriendsListSerializer(friends, many=True, context={"request": self.request})
        return Response(serializer.data)