from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import People, Role, Owner
from .serializers import PeopleSerializers, RoleSerializers, OwnerSerializers


class OwnerView(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializers


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

            obj = People(
                name=data['name'],
                lastName=data['lastName'],
                age=data['age'],
                nickname=data['nickname'],
                password=data['password'],
                avatar=data['avatar'],
                mail=data['mail'],
                token=data['token'],
                role=role,
                sex=data['sex']
            )
            obj.save()
        elif data['role'] == 3:
            # Registar Propietario
            # id_role=3,   ==> Propietario
            
            role = Role.objects.get(id=data['role'])
            owner = Owner.objects.get(id=data['owner'])

            obj = People(
                name=data['name'],
                lastName=data['lastName'],
                age=data['age'],
                nickname=data['nickname'],
                password=data['password'],
                avatar=data['avatar'],
                mail=data['mail'],
                token=data['token'],
                role=role,
                owner=owner,
                sex=data['sex']
            )
            obj.save()
        else:
            return Response({'status': 400, 'message': 'BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 201, 'message': 'OK'},status=status.HTTP_201_CREATED)