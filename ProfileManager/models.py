from django.db import models
from django.contrib.auth.models import AbstractBaseUser #include the user profile model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from datetime import datetime
import os
import uuid
from django.utils import timezone


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username, email, first_name, last_name, password=None): #when we dont specify a password it be none
        """Create a new user profile"""

        if not email or not username:
            raise ValueError('username and email are required') #Error message
        email = self.normalize_email(email) #normalise the email (convert it to lower case)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.last_login = datetime.now()
        #user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """Create and save a new superuser with given details"""

        user = self.create_user(username, email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


def imageFilePath(instance, filename):
    """Generate file path for new mage/file"""

    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/image/', filename)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Data base for users in the system Custom User model"""

    username = models.CharField(max_length=255, unique=True) #username must be unique
    image = models.ImageField(null=True, blank=True, upload_to=imageFilePath)
    email = models.EmailField(max_length=255, unique=True) #email must be unique
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now_add=True) #current date_time
    is_active = models.BooleanField(default=False) #User permission profile activate or not
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        """Return the string representation of our user"""
        return self.username

