from django.contrib import admin
from .models import (
    CustomUser,
    Survey,
    Question,
    AnswerQuestion,
    UserSession,
    UserAnswer,
)
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("role",)}),
    )


class AnswerQuestionInline(admin.TabularInline):
    model = AnswerQuestion
    extra = 1
    ordering = ["priority"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "survey", "priority")
    list_filter = ("survey",)
    search_fields = ("title",)
    ordering = ["survey", "priority"]
    inlines = [AnswerQuestionInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    ordering = ["priority"]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("title",)
    ordering = ["-created_at"]
    inlines = [QuestionInline]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "survey", "startes_at", "is_finished")
    list_filter = ("is_finished", "survey")
    search_fields = ("user__username", "survey__title")
    ordering = ["-startes_at"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("user_session", "question", "answer")
    list_filter = ("question__survey",)
    search_fields = ("user_session__user__username", "question__title", "answer__title")
    ordering = ["user_session"]
