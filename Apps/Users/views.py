# Django Rest Framework
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Django
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Local Files
from .models import People, Role, Owner
from .serializers import PeopleSerializers, RoleSerializers, OwnerSerializers
from .serializers import TokenSerializers, UserSerializers
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

    # POST: /api/v1/users/people/
    def create(self, request):
        # Este Metodo recibe los Datos de la persona y guarda el registro en la BD

        # Debug
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
            return Response({'status': 400, 'message': 'USERNAME_ALREADY_EXISTS'})
        

        if data.get('role') == 1:
            # Registrar Usuario
            # id_role=1,  ==> Usuario

            role = Role.objects.get(id=data.get('role'))

            # Crear el registro de Usuario
            user = User.objects.create_user(
                username=data.get('nickname'),
                is_superuser=False,
                first_name=data.get('name'),
                last_name=data.get('lastName'),
                email=data.get('mail'),
                is_staff=False,
                is_active=True
            )
            # Se encripta la contraseña
            user.set_password(data.get('password'))

            # Guardar Registro User
            user.save()

            obj = People(
                age=data.get('age'),
                avatar=data.get('avatar'),
                role=role,
                sex=data.get('sex'),
                user=user
            )

            # Guardar la Persona
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
            user = User.objects.create_user(
                username=data.get('nickname'),
                is_superuser=False,
                first_name=data.get('name'),
                last_name=data.get('lastName'),
                email=data.get('mail'),
                is_staff=False,
                is_active=True
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


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class TokenView(viewsets.ViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializers

    # Pedir un Token con un Usuario
    # POST: api/v1/users/api-token-auth/
    def create(self, request):

        # Verificar que el usuario haya enviado el 'username' y 'password'
        if request.data.get('username') and request.data.get('password'):
            try:
                # Se realiza el proceso de Autenticación
                # En caso de que el usuario y contraseña sean correctos
                # Retorna una instancia de 'User' con los datos del usuario
                # En caso contrario retorna None
                user = authenticate(
                    username=request.data.get('username'),
                    password=request.data.get('password')
                )

                # Validación

                if user is not None:
                    # Se crea el token del usuario 'user'
                    token = Token.objects.create(user=user)

                    # Envia el Token al Cliente
                    return Response(
                        {'status': 200, 'message': 'OK' ,'Token': token.key}, 
                        status=status.HTTP_200_OK
                    )
                else:
                    # si el metodo authenticate(...) retorna None
                    # Significa quela contraseña o el nombre de usuario
                    # Estan incorrectos
                    return Response(
                        {'status': 400, 'message': 'INCORRECT_PASSWORD_OR_USERNAME'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except IntegrityError:
                # Cuando se va a pedir un Token
                # y se ejecuta 'Token.objects.create(user=user)'
                # Si el usuario ya tiene un Token lanza la Excepción
                # IntegrityError:
                return Response(
                    {'status': 400,'message': 'ALREADY_HAVE_TOKEN'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Si request.data.get('username') o request.data.get('password') es None
            # Significa que el usuario no envio desde el cliente el nombre de usuario
            # O la contraseña por tal motivo no se puede autenticar
            return Response(
                {'status': 400,'message': 'USERNAME_OR_PASSWORD_IS_NONE'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TokenLogOutView(viewsets.ViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializers

    # Eliminar Token y Salir de la Sesión
    # POST: api/v1/users/api-token-logout/
    def create(self, request):
        # Si las credenciales de autenticación enviadas son correctas
        # entonces 'request.user' tiene un objeto de tipo 'User'

        isThereUser = False
        user = None

        if request.data.get('headers') and request.data.get('headers').get('Authorization'):
            tokenKey = request.data.get('headers').get('Authorization').split(' ')[1]
            token = Token.objects.get(key=tokenKey)
            user = User.objects.get(pk=token.user_id)
            
            if user is not None:
                isThereUser = True

        if isThereUser:
            try:
                # Eliminar la sesión el la BB
                user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):
                pass
            
            # Cerrar Sesión
            logout(request)

            # Respuesta Exitosa
            return Response(
                {'status': 200,'message': "LOGOUT_WAS_SUCCESSFUL"},
                status=status.HTTP_200_OK
            )
        
        # Respuesta Fallida
        return Response(
                {'status': 400,'message': "LOGOUT_DONT_WAS_SUCCESSFUL"},
                status=status.HTTP_400_BAD_REQUEST
            )

class TokenToRoleView(viewsets.ViewSet):

    # El cliente envia un token y este metodo responde con el role
    # del usuario al que pertenece el token
    # POST: api/v1/users/token-role/
    def create(self, request):
        if request.data.get('headers') and request.data.get('headers').get('Authorization'):
            tokenKey = request.data.get('headers').get('Authorization').split(' ')[1]
            token = Token.objects.get(key=tokenKey)
            user = User.objects.get(pk=token.user_id)

            people = People.objects.select_related("user").filter(user_id=user.id)
            people = people[0]

            if people is not None:
                return Response(
                    {
                        'status': 200,'message': "OK",
                        'role_name': people.role.name,
                        'role_id': people.role.id
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            {'status': 400,'message': "HTTP_400_BAD_REQUEST"},
            status=status.HTTP_400_BAD_REQUEST
        )
        