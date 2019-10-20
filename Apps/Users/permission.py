from rest_framework import permissions
from django.contrib.auth.models import User

from .models import People

class IsUser(permissions.BasePermission):        

    def has_permission(self, request, view):
        
        if isinstance(request.user, User):
            user = People.objects.select_related("user_ptr").filter(username = request.user.username)
            user = user[0]
            if str(user.role)== 'Usuario':
                return True
            return False
        else:
            return False
