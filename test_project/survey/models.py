from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='user', verbose_name="Роль")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )


class Survey(models.Model):
    title = models.CharField(verbose_name="Название опроса", max_length=100)
    author = models.ForeignKey(CustomUser, related_name="surveys", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(verbose_name="Вопрос", max_length=250)
    priority = models.IntegerField(default=0)
    survey = models.ForeignKey(Survey, related_name="questions", on_delete=models.CASCADE)


class AnswerQuestion(models.Model):
    title = models.CharField(verbose_name="Ответ", max_length=250)
    priority = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name="answer_questsions", on_delete=models.CASCADE)


class UserSession(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_sessions", on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name="user_sessions", on_delete=models.CASCADE)
    startes_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)


class UserAnswer(models.Model):
    user_session = models.ForeignKey(UserSession, related_name="user_answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="user_answers", on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerQuestion, related_name="user_answers", on_delete=models.CASCADE)