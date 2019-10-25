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
        #   'mail': 'lmbaeza@unal.edu.co', 'token': 'hash', 'role': 1, 'sex': 'M',
        #   'documentNumber': 1032452654, 'documentType': 'CC'
        # }

        data = request.data

        userCount = User.objects.filter(username=data.get('nickname')).count()

        # Verificar que el 'username' no este registrado en la base de datos
        # Si 'userCount' tiene algun registro significa que el 'username' ya existe


        if userCount != 0:
            print("True")
            return Response({'status': 400, 'message': 'USERNAME_ALREADY_EXISTS'})
        
        
        if data.get('role') == 1:
            # Registrar Usuario
            # id_role=1,  ==> Usuario

            role = Role.objects.get(id=data.get('role'))

            user = User(
                username=data.get('nickname'),
                is_superuser=False,
                first_name=data.get('name'),
                last_name=data.get('lastName'),
                email=data.get('mail'),
                is_staff=False,
                is_active=False
            )
            # Se encripta la contraseña
            user.set_password(data.get('password'))

            user.save()

            obj = People(
                age=data.get('age'),
                avatar=data.get('avatar'),
                role=role,
                sex=data.get('sex'),
                user=user
            )

            obj.save()
           
        elif data.get('role') == 3:
            # Registar Propietario
            # id_role=3,   ==> Propietario

            # Crear el registro del Propietario en la BD
            owner = Owner(
                documentNumber=data.get('documentNumber'),
                documentType=data.get('documentType')
            )
            owner.save()
            
            # Buscar el Objeto del 'Role' que va a tener el nuevo propietario
            role = Role.objects.get(id=data.get('role'))

            # Crear el registro del Usuario Asociado al Propietario
            user = User(
                username=data.get('nickname'),
                is_superuser=False,
                first_name=data.get('name'),
                last_name=data.get('lastName'),
                email=data.get('mail'),
                is_staff=False,
                is_active=False
            )

            # Se encripta la contraseña
            user.set_password(data.get('password'))

            # Guardar Registro User
            user.save()
            
            # Crear registro de Persona asociado al Propietario y Usuario
            obj = People(
                age=data.get('age'),
                avatar=data.get('avatar'),
                role=role,
                owner=owner,
                sex=data.get('sex'),
                user=user
            )

            # Guardar registro de la nueva persona
            obj.save()
        else:
            # Cuando el role no coincide ni con Usuario ni Propietarios
            return Response({'status': 400, 'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

        # Enviamos una respuesta satisfactoria cuando el registro fué creado
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