from rest_framework import routers
from django.urls import path, include
from .views import SurveyViewSet, QuestionViewSet

router = routers.DefaultRouter()

router.register(r'surveys', SurveyViewSet, basename='surveys')
router.register(r'questions', QuestionViewSet, basename='questions')


urlpatterns = [
    path('api/', include(router.urls)),
]