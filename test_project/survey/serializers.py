# serializers.py
from rest_framework import serializers
from .models import Survey, Question, AnswerQuestion


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerQuestion
        fields = ['id', 'title', 'priority']


class QuestionDetailSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, read_only=True, source='answer_questsions')  # обратите внимание на source!
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'priority', 'answer_options']


class SurveyListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'author_name', 'created_at', 'question_count']


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    total_questions = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Survey
        fields = [
            'id', 
            'title', 
            'author_name', 
            'created_at', 
            'questions',
            'total_questions'
        ]