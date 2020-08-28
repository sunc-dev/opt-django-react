# apps/authentication/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fav_color = models.CharField(blank=True, max_length=120)
