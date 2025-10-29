from django.db.models import Count
from .models import Survey, Question, UserSession, UserAnswer, CustomUser


class SurveyStatisticsService:

    @staticmethod
    def get_summary():
        return {
            "total_surveys": Survey.objects.count(),
            "total_questions": Question.objects.count(),
            "total_users": CustomUser.objects.count(),
            "total_sessions": UserSession.objects.count(),
            "finished_sessions": UserSession.objects.filter(is_finished=True).count(),
        }

    @staticmethod
    def get_survey_stats(survey_id: int):
        survey = Survey.objects.get(id=survey_id)
        total_sessions = survey.user_sessions.count()
        finished = survey.user_sessions.filter(is_finished=True).count()
        answers = (
            UserAnswer.objects.filter(question__survey=survey)
            .values('answer__title')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return {
            "survey_title": survey.title,
            "total_sessions": total_sessions,
            "finished_sessions": finished,
            "completion_rate": finished / total_sessions * 100 if total_sessions else 0,
            "popular_answers": list(answers[:5]),
        }
