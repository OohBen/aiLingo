from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/languages/", include("languages.urls")),
    path("api/quizzes/", include("quizzes.urls")),
    path("api/lessons/", include("lessons.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/chat/", include("chat.urls")),
    
]
