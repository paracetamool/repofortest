# views.py
from rest_framework import viewsets, permissions
from django.db.models import Count, Prefetch
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Survey, Question, AnswerQuestion, UserAnswer, UserSession
from django.shortcuts import get_object_or_404
from .serializers import SurveyListSerializer, SurveyDetailSerializer, QuestionDetailSerializer

class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.action == 'list':
            return Survey.objects.annotate(
                question_count=Count("questions")
            ).select_related("author").order_by("-created_at")
        else:
            return Survey.objects.prefetch_related(
                'questions__answer_questsions'
            ).select_related("author")

    def get_serializer_class(self):
        if self.action == 'list':
            return SurveyListSerializer
        return SurveyDetailSerializer



class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionDetailSerializer

    def get_queryset(self):
        q = Question.objects.prefetch_related(
            Prefetch(
                'answer_questsions',
                queryset=AnswerQuestion.objects.order_by('-title')
            )
        ).all()
        return q
    

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        question = self.get_object()
        user = request.user
        
        answer_id = request.data.get('answer_id')
        if not answer_id:
            return Response(
                {"error": "answer_id обязателен"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        answer = get_object_or_404(AnswerQuestion, id=answer_id, question=question)
        
        survey = question.survey
        user_session, created = UserSession.objects.get_or_create(
            user=user,
            survey=survey,
            defaults={'is_finished': False}
        )
        
        user_answer, created = UserAnswer.objects.get_or_create(
            user_session=user_session,
            question=question,
            defaults={'answer': answer}
        )
        
        if not created:
            # Если ответ уже был, обновляем его
            user_answer.answer = answer
            user_answer.save()
        
        return Response({
            "message": "Ответ сохранен",
            "question_id": question.id,
            "answer_id": answer.id,
            "answer_text": answer.title,
            "session_id": user_session.id
        })