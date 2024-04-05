from rest_framework import generics
from .models import Lesson, UserLesson
from .serializers import LessonSerializer, UserLessonSerializer

# class LessonListCreateView(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer

# class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer


class UserLessonListCreateView(generics.ListCreateAPIView):
    serializer_class = UserLessonSerializer

    def get_queryset(self):
        return UserLesson.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserLessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLesson.objects.all()
    serializer_class = UserLessonSerializer
