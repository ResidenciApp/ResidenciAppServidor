from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError

from .models import People, Role, Owner
from .serializers import PeopleSerializers, RoleSerializers, OwnerSerializers, TokenSerializers
from .permission import IsUser


class OwnerView(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializers
    permission_classes = (IsUser, IsAuthenticated)


class RoleView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializers


class PeopleView(viewsets.ModelViewSet):
    queryset = People.objects.all().select_related('role')
    serializer_class = PeopleSerializers

    
    def create(self, request):
        # POST: /api/v1/users/people/
        # Recibe los Datos de la persona y guarda el registro en la BD

        print(request.data)

        # Ejemplo: request.data
        # {
        #   'name': 'Luis Miguel', 'lastName': 'Baez Aponte', 'age': 20,
        #   'nickname': 'lmbaeza', 'password': 'admin', 'avatar': 'avatar',
        #   'mail': 'lmbaeza@unal.edu.co', 'token': 'hash', 'role': 1, 'sex': 'M'
        # }

        data = request.data

        
        if data['role'] == 1:
            # Registrar Usuario
            # id_role=1,  ==> Usuario
            

            role = Role.objects.get(id=data['role'])
            
            # Registramos la persona con el role Usuario
            obj = People(
                age=data.get('age'),
                avatar=data.get('avatar'),
                role=role,
                sex=data.get('sex')
            )
            obj.save()

            user = User.objects.filter(id=obj.id)
            user = user[0]

            user.username=data.get('nickname')
            user.is_superuser=False
            user.first_name=data.get('name')
            user.last_name=data.get('lastName')
            user.email=data.get('mail')
            user.is_staff=False
            user.is_active=False

            # Se encripta la contraseña
            user.set_password(data.get('password'))

            # Guardamos los datos en la DB
            user.save()
           
        elif data['role'] == 3:
            # Registar Propietario
            # id_role=3,   ==> Propietario

            # Registramos el Propietario
            owner = Owner(
                documentNumber=data.get('documentNumber'),
                documentType=data.get('documentType')
            )
            owner.save()
            
            role = Role.objects.get(id=data.get('role'))

            # Asociamos el Propietario con la entidad Persona
            obj = People(
                age=data.get('age'),
                avatar=data.get('avatar'),
                role=role,
                owner=owner,
                sex=data.get('sex')
            )
            obj.save()

            user = User.objects.filter(id=obj.id)
            user = user[0]

            user.username=data.get('nickname')
            user.is_superuser=False
            user.first_name=data.get('name')
            user.last_name=data.get('lastName')
            user.email=data.get('mail')
            user.is_staff=False
            user.is_active=False

            # Se encripta la contraseña
            user.set_password(data.get('password'))

            # Guardamos los datos en la DB
            user.save()
        else:
            return Response({'status': 400, 'message': 'BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 201, 'message': 'OK'},status=status.HTTP_201_CREATED)


class TokenView(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializers

    # Pedir un Token
    # POST: api/v1/users/api-token-auth/
    def create(self, request):

        if request.data.get('username') and request.data.get('password'):
            try:
                user = authenticate(
                    username=request.data.get('username'),
                    password=request.data.get('password')
                )

                if user is not None:
                    token = Token.objects.create(user=user)

                    return Response(
                        {'Token': token.key}, 
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {'status': 400, 'message': 'Ya tienes un Token Vigente'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except IntegrityError:
                return Response(
                    {'status': 400,'message': 'Ya tienes un Token Vigente'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'status': 400,'message': 'Falta "username" o "Password"'},
                status=status.HTTP_400_BAD_REQUEST
            )