from rest_framework.permissions import BasePermission
from accounts.models import User
from django.shortcuts import get_object_or_404


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(User , pk=request.user.id)
        return user.is_driver and user.is_authenticated