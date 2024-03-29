from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from Apps.Users.models import *

from django.contrib.auth.models import User
from Apps.Users.models import People, Owner

# Create your views here.

# path: api/v1/student_housing/residence_publication/
class ResidencePublicationView(viewsets.ModelViewSet):
    queryset = ResidencePublication.objects.all()
    serializer_class = ResidencePublicationSerializers

    # GET: api/v1/users/residencePublication/?id=<number>
    def list(self, request):
        if request.query_params.get('id'):
            residence = ResidencePublication\
                .objects\
                .filter(id=request.query_params.get('id'))\
                .prefetch_related('services')

            if(len(residence) >= 1):
                serializer = ResidencePublicationSerializers(residence[0], many=False)
            else:
                serializer = ResidencePublicationSerializers(residence, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            residence = ResidencePublication.objects.all()
            serializer = ResidencePublicationSerializers(residence, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: api/v1/users/residencePublication/
    def create(self, request):
        data = request.data

        # print(data)

        # request.data: Tiene el siguiente diccionario de datos
        # {
        #   owner: string,
        #   name: string,
        #   price: integer,
        #   address: string,
        #   locality: string,
        #   services: ids list,
        #   description: string,
        #   city: string,
        #   rules: string,
        #   photo: string 
        # }

        # Buscar un propietario en la base de datos
        user = User.objects.filter(username=request.data.get('owner'))[0]

        # Validación
        if user is None:
            return Response({'status': 400, 'message': 'USERNAME_DONT_EXIST'})

        # Buscar los datos del usuario, asociados al propietario
        people = People.objects.select_related("user").filter(user_id=user.id)[0]

        # Validación
        if people is None or people.owner is None:
            return Response({'status': 400, 'message': 'OWNER_DONT_EXIST'})


        location = Location(
            city=request.data.get('city'),
            neighborhood='',
            locality=request.data.get('locality'),
            address=request.data.get('address')
        )
        location.save()

        # Registrar residencia
        residence = ResidencePublication(
            name=request.data.get('name'),
            photo=request.data.get('photo'),
            price=request.data.get('price'),
            rules=request.data.get('rules'),
            owner=people.owner,
            description=request.data.get('description'),
            location=location
        )
        # Guardar el registro
        residence.save()
        
        servicesArr =  request.data.get('services')

        # Registar los servicios asociados a la recidencia
        for index in range(len(servicesArr)):
            service = Service.objects.get(id=servicesArr[index])
            residence.services.add(service)
            residence.save()
        
        # Respuesta Positiva
        return Response({'status': 201, 'message': 'OK'}, status=status.HTTP_201_CREATED)

from requests import post

class UploadPhotoView(viewsets.ModelViewSet):
    queryset = ResidencePublication.objects.all()
    serializer_class = ResidencePublicationSerializers

    def create(self, request):
        url = "https://api.imgbb.com/1/upload"

        payload = {
            "key": 'd853d7157ae198506590c3305ed90fe0',
            "image": request.data.get('file').split('base64,')[1],
        }
        res = post(url, payload)

        data = res.json()

        url = data.get('data').get('url')

        return Response({'status': 201, 'message': 'OK', 'url': url }, status=status.HTTP_201_CREATED)

class Search(APIView):

    def get(self, request, format=None):
        return Response([])

    def post(self, request, format=None):
        # print(request.data)

        data = request.data

        dataResponse = []

        if data.get('name') == '' or data.get('name') == ' ':
            dataResponse = ResidencePublication.objects.filter(
                (
                    Q(price__gte=int(data.get('MinPrice'))) &
                    Q(price__lte=int(data.get('MaxPrice')))
                )
            )
        else:
            dataResponse = ResidencePublication.objects.filter(
                Q(name__contains=data.get('name')) |
                (
                    Q(price__gte=int(data.get('MinPrice'))) &
                    Q(price__lte=int(data.get('MaxPrice')))
                )
            )

        serializer = ResidencePublicationSerializers(dataResponse, many=True)

        return Response({"message": "received", "data": serializer.data})

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class QualificationView(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializers

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers

class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers

    def create(self, request):
        data = request.data

        # request.data: Tiene el siguiente diccionario de datos
        # {
        #   "description" = string
        #   "publication" = id
        #   "people" = id

        # }
        # Buscar persona de la Base de datos
        people=People.objects.get(id=request.data.get('people'))
        # Buscar la publicacion en la Base de Datos
        publication=ResidencePublication.objects.get(id=request.data.get('publication'))

        # Crear el registro de notificacion asociando la persona y la publicacion de residencia
        notification = Notification(
            description= request.data.get('description'),
            person = people,
            publication = publication
        )
        # Guardar la notificacion
        notification.save()
        return Response({'status': 201, 'message': 'OK'}, status=status.HTTP_201_CREATED)

class ReportView(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializers

class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

class PromotionView(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializers