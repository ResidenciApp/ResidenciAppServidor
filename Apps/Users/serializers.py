from .models import People, Role, Owner
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


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


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class PeopleSerializers(serializers.ModelSerializer):
    role = RoleSerializers(read_only=True)
    
    owner = OwnerSerializers(read_only=True)

    user = UserSerializers(read_only=True)

    class Meta:
        # Modelo al que hace referencia
        model = People

        # Que campos quiero visualizar
        fields = ('__all__')


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('__all__')