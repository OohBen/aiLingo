from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Analytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
