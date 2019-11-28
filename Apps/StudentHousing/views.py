from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import *
from .models import *
from Apps.Users.models import *

from django.contrib.auth.models import User
from Apps.Users.models import People, Owner

# Create your views here.

# path: api/v1/users/residencePublication/
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

        print(data)

        # request.data: Tiene el siguiente diccionario de datos
        # {
        #   owner: string,
        #   name: string,
        #   price: integer,
        #   address: string,
        #   locality: integer id,
        #   services: ids list,
        #   description: string,
        #   city: integer id,
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

        # Registrar residencia
        residence = ResidencePublication(
            name=request.data.get('name'),
            photo=request.data.get('photo'),
            price=request.data.get('price'),
            address=request.data.get('address'),
            rules=request.data.get('rules'),
            locality = request.data.get('locality'),
            neighborhood = '',
            owner=people.owner,
            description=request.data.get('description')
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

from requests import post

class UploadPhotoView(viewsets.ModelViewSet):
    queryset = ResidencePublication.objects.all()
    serializer_class = ResidencePublicationSerializers

    def create(self, request):
        # Url del servicio para guardar imagenes
        url = "https://api.imgbb.com/1/upload"

        # Body: key de la api y la imagen a guardar
        payload = {
            "key": 'd853d7157ae198506590c3305ed90fe0',
            "image": request.data.get('file').split('base64,')[1],
        }
        # Se realiza la peticion
        res = post(url, payload)
        # pasar la respuesta a formato json
        data = res.json()

        # Obtener la url de la respuesta
        url = data.get('data').get('url')

        # Responder con el estatus y la url
        return Response({'status': 201, 'message': 'OK', 'url': url }, status=status.HTTP_201_CREATED)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class QualificationView(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializers

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers

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