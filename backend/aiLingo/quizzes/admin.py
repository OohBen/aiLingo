from django.contrib import admin
from .models import Quiz, Question, Attempt

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'duration', 'passing_score')
    list_filter = ('language',)
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('text',)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'date')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username',)