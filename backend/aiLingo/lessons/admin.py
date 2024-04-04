from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'language')
    list_filter = ('language',)
    search_fields = ('title', 'content')