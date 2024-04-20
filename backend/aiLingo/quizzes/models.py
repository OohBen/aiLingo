from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from languages.models import Language

from django.db import models
from django.conf import settings


class Quiz(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    passing_score = models.IntegerField()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    choices = models.JSONField()
    answer = models.IntegerField()
    explanations = models.JSONField(null=True, blank=True)
    worth = models.IntegerField(default=1)

    def __str__(self):
        return self.text[:50]


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score}%"
