from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return getattr(user, 'role', None) in ('moderator', 'Модератор')