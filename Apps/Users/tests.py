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
from Apps.Users.serializers import PeopleSerializers
from Apps.Users.models import People
from Apps.Users.models import Role

# Ejecutar 'ALTER USER admin CREATEDB;' en postgres
# o 'ALTER USER postgres CREATEDB;' 

class UserSignUp(APITestCase):
    
    def test_signup(self):
        data = {
            'name': 'testCase name',
            'lastName': 'testCase lastname',
            'age': 10,
            'nickname': 'testCase username',
            'password': 'testCase password',
            'avatar': 'testCase avatar',
            'mail': 'testCase email',
            'token': 'TestCase token',
            'role': 1, # Role 1 ==> Usuario
            'sex': 'O'
        }

        response = self.client.post('/api/v1/users/people/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TokenAuthentication(APITestCase):

    list_url = reverse('people-list')

    def setUp(self):
        self.role = Role.objects.get(id=1)

        # Crear el registro de Usuario
        self.user = User.objects.create_user(
            username='test username',
            is_superuser=False,
            first_name='test first name',
            last_name='test last name',
            email='test@email.com',
            is_staff=False,
            is_active=True
        )
        # Se encripta la contraseña
        self.user.set_password('test password')

        # Guardar Registro User
        self.user.save()

        self.people = People(
            age=1,
            avatar='test avatar',
            role=self.role,
            sex='O',
            user=self.user
        )

        # Guardar la Persona
        self.people.save()

        self.token = Token.objects.create(user=self.user)

        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ str(self.token))


    def test_token_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

