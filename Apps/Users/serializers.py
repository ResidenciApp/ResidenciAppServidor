from .models import People, Role, Owner
from rest_framework import serializers


class OwnerSerializers(serializers.ModelSerializer):
    class Meta:
        # Modelo al que hace referencia
        model = Owner

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


class PeopleSerializers(serializers.ModelSerializer):
    role = RoleSerializers(read_only=True)
    
    owner = OwnerSerializers(read_only=True)

    class Meta:
        # Modelo al que hace referencia
        model = People

        # Que campos quiero visualizar
        fields = ('__all__')