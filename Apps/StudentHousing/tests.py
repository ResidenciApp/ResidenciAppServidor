from django.test import TestCase

# Create your tests here.
from django.test import TestCase
import json

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Django Rest Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

# Local
from Apps.StudentHousing.models import ResidencePublication
from Apps.Users.models import People, Role, Owner
from Apps.Users.serializers import PeopleSerializers
from Apps.Users.models import *
from _markupbase import *
from .models import *

class PruebaSH(APITestCase):

    def test_prueba1(self):
        owner = Owner(
            documentNumber=1,
            documentType='CC'
        )
        owner.save()

        # Buscar el Objeto del 'Role' que va a tener el nuevo propietario
        role = Role.objects.get(id=3)
        # Crear el registro del Usuario Asociado al Propietario
        user = User.objects.create_user(
            username='gdgarcian',
            is_superuser=False,
            first_name='German',
            last_name='Garcia',
            email='abc@abc.com',
            is_staff=False,
            is_active=True
        )
        # Se encripta la contraseña
        user.set_password('password')

        # Guardar Registro User
        user.save()

        # Crear registro de Persona asociado al Propietario y Usuario
        obj = People(
            age=1,
            avatar='some',
            role=role,
            owner=owner,
            sex='M',
            user=user
        )

        # Guardar registro de la nueva persona
        obj.save()

        data = {
          "owner":"gdgarcian",
          "name": "Zuleta",
          "price": 231,
          "address": "hola direccion",
          "locality": 45,
          "services": [],
          "description": "holamIundo",
          "city": 1,
          "rules": "regla",
          "photo": "fotico xd"
        }

        response = self.client.post('/api/v1/student_housing/residence_publication/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class NotificationTesting(APITestCase):

    def test_notif(self):
        data = {
            "description" : "Nueva Notificacion",
            "publication" : 1,
            "people" : 1
        }

        owner = Owner(
            documentNumber=123456,
            documentType='CC'
        )
        owner.save()

        role = Role.objects.get(id=3)

        # Crear el registro de Usuario
        user = User.objects.create_user(
            username='test username',
            is_superuser=False,
            first_name='test first name',
            last_name='test last name',
            email='test@email.com',
            is_staff=False,
            is_active=True
        )
        # Se encripta la contraseña
        user.set_password('test password')

        # Guardar Registro User
        user.save()

        people = People(
            age=1,
            avatar='test avatar',
            role=role,
            sex='O',
            user=user,
            owner=owner
        )


        # Guardar la Persona
        people.save()

        location = Location(
            city='Bogotá D.C.',
            neighborhood='',
            locality='Teusaquillo',
            address='Calle 39 N° 45 - 85'
        )

        location.save()

        # Registrar residencia
        residence = ResidencePublication(
            name='name',
            photo='url',
            price=1234,
            rules='rules ...',
            owner=owner,
            description='description ...',
            location=location
        )
        # Guardar el registro
        residence.save()

        response = self.client.post('/api/v1/student_housing/notification/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)





