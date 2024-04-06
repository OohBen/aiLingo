from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language_progress = models.JSONField(default=dict)
    quiz_analytics = models.JSONField(default=dict)
    chat_analytics = models.JSONField(default=dict)

    def update_quiz_analytics(self, language, score, topic_scores):
        if language.name not in self.quiz_analytics:
            self.quiz_analytics[language.name] = {
                'total_quizzes': 0,
                'total_score': 0,
                'topic_scores': {},
            }

        self.quiz_analytics[language.name]['total_quizzes'] += 1
        self.quiz_analytics[language.name]['total_score'] += score

        for topic, score in topic_scores.items():
            if topic not in self.quiz_analytics[language.name]['topic_scores']:
                self.quiz_analytics[language.name]['topic_scores'][topic] = 0
            self.quiz_analytics[language.name]['topic_scores'][topic] += score

        self.calculate_completion_percentage(language.name)
        self.save()

    def update_chat_analytics(self, language, chat_score, topic_scores):
        if language.name not in self.chat_analytics:
            self.chat_analytics[language.name] = {
                'total_chats': 0,
                'total_score': 0,
                'topic_scores': {},
            }

        self.chat_analytics[language.name]['total_chats'] += 1
        self.chat_analytics[language.name]['total_score'] += chat_score

        for topic, score in topic_scores.items():
            if topic not in self.chat_analytics[language.name]['topic_scores']:
                self.chat_analytics[language.name]['topic_scores'][topic] = 0
            self.chat_analytics[language.name]['topic_scores'][topic] += score

        self.calculate_completion_percentage(language.name)
        self.save()

    def calculate_completion_percentage(self, language_name):
        if language_name not in self.language_progress:
            self.language_progress[language_name] = {
                'total_quizzes': 0,
                'total_chats': 0,
                'total_score': 0,
                'completion_percentage': 0,
            }

        self.language_progress[language_name]['total_quizzes'] = self.quiz_analytics.get(language_name, {}).get('total_quizzes', 0)
        self.language_progress[language_name]['total_chats'] = self.chat_analytics.get(language_name, {}).get('total_chats', 0)
        self.language_progress[language_name]['total_score'] = (
            self.quiz_analytics.get(language_name, {}).get('total_score', 0) +
            self.chat_analytics.get(language_name, {}).get('total_score', 0)
        )

        total_activities = self.language_progress[language_name]['total_quizzes'] + self.language_progress[language_name]['total_chats']
        if total_activities > 0:
            self.language_progress[language_name]['completion_percentage'] = (
                self.language_progress[language_name]['total_score'] / total_activities
            )
        else:
            self.language_progress[language_name]['completion_percentage'] = 0