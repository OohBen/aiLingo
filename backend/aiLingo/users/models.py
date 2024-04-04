from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from languages.models import Language
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    home_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)