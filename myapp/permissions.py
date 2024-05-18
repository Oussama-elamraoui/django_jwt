# permissions.py

from rest_framework.permissions import BasePermission
from django.utils import timezone

class IsSubscribed(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.subscription_end_date and user.subscription_end_date > timezone.now():
            return True
        return False
