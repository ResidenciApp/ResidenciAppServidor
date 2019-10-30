from rest_framework import permissions
from django.contrib.auth.models import User

from .models import People

class IsUser(permissions.BasePermission): 

    # Este metodo permite verificar si un usuario esta autenticado
    # y si lo esta, verifica que tenga el role de 'Usuario'
    def has_permission(self, request, view):
        
        # si 'equest.user' es una instancia de 'User', eso significa
        # que el usuario esta Autenticado
        if isinstance(request.user, User):
            # Traer el usuario desde la Base de Datos
            user = People.objects.select_related("user").filter(user_id=request.user.id)
            user = user[0]
            # Verificar que el usuario tenga el role de 'Usuario'
            if str(user.role)== 'Usuario':
                return True
            return False
        else:
            return False


class IsOwner(permissions.BasePermission):   

    # Este metodo permite verificar si un usuario esta autenticado
    # y si lo esta, verifica que tenga el role de 'Propietario'
    def has_permission(self, request, view):

        # si 'equest.user' es una instancia de 'User', eso significa
        # que el usuario esta Autenticado
        if isinstance(request.user, User):
            # Traer el usuario desde la Base de Datos
            user = People.objects.select_related("user").filter(user_id=request.user.id)
            user = user[0]
            # Verificar que el usuario tenga el role de 'Propietario'
            if str(user.role)== 'Propietario':
                return True
            return False
        else:
            return False


class IsAdministrator(permissions.BasePermission):        

    # Este metodo permite verificar si un usuario esta autenticado
    # y si lo esta, verifica que tenga el role de 'Administrador'
    def has_permission(self, request, view):
        
        # si 'equest.user' es una instancia de 'User', eso significa
        # que el usuario esta Autenticado
        if isinstance(request.user, User):
            # Traer el usuario desde la Base de Datos
            user = People.objects.select_related("user").filter(user_id=request.user.id)
            user = user[0]
            # Verificar que el usuario tenga el role de 'Administrador'
            if str(user.role)== 'Administrador':
                return True
            return False
        else:
            return False


class IsUserOrOwner(permissions.BasePermission):        

    # Este metodo permite verificar si un usuario esta autenticado
    # y si lo esta, verifica que tenga el role de 'Usuario' o 'Propietario'
    def has_permission(self, request, view):
        
        # si 'equest.user' es una instancia de 'User', eso significa
        # que el usuario esta Autenticado
        if isinstance(request.user, User):
            # Traer el usuario desde la Base de Datos
            user = People.objects.select_related("user").filter(user_id=request.user.id)
            user = user[0]
            # Verificar que el usuario tenga el role de 'Usuario' o 'Propietario'
            if str(user.role)== 'Usuario' or str(user.role) == 'Propietario':
                return True
            return False
        else:
            return False
