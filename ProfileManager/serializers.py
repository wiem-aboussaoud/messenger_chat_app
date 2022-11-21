from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from operator import itemgetter
from django.contrib.sites.shortcuts import get_current_site


class CustumAuthTokenSerializer(serializers.Serializer):
    """Class serializer for log in"""

    username = serializers.CharField(label=_("username"))
    password = serializers.CharField(
        label=_("password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        """ Get the username from the email"""
        if username.find('@') != 1:
            val = UserProfile.objects.filter(email=username).values('username')
            if len(val) == 1:
                usernameList = list(map(itemgetter('username'), val))
                username = usernameList[0]

        userList = UserProfile.objects.filter(username=username)
        if (len(userList) == 0):
            msg = _('User does not exist')
            raise serializers.ValidationError(msg)
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            '''update the latest login of the users'''
            UserProfile.objects.filter(email=username).update(last_login= datetime.now())
            if not user:
                raise serializers.ValidationError({'password': [_('Password incorrect')]})
        else:
            msg = _('Username or password incorrect')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs



class UserCreateProfileSerializer(serializers.Serializer):
    """Serializers a user profile object"""

    username = serializers.CharField(label=_("username"))
    email = serializers.EmailField(label=_("email"))
    first_name = serializers.CharField(label=_("first_name"))
    last_name = serializers.CharField(label=_("last_name"))
    password = serializers.CharField(
        label=_("password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, validated_data):
        """Create new user and send the validation email"""
        is_username_exist = UserProfile.objects.filter(username=validated_data['username'])
        is_email_exist = UserProfile.objects.filter(email=validated_data['email'])
        if (len(is_username_exist) != 0):
            raise serializers.ValidationError({'username':
                                            [_("Ce nom d'utilisateur est deja utilisé, essayer avec un autre")]})

        if (len(is_email_exist) != 0):
            raise serializers.ValidationError({'email':
                                                [_("Cet adresse email est deja utilisé, essayer avec une autre")]})


        user = UserProfile.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        print("user created")

        return user


class FriendsListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'image')

    def get_image(self, obj, *args, **kwargs):
        if obj.image:
            current_site = get_current_site(self.context["request"])

            return current_site.domain + obj.image.url
        else:
            return None