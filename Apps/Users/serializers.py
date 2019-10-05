from .models import Persona, Role, Propietario
from rest_framework import serializers


class PropietarioSerializers(serializers.ModelSerializer):
    class Meta:
        # Modelo al que hace referencia
        model = Propietario

        # Que campos quiero visualizar
        fields = (
            'id', 'documentNumber', 'documentType'
        )


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        # Modelo al que hace referencia
        model = Role

        # Que campos quiero visualizar
        fields = (
            'id', 'name'
        )


class PersonaSerializers(serializers.ModelSerializer):
    role = RoleSerializers(read_only=True)
    owner = PropietarioSerializers(read_only=True)

    class Meta:
        # Modelo al que hace referencia
        model = Persona

        # Que campos quiero visualizar
        fields = ('__all__')