from rest_framework import generics, viewsets
from .models import Persona, Role, Propietario
from .serializers import PersonaSerializers, RoleSerializers, PropietarioSerializers


class PropietarioView(viewsets.ModelViewSet):
    queryset = Propietario.objects.all()
    serializer_class = PropietarioSerializers


class RoleView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializers


class PersonaView(viewsets.ModelViewSet):
    queryset = Persona.objects.all().select_related('role')
    serializer_class = PersonaSerializers
